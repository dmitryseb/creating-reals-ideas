import requests

# Replace with your vsegpt.ru API key
API_KEY = ""
API_URL = "https://api.vsegpt.ru/v1/chat/completions"  # Example endpoint, check their docs

def get_gpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",  # Replace with the model they support
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

# Example usage
user_input = input("Введите ваш запрос: ")
bot_response = get_gpt_response(user_input)
print("Ответ от GPT:", bot_response)

