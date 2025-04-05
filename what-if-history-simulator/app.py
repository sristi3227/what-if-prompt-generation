from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
API_KEY = os.getenv("HF_API_KEY")  # Get your key from .env
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

@app.route("/")
def home():
    return jsonify({"message": "What If? History Simulator API is running!"})

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"story": "Prompt is empty"}), 400

        payload = {
            "inputs": prompt.strip()
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()

            # Check if it's a list response (usual case)
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                story = result[0]["generated_text"]
            # Sometimes it might return as a dict with key 'generated_text'
            elif isinstance(result, dict) and "generated_text" in result:
                story = result["generated_text"]
            else:
                story = "No story found in response."

            return jsonify({"story": story.strip()})
        else:
            print("HF API Error:", response.status_code, response.text)
            return jsonify({"story": "Failed to generate story. Please try again"}), 500

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"story": "Internal server error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
