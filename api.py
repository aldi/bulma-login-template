import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import openai
from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/get-response', methods=['POST', 'OPTIONS'])
def get_response():
    if request.method == 'OPTIONS':
        # This will allow preflight requests, which are made by browsers
        return _build_cors_preflight_response()
    elif request.method == 'POST':
        data = request.get_json()
        user_message = data['message']
        try:
            chat_completion = openai.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": user_message
                }],
                model="gpt-3.5-turbo",
            )
            chat_response = chat_completion.choices[0].message.content
            return jsonify({'response': chat_response})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def _build_cors_preflight_response():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)
