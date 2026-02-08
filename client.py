import socket
import sys
import json
import threading

# Configuration
HOST = '127.0.0.1'
PORT = 5050


def receive_messages(client_socket):
    """
    Listens for messages from the server in a separate thread.
    """
    try:
        while True:
            # Wait for message (Blocking)
            msg_bytes = client_socket.recv(1024)
            if not msg_bytes:
                # Server has closed the connection
                print("[INFO] Server disconnected. Press Enter to exit.")
                break

            # Decode and display the message
            msg_json = json.loads(msg_bytes.decode('utf-8'))

            # Ensure the message has the expected structure
            if msg_json.get("type") == "message":
                sender = msg_json.get("from")
                data = msg_json.get("data")
                print(f"\n[{sender}]: {data}")
            else:
                # Handle other message types from server if any (e.g., server announcements)
                print(
                    f"\n[SERVER]: {msg_json.get('data', 'Received an unknown message type.')}")

    except ConnectionResetError:
        print("[INFO] Connection to server was lost. Press Enter to exit.")
    except Exception:
        # We can ignore errors that happen when the main socket is closing
        pass


def start_client():
    # 1. Get Username
    username = input("Enter username: ")
    if not username:
        print("Username cannot be empty.")
        sys.exit(0)

    # 2. Connect
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
        print(f"[SUCCESS] Connected to server. Type 'quit' to exit.")

        # 3. Send Handshake
        join_message = {"type": "join", "data": username}
        client_socket.send(json.dumps(join_message).encode('utf-8'))

        # 4. Start Receiver Thread
        # This thread will run 'receive_messages' in the background
        receiver_thread = threading.Thread(
            target=receive_messages, args=(client_socket,))
        # Allows main thread to exit even if this thread is running
        receiver_thread.daemon = True
        receiver_thread.start()

        # 5. Chat Loop (Main Thread)
        while True:
            msg = input("You: ")

            if msg.lower() == 'quit':
                break

            chat_message = {"type": "chat", "data": msg}
            client_socket.send(json.dumps(chat_message).encode('utf-8'))

    except (ConnectionRefusedError, KeyboardInterrupt):
        print(f"\n[INFO] Disconnecting from server.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        client_socket.close()
        print("[CLOSED] Connection closed.")


if __name__ == "__main__":
    start_client()
