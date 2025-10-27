from __future__ import annotations

import os
import pathlib
import tempfile
import logging
from typing import Optional

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from google import genai

# Config
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "8"))
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
DEFAULT_RATE_LIMIT = os.getenv("RATE_LIMIT", "100 per minute")
CHAT_RATE_LIMIT = os.getenv("CHAT_RATE_LIMIT", "20 per minute")
CROP_RATE_LIMIT = os.getenv("CROP_RATE_LIMIT", "10 per minute")
PLANT_HEALTH_RATE_LIMIT = os.getenv("PLANT_HEALTH_RATE_LIMIT", "8 per minute")


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


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
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        return response

    # CORS (Vercel will serve same-origin front-end by default)
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
    CORS(
        app,
        resources={r"/api/*": {"origins": [o.strip() for o in allowed_origins.split(",") if o.strip()]}},
        supports_credentials=False,
    )

    # Rate Limiting
    limiter = Limiter(get_remote_address, app=app, default_limits=[DEFAULT_RATE_LIMIT])

    # Health endpoints
    @app.get("/api/healthz")
    def healthz():
        return jsonify({"status": "ok"})

    @app.get("/api/readyz")
    def readyz():
        ready = bool(os.getenv("GEMINI_API_KEY"))
        return (jsonify({"ready": ready}), 200 if ready else 503)

    # Initialize AI client lazily
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    chat_session = client.chats.create(model="gemini-2.5-flash")

    api_bp = Blueprint("api", __name__, url_prefix="/api")

    @api_bp.post("/chat")
    @limiter.limit(CHAT_RATE_LIMIT)
    def chat():
        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or "").strip()
        user_name = (data.get("name") or "Friend").strip()
        if not user_message:
            return jsonify({"reply": "Please enter a message."}), 400
        try:
            persona_and_instructions = (
                "Your name is Oasis, a professional plant assistant providing accurate gardening information."
            )
            full_prompt = (
                f"Hello {user_name}! {persona_and_instructions} Now, please respond to the user's question:\n{user_message}"
            )
            response = chat_session.send_message(full_prompt)
            return jsonify({"reply": response.text})
        except Exception as e:  # noqa: BLE001
            logging.exception("chat_error")
            return jsonify({"reply": f"Error: {str(e)}"}), 500

    @api_bp.post("/crop-plan")
    @limiter.limit(CROP_RATE_LIMIT)
    def crop_plan():
        from oasis_serverside.ai_handlers import get_crop_recommendations  # lazy import for Vercel cold start

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

    @api_bp.post("/plant-health")
    @limiter.limit(PLANT_HEALTH_RATE_LIMIT)
    def plant_health():
        from oasis_serverside.ai_handlers import analyze_plant_image  # lazy import

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
            except Exception:  # noqa: BLE001
                logging.exception("cleanup_failed")

    app.register_blueprint(api_bp)

    # Root
    @app.get("/")
    def root():
        return jsonify({"status": "My Oasis backend on Vercel", "health": "/api/healthz", "ready": "/api/readyz"})

    @app.errorhandler(413)
    def request_entity_too_large(_):
        return jsonify({"error": f"File too large. Max {MAX_UPLOAD_MB} MB"}), 413

    return app


# Vercel entrypoint
app = create_app()
