import requests
import time
import os

API_URL = "http://localhost:8080"
LAST_CHECK_FILE = "last_check.txt"

def get_last_check_time():
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r') as f:
            return f.read().strip()
    return None

def save_last_check_time(timestamp):
    with open(LAST_CHECK_FILE, 'w') as f:
        f.write(timestamp)

def check_new_messages():
    """Проверяет новые сообщения и выводит их"""
    try:
        response = requests.get(f"{API_URL}/api/pending-messages", timeout=5)
        if response.ok:
            data = response.json()
            messages = data.get('messages', [])

            for msg in messages:
                message_text = msg.get('message', '')
                timestamp = msg.get('timestamp', '')

                if message_text:
                    print(f"\n[WEB MESSAGE] {message_text}")

                    # Отмечаем как обработанное
                    requests.post(f"{API_URL}/api/mark-processed",
                                json={'timestamp': timestamp},
                                timeout=5)

            return len(messages)
    except Exception as e:
        print(f"Error checking messages: {e}")
    return 0

def main():
    print("Web message monitor started")
    print("Checking for new messages every 3 seconds...")
    print()

    while True:
        count = check_new_messages()
        if count > 0:
            print(f"Processed {count} message(s)")
        time.sleep(3)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nMonitor stopped")
