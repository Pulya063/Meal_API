import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_meal_details(title: str):
    prompt = f"Ти професійний дієтолог. Напиши назви страв за цими інгредієнтами '{title}'. Відповідь має бути у форматі: 'Назва страви: '."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
