from flask import Flask, request, jsonify
from flask_cors import CORS
from collecting_links import generate_links_file
from links_to_ideas import generate_ideas


app = Flask(__name__)
CORS(app)

@app.route('/generate_video', methods=['POST'])
def gen():
    data = request.get_json()
    user_input = data.get('text', '')
    generate_links_file(user_input)
    ideas = generate_ideas()
    return jsonify({'bot_response': ideas})

if __name__ == '__main__':
    app.run(debug=True)