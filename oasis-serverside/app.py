from flask import Flask, request, jsonify, Blueprint, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from ai_handlers import get_crop_recommendations, analyze_plant_image
from google import genai
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import tempfile
import logging
import os
import pathlib
from functools import wraps

# Simple in-memory user store (for demonstration purposes)
# In a real application, use a proper database
USERS = {
    "admin": "password"
}

# Simple token store (in a real app, use a more secure method like JWT)
SESSIONS = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token not in SESSIONS:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function



# Configuration
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
DEFAULT_RATE_LIMIT = os.getenv("RATE_LIMIT", "100 per minute")
CHAT_RATE_LIMIT = os.getenv("CHAT_RATE_LIMIT", "20 per minute")
CROP_RATE_LIMIT = os.getenv("CROP_RATE_LIMIT", "10 per minute")
PLANT_HEALTH_RATE_LIMIT = os.getenv("PLANT_HEALTH_RATE_LIMIT", "8 per minute")
FRONTEND_DIST = os.getenv("FRONTEND_DIST", str(pathlib.Path(__file__).resolve().parents[1] / "client" / "dist"))


def create_app() -> Flask:
    app = Flask(__name__)

    # Security and size limits
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024

    # Logging
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, log_level, logging.INFO))
    logger = logging.getLogger("oasis")

    @app.before_request
    def _log_request():
        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.path,
                "remote_addr": request.headers.get("X-Forwarded-For", request.remote_addr),
            },
        )

    @app.after_request
    def _log_response(response):
        logger.info(
            "response",
            extra={
                "status": response.status_code,
                "path": request.path,
            },
        )
        # Security headers
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        return response

    # CORS
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
    CORS(
        app,
        resources={r"/api/*": {"origins": [o.strip() for o in allowed_origins.split(",") if o.strip()]}},
        supports_credentials=False,
    )

    # Rate Limiting
    limiter = Limiter(get_remote_address, app=app, default_limits=[DEFAULT_RATE_LIMIT])

    # Health and readiness endpoints
    @app.route("/healthz")
    def healthz():
        return jsonify({"status": "ok"})

    @app.route("/readyz")
    def readyz():
        ready = bool(os.getenv("GEMINI_API_KEY"))
        return (jsonify({"ready": ready}), 200 if ready else 503)

    # Initialize AI client lazily to avoid startup failures
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    chat_session = client.chats.create(model="gemini-2.5-flash")

    # API Blueprint
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    @api_bp.route("/login", methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        username = data.get("username")
        password = data.get("password")

        if username in USERS and USERS[username] == password:
            # Simple token generation (in a real app, use a more secure method like JWT)
            token = f"token_for_{username}"
            SESSIONS[token] = username
            return jsonify({"token": token})
        
        return jsonify({"message": "Invalid credentials"}), 401

    @api_bp.route("/register", methods=["POST"])
    def register():
        data = request.get_json(silent=True) or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        if username in USERS:
            return jsonify({"message": "Username already exists"}), 400

        USERS[username] = password
        return jsonify({"message": "User registered successfully"}), 201

    @api_bp.route("/chat", methods=["POST"])
    @limiter.limit(CHAT_RATE_LIMIT)
    @login_required
    def chat():
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or "").strip()
        user_name = (data.get("name") or "Friend").strip()
        if not user_message:
            return jsonify({"reply": "Please enter a message."}), 400
        try:
            persona_and_instructions = (
                "Your name is Oasis, a professional plant assistant dedicated to providing "
                "comprehensive and accurate information for gardening needs."
            )
            full_prompt = (
                f"Hello {user_name}! {persona_and_instructions} Now, please respond to the user's question:\n{user_message}"
            )
            response = chat_session.send_message(full_prompt)
            return jsonify({"reply": response.text})
        except Exception as e:
            logging.exception("chat_error")
            return jsonify({"reply": f"Error: {str(e)}"}), 500

    @api_bp.route("/crop-plan", methods=["POST"])
    @limiter.limit(CROP_RATE_LIMIT)
    @login_required
    def crop_plan():
        data = request.get_json(silent=True) or {}
        user_info = (data.get("user_info") or "").strip()
        if not user_info:
            return jsonify({"error": "user_info is required"}), 400

        recommendations_text = get_crop_recommendations(user_info)
        recommendations_list = [line.strip() for line in recommendations_text.split("\n") if line.strip()]
        return jsonify(
            {
                "recommendations_text": recommendations_text,
                "recommendations_list": recommendations_list,
            }
        )

    def _allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

    @api_bp.route("/plant-health", methods=["POST"])
    @limiter.limit(PLANT_HEALTH_RATE_LIMIT)
    @login_required
    def plant_health():
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400
        if not _allowed_file(file.filename):
            return jsonify({"error": "Unsupported file type"}), 400

        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(prefix="oasis_", suffix=f"_{filename}", delete=False) as tmp:
            file_path = tmp.name
            file.save(file_path)
        try:
            diagnosis = analyze_plant_image(file_path)
            return jsonify({"diagnosis": diagnosis})
        finally:
            try:
                os.remove(file_path)
            except Exception:
                logging.exception("cleanup_failed")

    # Register blueprint
    app.register_blueprint(api_bp)

    # 413 handler
    @app.errorhandler(413)
    def request_entity_too_large(_):
        return jsonify({"error": f"File too large. Max {MAX_UPLOAD_MB} MB"}), 413

    # Root route
    @app.route("/")
    def root():
        return jsonify({"status": "My Oasis backend is running!", "health": "/healthz", "ready": "/readyz"})

    # Serve SPA (if built assets exist)
    dist_path = pathlib.Path(FRONTEND_DIST)

    @app.route("/assets/<path:filename>")
    def assets(filename: str):
        if dist_path.exists():
            return send_from_directory(dist_path / "assets", filename)
        return ("Not Found", 404)

    @app.route("/<path:path>")
    def spa_catch_all(path: str):
        if path.startswith("api/"):
            return ("Not Found", 404)
        index_file = dist_path / "index.html"
        if dist_path.exists() and index_file.exists():
            return send_from_directory(dist_path, "index.html")
        return ("Not Found", 404)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
