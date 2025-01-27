from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

API_KEY = "sk-or-vv-4f848a48f8b3eecfbb97c5cc5d0f558b163de9ad049ae6a0f9dac0aaa77b4ba9"
API_URL = "https://api.vsegpt.ru/v1/chat/completions"

shorts_data = [
    {"title": "Dance challenge", "hashtags": ["#dance", "#trending", "#fun"], "description": "A viral dance challenge with upbeat music."},
    {"title": "Life hacks", "hashtags": ["#lifehacks", "#tips", "#tutorial"], "description": "Quick and useful tips to make daily tasks easier."},
    {"title": "Funny skit", "hashtags": ["#comedy", "#funny", "#skit"], "description": "A short and funny skit that will make you laugh."},
]

context = "You are an expert in creating YouTube Shorts content. Below are some popular Shorts, their themes, and associated hashtags:\n"
for short in shorts_data:
    context += f"Title: {short['title']}\nHashtags: {', '.join(short['hashtags'])}\nDescription: {short['description']}\n\n"

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
        "max_tokens": 1000
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")


def make_prompt(shorts_data):
    context = "You are an expert in creating YouTube Shorts content. Below are some popular Shorts, their themes, and associated hashtags:\n"
    for short in shorts_data:
        context += f"Title: {short['title']}\nHashtags: {', '.join(short['hashtags'])}\nDescription: {short['description']}\n\n"
    return context + "Give useful ideas for short video using this information"

app = Flask(__name__)
CORS(app)

@app.route('/generate_video', methods=['POST'])
def gen():
    data = request.get_json()
    user_input = data.get('text', '')
    bot_response = get_gpt_response(make_prompt(shorts_data) + "\n" + user_input)
    return jsonify({'bot_response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)