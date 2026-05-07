"""
Веб-сервер для Live Chat с Claude
Простой интерфейс для общения с Claude через веб-браузер
"""

from flask import Flask, render_template, jsonify, request
import os
import json
from datetime import datetime

app = Flask(__name__)

# Пути
CHAT_LOG_PATH = r"C:\Users\DENDY\.claude\projects\C--scripts\fa955348-558b-4e87-bb45-185417f33faa.jsonl"
COMMAND_FILE = r"C:\scripts\WebControl\commands.txt"

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
    messages = []

    # Загрузить сообщения из основного чата Claude
    try:
        if os.path.exists(CHAT_LOG_PATH):
            with open(CHAT_LOG_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-100:]:
                    if line.strip():
                        try:
                            msg = json.loads(line)
                            msg_type = msg.get('type', '')

                            # Получить message объект
                            message_obj = msg.get('message', {})
                            role = message_obj.get('role', '')
                            content_data = message_obj.get('content', '')

                            content = ''

                            # Обработка строкового контента
                            if isinstance(content_data, str):
                                content = content_data
                            # Обработка массива контента
                            elif isinstance(content_data, list):
                                for item in content_data:
                                    if isinstance(item, dict):
                                        item_type = item.get('type', '')
                                        # Текстовый контент
                                        if item_type == 'text':
                                            content += item.get('text', '')
                                        # Пропустить tool_use и tool_result
                                        elif item_type in ['tool_use', 'tool_result']:
                                            continue
                                    elif isinstance(item, str):
                                        content += item

                            # Определить тип сообщения
                            display_type = 'assistant' if role == 'assistant' else 'human'

                            # Добавить только если есть текстовый контент
                            if content.strip() and len(content) > 10:
                                # Пропустить системные сообщения
                                if 'tool_use_id' not in str(content_data):
                                    messages.append({
                                        'type': display_type,
                                        'content': content[:1000],
                                        'timestamp': msg.get('timestamp', '')
                                    })
                        except Exception as e:
                            continue
    except Exception as e:
        pass

    # Добавить сообщения из локальной истории (команды с веб-интерфейса)
    try:
        chat_history_file = os.path.join(os.path.dirname(COMMAND_FILE), 'chat_history.json')
        if os.path.exists(chat_history_file):
            with open(chat_history_file, 'r', encoding='utf-8') as f:
                try:
                    history = json.load(f)
                    messages.extend(history)
                except:
                    pass
    except Exception as e:
        pass

    # Сортировать по времени и вернуть последние 20
    messages.sort(key=lambda x: x.get('timestamp', ''))

    return jsonify({"messages": messages[-20:]})

@app.route('/api/chat/send', methods=['POST'])
def chat_send():
    """Отправить команду Claude"""
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Сохранить команду в файл для Claude
    try:
        with open(COMMAND_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().isoformat()}|{message}\n")
    except Exception as e:
        return jsonify({"error": f"Failed to save command: {str(e)}"}), 500

    # Также сохранить в историю чата для отображения
    try:
        chat_history_file = os.path.join(os.path.dirname(COMMAND_FILE), 'chat_history.json')

        # Загрузить существующую историю
        history = []
        if os.path.exists(chat_history_file):
            with open(chat_history_file, 'r', encoding='utf-8') as f:
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

        # Сохранить обновленную историю
        with open(chat_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Warning: Failed to save to chat history: {e}")

    return jsonify({
        "success": True,
        "message": "Command sent! Claude will see it and respond."
    })

if __name__ == '__main__':
    import socket

    # Получить локальный IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except:
        local_ip = "192.168.0.103"

    print("="*60)
    print("Claude Live Chat - Web Interface")
    print("="*60)
    print("\nServer starting...")

    print("\n[*] Access URLs:")
    print(f"1. This PC: http://localhost:5000")
    print(f"2. Local network: http://{local_ip}:5000")

    print("\n[*] For mobile access:")
    print(f"   Open browser and go to: http://{local_ip}:5000")
    print("   (Make sure device is on the same Wi-Fi network)")

    print("\n[*] For remote access:")
    print("   Due to network restrictions, use one of these:")
    print("   - VPN (Tailscale, ZeroTier)")
    print("   - Port forwarding on router")
    print("   - SSH tunnel: ssh -R 80:localhost:5000 serveo.net")

    print("\nPress Ctrl+C to stop")
    print("="*60)

    # Запуск сервера на всех интерфейсах
    app.run(host='0.0.0.0', port=5000, debug=False)
