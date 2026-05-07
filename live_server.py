from flask import Flask, render_template, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Путь к истории чата Claude Code
CHAT_HISTORY_PATH = os.path.expanduser('~/.claude/chat_history.json')

@app.route('/')
def index():
    return render_template('live_chat.html')

@app.route('/api/messages')
def get_messages():
    try:
        if os.path.exists(CHAT_HISTORY_PATH):
            with open(CHAT_HISTORY_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                messages = data.get('messages', [])

                # Форматируем сообщения
                formatted = []
                for msg in messages[-50:]:  # Последние 50 сообщений
                    formatted.append({
                        'role': msg.get('role', 'unknown'),
                        'content': msg.get('content', ''),
                        'timestamp': msg.get('timestamp', '')
                    })

                return jsonify({
                    'success': True,
                    'messages': formatted
                })
        else:
            return jsonify({
                'success': True,
                'messages': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
