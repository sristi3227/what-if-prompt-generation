import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Please set it in your .env file.")

# ✅ Working Hugging Face model for text generation
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 📝 Alternate History Prompt
DATA = {
    "inputs": (
        "What if dinosaurs never went extinct? Write a short alternate history story about how humans and dinosaurs coexist in the modern world."
    )
}

try:
    response = requests.post(API_URL, headers=HEADERS, json=DATA)

    if response.status_code != 200:
        print("Error:", response.json())
    else:
        print("Generated Alternate History:", response.json()[0]["generated_text"])

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
