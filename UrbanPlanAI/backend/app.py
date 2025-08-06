import os
import json
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
app = Flask(__name__)
CORS(
    app, origins="*", methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"]
)


# --- Force CORS headers manually ---
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://urban-infra.vercel.app"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# --- Gemini Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# --- Prompt Template ---
PROMPT = """
You are "UrbanInfra", an AI agent specializing in urban planning and green space development...
[TRUNCATED FOR BREVITY – KEEP FULL PROMPT AS BEFORE]
"""


# --- Status Route ---
@app.route("/")
def status():
    return jsonify({"status": "Backend is running"}), 200


# --- Main Image Analyze Endpoint ---
@app.route("/analyze", methods=["POST", "OPTIONS"])
def analyze_image():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    if not data or "imageUrl" not in data:
        return jsonify({"error": "imageUrl not provided"}), 400

    image_url = data["imageUrl"]

    try:
        # Fetch image
        response = requests.get(image_url)
        response.raise_for_status()

        image_content = response.content
        mime_type = response.headers.get("Content-Type", "image/png")

        if not mime_type.startswith("image/"):
            return jsonify({"error": "Invalid image type"}), 400

        model = genai.GenerativeModel("gemini-pro-vision")
        image_part = {"mime_type": mime_type, "data": image_content}

        result = model.generate_content([PROMPT, image_part])
        parsed = json.loads(result.text.strip())

        return jsonify(parsed), 200

    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch image", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# --- Entry Point ---
if __name__ == "__main__":
    app.run(debug=True)
