from __future__ import annotations

import os
from google import genai

# Keep implementation minimal here, import original where possible

from oasis_serverside_original.ai_handlers import (
    get_crop_recommendations as _orig_get_crop_recommendations,
    analyze_plant_image as _orig_analyze_plant_image,
)


def get_crop_recommendations(user_info: str, bot_name: str = "Oasis") -> str:
    return _orig_get_crop_recommendations(user_info, bot_name)


def analyze_plant_image(image_path: str) -> str:
    return _orig_analyze_plant_image(image_path)
