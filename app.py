from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('web_chat.html')

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Отправляем сообщение в Claude Code CLI
        result = subprocess.run(
            ['claude', 'chat', message],
            capture_output=True,
            text=True,
            timeout=60
        )

        response = result.stdout.strip()

        return jsonify({
            'success': True,
            'response': response
        })

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Request timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
