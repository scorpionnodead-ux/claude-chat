"""
Веб-сервер для Live Chat с Claude (Cloud Version)
Простой интерфейс для общения с Claude через веб-браузер
"""

from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Пути для облачного окружения (относительные)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_HISTORY_FILE = os.path.join(BASE_DIR, 'chat_history.json')
COMMAND_FILE = os.path.join(BASE_DIR, 'commands.txt')

def ensure_files_exist():
    """Создать файлы если их нет"""
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    if not os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, 'w', encoding='utf-8') as f:
            f.write('')

@app.route('/')
def index():
    """Главная страница - редирект на чат"""
    return render_template('chat.html')

@app.route('/chat')
def chat():
    """Страница чата"""
    return render_template('chat.html')

@app.route('/api/chat/recent')
def chat_recent():
    """Получить последние 20 сообщений чата"""
    ensure_files_exist()
    messages = []

    # Загрузить сообщения из локальной истории
    try:
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                try:
                    messages = json.load(f)
                except:
                    messages = []
    except Exception as e:
        print(f"Error loading chat history: {e}")

    # Сортировать по времени и вернуть последние 20
    messages.sort(key=lambda x: x.get('timestamp', ''))

    return jsonify({"messages": messages[-20:]})

@app.route('/api/chat/send', methods=['POST'])
def chat_send():
    """Отправить команду Claude"""
    ensure_files_exist()
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Сохранить команду в файл
    try:
        with open(COMMAND_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()}|{message}\n")
    except Exception as e:
        return jsonify({"error": f"Failed to save command: {str(e)}"}), 500

    # Сохранить в историю чата для отображения
    try:
        # Загрузить существующую историю
        history = []
        if os.path.exists(CHAT_HISTORY_FILE):
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                except:
                    history = []

        # Добавить новое сообщение
        history.append({
            'type': 'human',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })

        # Сохранить обновленную историю (последние 100 сообщений)
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history[-100:], f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Warning: Failed to save to chat history: {e}")

    return jsonify({
        "success": True,
        "message": "Command sent! Claude will see it and respond."
    })

@app.route('/api/commands/pending')
def commands_pending():
    """Получить список ожидающих команд"""
    ensure_files_exist()
    commands = []

    try:
        if os.path.exists(COMMAND_FILE):
            with open(COMMAND_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if '|' in line:
                        timestamp, cmd = line.strip().split('|', 1)
                        commands.append({
                            'timestamp': timestamp,
                            'command': cmd
                        })
    except Exception as e:
        print(f"Error reading commands: {e}")

    return jsonify({"commands": commands})

@app.route('/api/commands/clear', methods=['POST'])
def commands_clear():
    """Очистить файл команд"""
    ensure_files_exist()
    try:
        with open(COMMAND_FILE, 'w', encoding='utf-8') as f:
            f.write('')
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import socket

    # Получить локальный IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "localhost"

    print("="*60)
    print("Claude Live Chat - Web Interface (Cloud Ready)")
    print("="*60)
    print("\nServer starting...")

    print("\n[*] Access URLs:")
    print(f"1. This PC: http://localhost:5000")
    print(f"2. Local network: http://{local_ip}:5000")

    print("\n[*] Cloud deployment ready for:")
    print("   - Fly.io")
    print("   - Render.com")
    print("   - Railway.app")

    print("\nPress Ctrl+C to stop")
    print("="*60)

    # Создать файлы при запуске
    ensure_files_exist()

    # Запуск сервера
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
