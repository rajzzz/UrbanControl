import os
import json
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify, make_response
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
app = Flask(__name__)

CORS(app, origins=["https://urban-infra.vercel.app"])

# --- Gemini API Setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# --- Gemini Prompt ---
PROMPT = """
You are "UrbanInfra", an AI agent specializing in urban planning and green space development.
Your task is to analyze a satellite image of an urban or suburban area.

Based on the image, determine if the area is underserved with greenery.

Respond in a strict JSON format. Do not include any text or markdown formatting before or after the JSON object.

1. If the area is UNDERSERVED:
- Set "status" to "Underserved".
- Provide a "greenery_score" from 1 (very poor) to 10 (excellent).
- Provide a single, concise paragraph for "justification".
- Identify 1 to 3 potential locations for new parks. Focus on barren land, unused plots, or large concrete areas.
- For each location, provide:
  - "name": A descriptive name (e.g., "Empty Lot by Elm Street").
  - "reason": A justification for choosing this spot.
  - "location_on_image": The approximate location on the image. Choose one from: "top-left", "top-center", "top-right", "center-left", "center", "center-right", "bottom-left", "bottom-center", "bottom-right".

2. If the area has ADEQUATE greenery:
- Set "status" to "Adequate".
- Provide a "greenery_score" from 1 to 10.
- Provide a single, concise "justification" paragraph explaining why new parks are not a high priority (e.g., presence of large parks, tree-lined streets, community gardens).
"""


# --- CORS: Add headers to every response ---
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://urban-infra.vercel.app"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# --- Status check route ---
@app.route("/")
def status():
    return jsonify({"status": "Backend is running"}), 200


# --- analyze route ---
#
@app.route("/analyze", methods=["POST"])
def analyze_post():
    data = request.get_json()
    if not data or "imageUrl" not in data:
        return jsonify({"error": "imageUrl not provided"}), 400

    image_url = data["imageUrl"]

    try:
        # Download the image
        response = requests.get(image_url)
        response.raise_for_status()
        image_content = response.content
        mime_type = response.headers.get("Content-Type", "image/png")

        if not mime_type.startswith("image/"):
            return jsonify({"error": "Invalid image MIME type"}), 400

        model = genai.GenerativeModel("gemini-pro-vision")
        image_part = {"mime_type": mime_type, "data": image_content}

        result = model.generate_content([PROMPT, image_part])
        parsed = json.loads(result.text.strip())

        return jsonify(parsed), 200

    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch image", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route("/analyze", methods=["OPTIONS"])
def analyze_options():
    response = make_response("", 200)
    response.headers["Access-Control-Allow-Origin"] = "https://urban-infra.vercel.app"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# --- Run locally ---
if __name__ == "__main__":
    app.run(debug=True)
