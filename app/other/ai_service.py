import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def generate_meal_details(title: str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"You are a professional nutritionist. Write the name of the dish using these ingredients: '{title}'. The answer should be in the following format and in english: 'First word of the name of the dish'"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text
