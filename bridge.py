import requests
import time
import sys
import json

API_URL = "http://localhost:8080"

def check_pending_messages():
    """Проверяет новые сообщения из веб-интерфейса"""
    try:
        response = requests.get(f"{API_URL}/api/pending-messages", timeout=5)
        if response.ok:
            data = response.json()
            return data.get('messages', [])
    except:
        pass
    return []

def mark_as_processed(timestamp):
    """Отмечает сообщение как обработанное"""
    try:
        requests.post(f"{API_URL}/api/mark-processed",
                     json={'timestamp': timestamp},
                     timeout=5)
    except:
        pass

def main():
    print("🔄 Web-to-CLI Bridge started")
    print("Monitoring for messages from web interface...")
    print()

    while True:
        messages = check_pending_messages()

        for msg in messages:
            message_text = msg.get('message', '')
            timestamp = msg.get('timestamp', '')

            if message_text:
                print(f"\n📨 New message from web: {message_text}")
                print("Forwarding to Claude Code CLI...")

                # Отправляем сообщение в текущую сессию Claude Code
                # Это будет выглядеть как обычный ввод пользователя
                print(message_text)
                sys.stdout.flush()

                # Отмечаем как обработанное
                mark_as_processed(timestamp)

        time.sleep(2)  # Проверяем каждые 2 секунды

if __name__ == '__main__':
    main()
