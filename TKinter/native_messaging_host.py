import json
import sys

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        sys.exit(0)
    message_length = int.from_bytes(raw_length, byteorder='little')
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def send_message(message):
    encoded_content = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(len(encoded_content).to_bytes(4, byteorder='little'))
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.buffer.flush()

while True:
    received_message = read_message()
    if received_message.get('action') == 'openUrl':
        url = received_message.get('url')
        # Perform actions with the received URL, e.g., open it in a browser
        print(f"Received URL: {url}")
        # Send a response back to the extension
        send_message({'received': True})
