import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
load_dotenv()  
from gptBackend import agent_executor

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/get-response', methods=['POST', 'OPTIONS'])
def get_response():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    elif request.method == 'POST':
        data = request.get_json()
        user_message = data['message']
        try:
            # Use AgentExecutor to get the response
            response = agent_executor({"input": user_message})["output"]
            return jsonify({'response': response})
        except Exception as e:
            app.logger.error('Error in get_response: %s', str(e))
            return jsonify({'error': str(e)}), 500

def _build_cors_preflight_response():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.errorhandler(500)
def internal_error(error):
    app.logger.error('Server Error: %s', str(error))
    return "500 error"

# api.py
import json

@app.route('/api/savePreferences', methods=['POST'])
def save_preferences():
    data = request.get_json()
    learning_prefs = data['learningPreferences']
    app.logger.debug("Learning preferences received: %s", learning_prefs)

    # Write preferences to a file
    try:
        with open('learning_preferences.json', 'w') as file:
            json.dump(learning_prefs, file)
        return jsonify({'status': 'success'})
    except Exception as e:
        app.logger.error('Error in save_preferences: %s', str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import openai
# from dotenv import load_dotenv
# load_dotenv()  
# from gptBackend import agent_executor

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# openai.api_key = os.getenv("OPENAI_API_KEY")

# @app.route('/get-response', methods=['POST', 'OPTIONS'])
# def get_response():
#     if request.method == 'OPTIONS':
#         return _build_cors_preflight_response()
#     elif request.method == 'POST':
#         data = request.get_json()
#         user_message = data['message']
#         try:
#             # Use AgentExecutor to get the response
#             response = agent_executor({"input":user_message})["output"]
#             return jsonify({'response': response})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# def _build_cors_preflight_response():
#     response = jsonify({})
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#     return response


# # api.py
# import json

# @app.route('/api/savePreferences', methods=['POST'])
# def save_preferences():
#     data = request.get_json()
#     learning_prefs = data['learningPreferences']
#     print("this is here")
#     print(learning_prefs, "learning prefs")

#     # Write preferences to a file
#     with open('learning_preferences.json', 'w') as file:
#         json.dump(learning_prefs, file)

#     return jsonify({'status': 'success'})



# if __name__ == '__main__':
#     app.run(debug=True)
