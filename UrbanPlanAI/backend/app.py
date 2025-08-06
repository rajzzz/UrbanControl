# backend/app.py

import os
import json
import requests
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
app = Flask(__name__)
# Allow requests from your frontend's origin
CORS(app, resources={r"/analyze": {"origins": "http://localhost:8000"}})

# Configure the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key=GEMINI_API_KEY)


# --- Gemini Prompt Engineering ---
# This is the core instruction set for the AI model.
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

- Example of an underserved JSON response:
{
  "status": "Underserved",
  "greenery_score": 3,
  "justification": "The area is densely packed with residential buildings with very few public parks visible. The existing greenery is limited to small, private yards.",
  "recommendations": [
    {
      "name": "Barren Plot near Residential Complex",
      "reason": "A significant, undeveloped patch of land is situated next to a dense residential area, making it an ideal candidate for a community park.",
      "location_on_image": "center-left"
    },
    {
      "name": "Unused Space by the Canal",
      "reason": "The large, empty space along the canal could be transformed into a linear park, providing recreational opportunities.",
      "location_on_image": "top-right"
    }
  ]
}

2. If the area has ADEQUATE greenery:
- Set "status" to "Adequate".
- Provide a "greenery_score" from 1 to 10.
- Provide a single, concise "justification" paragraph explaining why new parks are not a high priority (e.g., presence of large parks, tree-lined streets, community gardens).
- The output for this case should look like this:
{
  "status": "Adequate",
  "greenery_score": 8,
  "justification": "This neighborhood demonstrates a healthy distribution of green spaces, including a large central park, several smaller community gardens, and abundant tree cover along the streets. Resources might be better allocated to other civic improvements."
}
"""

# --- API Endpoint ---
@app.route('/analyze', methods=['POST'])
def analyze_image():
    # Get the image URL from the frontend request
    data = request.get_json()
    if not data or 'imageUrl' not in data:
        return jsonify({"error": "imageUrl not provided"}), 400

    image_url = data['imageUrl']

    try:
        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Open the image using PIL
        image = Image.open(io.BytesIO(response.content))

        # --- Call Gemini API ---
        model = genai.GenerativeModel('gemini-2.5-pro')
        # The API expects a list of content parts [prompt, image]
        api_response = model.generate_content([PROMPT, image])

        # Clean up the response to ensure it's valid JSON
        # Gemini might wrap the JSON in ```json ... ```
        response_text = api_response.text
        if response_text.startswith("```json"):
            response_text = response_text[7:-4]

        analysis_result = json.loads(response_text)

        return jsonify(analysis_result)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to download image: {e}"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred during analysis."}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)