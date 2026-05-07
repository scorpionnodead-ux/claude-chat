from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Путь к истории чата
CHAT_HISTORY_PATH = os.path.join(os.getcwd(), 'chat_history.json')

def load_history():
    if os.path.exists(CHAT_HISTORY_PATH):
        with open(CHAT_HISTORY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Если это массив, оборачиваем в объект
            if isinstance(data, list):
                return {'messages': data}
            return data
    return {'messages': []}

def save_history(data):
    with open(CHAT_HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('live_chat.html')

@app.route('/chat')
def chat():
    return render_template('web_chat.html')

@app.route('/api/messages')
def get_messages():
    try:
        history = load_history()
        messages = history.get('messages', [])

        # Если messages это список, берём последние 50
        if isinstance(messages, list):
            messages = messages[-50:]
        else:
            messages = []

        # Конвертируем type -> role для совместимости
        formatted = []
        for msg in messages:
            formatted.append({
                'role': msg.get('type', msg.get('role', 'unknown')),
                'content': msg.get('content', ''),
                'timestamp': msg.get('timestamp', '')
            })

        return jsonify({
            'success': True,
            'messages': formatted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Сохраняем сообщение пользователя
        history = load_history()
        history['messages'].append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        save_history(history)

        # Отправляем в Claude Code CLI
        result = subprocess.run(
            ['claude', 'chat', message],
            capture_output=True,
            text=True,
            timeout=60
        )

        response = result.stdout.strip()

        # Сохраняем ответ Claude
        history = load_history()
        history['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        save_history(history)

        return jsonify({
            'success': True,
            'response': response
        })

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Request timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
