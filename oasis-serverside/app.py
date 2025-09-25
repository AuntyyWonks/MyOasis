from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_handlers import get_crop_recommendations, analyze_plant_image
from google import genai
import os

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chat_session = client.chats.create(model="gemini-2.5-flash")

@app.route("/")
def index():
    return "My Oasis backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    user_name = data.get("name", "John")
    if not user_message:
        return jsonify({"reply": "Please enter a message."}), 400
    try:
        # The core persona and instructions for the model
        persona_and_instructions = "Your name is Oasis, a professional plant assistant dedicated to providing comprehensive and accurate information for gardening needs."

        full_prompt = ( f"Hello {user_name}! {persona_and_instructions} Now, please respond to the user's question:\n{user_message}")

        response = chat_session.send_message(full_prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500
    
@app.route("/crop-plan", methods=["POST"])
def crop_plan():
    data = request.json
    user_info = data.get("user_info", "").strip()
    if not user_info:
        return jsonify({"error": "user_info is required"}), 400

    recommendations_text = get_crop_recommendations(user_info)

    recommendations_list = [
        line.strip() for line in recommendations_text.split("\n") if line.strip()
    ]

    return jsonify({
        "recommendations_text": recommendations_text,  # full text
        "recommendations_list": recommendations_list  # structured list
    })

@app.route("/plant-health", methods=["POST"])
def plant_health():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = f"temp_{file.filename}"
    file.save(file_path)
    try:
        diagnosis = analyze_plant_image(file_path)
    finally:
        os.remove(file_path)

    return jsonify({"diagnosis": diagnosis})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
