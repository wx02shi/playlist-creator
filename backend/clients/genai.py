import os
from google import genai

genai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
