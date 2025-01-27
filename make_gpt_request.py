import requests
import os
from dotenv import load_dotenv
from logger_creation import logger

load_dotenv()

API_KEY = os.getenv('GPT_KEY_CHATGPT')
logger.info(API_KEY)
API_URL = "https://api.openai.com/v1/chat/completions"

def get_gpt_response(prompt, max_tokens=500):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

# Example usage
"""
user_input = input("Введите ваш запрос: ")
bot_response = get_gpt_response(user_input)
print("Ответ от GPT:", bot_response)
"""