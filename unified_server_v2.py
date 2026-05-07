from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Пути
CHAT_HISTORY_PATH = os.path.join(os.getcwd(), 'chat_history.json')
PENDING_MESSAGES_PATH = os.path.join(os.getcwd(), 'pending_messages.json')
PERMISSION_REQUESTS_PATH = os.path.join(os.getcwd(), 'permission_requests.json')

def load_history():
    if os.path.exists(CHAT_HISTORY_PATH):
        with open(CHAT_HISTORY_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return {'messages': data}
            return data
    return {'messages': []}

def save_history(data):
    with open(CHAT_HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_pending_messages():
    if os.path.exists(PENDING_MESSAGES_PATH):
        with open(PENDING_MESSAGES_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_pending_messages(messages):
    with open(PENDING_MESSAGES_PATH, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def load_permission_requests():
    if os.path.exists(PERMISSION_REQUESTS_PATH):
        with open(PERMISSION_REQUESTS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_permission_requests(requests):
    with open(PERMISSION_REQUESTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('live_chat.html')

@app.route('/chat')
def chat():
    return render_template('interactive_chat.html')

@app.route('/live')
def live():
    return render_template('live_chat.html')

@app.route('/api/messages')
def get_messages():
    try:
        history = load_history()
        messages = history.get('messages', [])

        if isinstance(messages, list):
            messages = messages[-50:]
        else:
            messages = []

        # Конвертируем type -> role
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
        # Сохраняем в историю
        history = load_history()
        history['messages'].append({
            'type': 'human',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        save_history(history)

        # Добавляем в очередь для CLI
        pending = load_pending_messages()
        pending.append({
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'processed': False
        })
        save_pending_messages(pending)

        return jsonify({
            'success': True,
            'message': 'Message queued for Claude Code CLI'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pending-messages')
def get_pending_messages():
    """Endpoint для CLI чтобы получить новые сообщения"""
    try:
        pending = load_pending_messages()
        unprocessed = [m for m in pending if not m.get('processed', False)]

        return jsonify({
            'success': True,
            'messages': unprocessed
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mark-processed', methods=['POST'])
def mark_processed():
    """Отметить сообщение как обработанное"""
    data = request.json
    timestamp = data.get('timestamp')

    try:
        pending = load_pending_messages()
        for msg in pending:
            if msg.get('timestamp') == timestamp:
                msg['processed'] = True
        save_pending_messages(pending)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/permission-requests')
def get_permission_requests():
    """Получить активные запросы разрешений"""
    try:
        requests = load_permission_requests()
        active = [r for r in requests if not r.get('answered', False)]

        return jsonify({
            'success': True,
            'requests': active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/answer-permission', methods=['POST'])
def answer_permission():
    """Ответить на запрос разрешения"""
    data = request.json
    request_id = data.get('request_id')
    answer = data.get('answer')  # 'yes' or 'no'

    try:
        requests = load_permission_requests()
        for req in requests:
            if req.get('id') == request_id:
                req['answered'] = True
                req['answer'] = answer
                req['answered_at'] = datetime.now().isoformat()
        save_permission_requests(requests)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
