import requests
import time
import sys
from datetime import datetime

API_URL = "http://localhost:8080"

def check_and_display_messages():
    """Проверяет и отображает новые сообщения"""
    try:
        response = requests.get(f"{API_URL}/api/pending-messages", timeout=5)
        if response.ok:
            data = response.json()
            messages = data.get('messages', [])

            for msg in messages:
                message_text = msg.get('message', '')
                timestamp = msg.get('timestamp', '')

                if message_text:
                    print(f"\n{'='*60}")
                    print(f"[WEB MESSAGE] {message_text}")
                    print(f"Time: {timestamp}")
                    print(f"{'='*60}\n")
                    sys.stdout.flush()

                    # Отмечаем как обработанное
                    requests.post(f"{API_URL}/api/mark-processed",
                                json={'timestamp': timestamp},
                                timeout=5)

            return len(messages)
    except Exception as e:
        pass
    return 0

def save_assistant_message(content):
    """Сохраняет ответ ассистента в историю"""
    try:
        # Получаем текущую историю
        response = requests.get(f"{API_URL}/api/messages", timeout=5)
        if response.ok:
            # Добавляем новое сообщение через API
            history_response = requests.get("http://localhost:8080/api/messages")
            # Сохраняем напрямую в файл
            import json
            history_file = "C:/scripts/WebControl/chat_history.json"
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, list):
                data.append({
                    'type': 'assistant',
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                })
            else:
                data['messages'].append({
                    'type': 'assistant',
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                })

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass

# Запускаем проверку каждые 3 секунды
print("Auto-check started. Monitoring web messages every 3 seconds...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        count = check_and_display_messages()
        time.sleep(3)
except KeyboardInterrupt:
    print("\nAuto-check stopped")
