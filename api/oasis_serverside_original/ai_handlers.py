from __future__ import annotations

# Import the original implementation from the monorepo path
# Vercel's Python builder uses the /api directory as the module root,
# so we vendor a copy by reading relative to the repository at build time.

# For simplicity in this environment, directly copy the logic here.

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_crop_recommendations(user_info: str, bot_name: str = "Oasis") -> str:
    try:
        def _classify_input(text: str) -> str:
            t = text.strip().lower()
            spaces = {"balcony", "patio", "small yard", "raised bed", "container", "pots", "balcony garden"}
            seasons = {"spring", "summer", "autumn", "fall", "winter", "rainy season", "dry season"}
            if any(s in t for s in spaces):
                return "space"
            if any(s in t for s in seasons):
                return "season"
            return "location"

        kind = _classify_input(user_info)

        prompt = (
            f"You are a helpful and knowledgeable South African gardening assistant named {bot_name}. "
            "Your sole task is to provide a structured gardening guide for a home garden in a specific location in South Africa. "
            "Strictly follow all instructions below.\n\n"
            f"**User input (place):** {user_info}\n\n"
            "**Instructions (MUST BE FOLLOWED PRECISELY):**\n"
            "1.  **Greeting & Introduction:** Your response MUST start with the exact phrase:"
            f"'Hello, I’m {bot_name}! Let’s plan your garden in {user_info}.' "
            "Add an emoji at the end of this line. For example, 🌱 or 🌿.\n"
            "2.  **Local Flavor:** Immediately following the greeting, provide a brief 2-3 sentence introduction about the specified location. This must include its geography, province/region, general climate, and a cultural or agricultural note.\n"
            "3.  **Structure and Formatting:** You MUST format the response using the following structure, using the exact Markdown headings, bolding, and horizontal rules (---) as shown. Do not deviate from this structure or add extra sections.\n"
            "---"
            "## General Growing Conditions for {user_info}:"
            " * **Climate:** [Describe the climate here]"
            " * **Sunlight:** [Give a sunlight recommendation here]"
            " * **Soil:** [Advise on soil conditions here]"
            "---"
            "## Low-Maintenance & Space-Efficient Crop Recommendations:"
            " * **Year-Round Staples:** [List 3-4 crops here]"
            " * **Herbs:** [List 5-6 herbs here]"
            "---"
            "## Seasonal Recommendations for {user_info}:"
            " * **Spring (Sept–Oct):** [List crops here]"
            " * **Summer (Nov–Mar):** [List crops here]"
            " * **Autumn (Apr–May):** [List crops here]"
            " * **Winter (Jun–Aug):** [List crops here]"
            "---"
            "## General Low-Maintenance Tips:"
            " * [Provide 4-5 practical tips here]"
            "---"
            "4.  **Closing:** End the response with a single, encouraging closing statement, signed off with your name. For example: "
            f"'Happy gardening! – {bot_name}'"
            "5.  **Tone & Content:** The tone must be warm, knowledgeable, and friendly. All recommendations must be practical and specific to the region. Do not include excessive details or sub-lists for each crop."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:  # noqa: BLE001
        return f"Error fetching crop recommendations: {e}"


essage_prefix = "Assess this image for diseases or pests and suggest low-cost remedies for a home garden in South Africa."


def analyze_plant_image(image_path: str) -> str:
    try:
        uploaded_file = client.files.upload(file=image_path)
        prompt = message_prefix
        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=[prompt, uploaded_file],
        )
        return "".join([stream.text for stream in response])
    except Exception as e:  # noqa: BLE001
        return f"Error analyzing plant image: {e}"
