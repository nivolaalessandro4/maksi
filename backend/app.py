from flask import Flask, request, jsonify, session
from chatbot import Chatbot

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
chatbot = Chatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message')
        user_id = data.get('user_id', 'default_user')  # Default user ID if not provided

        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # Get response from the chatbot
        response = chatbot.get_response(user_input, user_id)
        return jsonify({'message': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        user_input = data.get('feedback')
        user_id = data.get('user_id', 'default_user')  # Default user ID if not provided

        if not user_input:
            return jsonify({'error': 'No feedback provided'}), 400

        # Handle feedback
        response = chatbot.get_response(user_input, user_id)
        return jsonify({'message': response})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
