import socket
import threading
import json
import os

# Configuration
# Logic Change: Use environment variable for Host binding.
# In Docker, we must bind to '0.0.0.0' to be accessible outside the container.
# Default remains '127.0.0.1' for local non-docker testing.
HOST = os.getenv('HOST', '127.0.0.1')
PORT = 5050

# Shared state for clients
clients = {}  # {conn: username, ...}
clients_lock = threading.Lock()


def broadcast(message, sender_conn):
    """
    Sends a message to all clients except the sender.
    This function is thread-safe.
    """
    with clients_lock:
        # Use list() to avoid issues with dict size changing during iteration
        for conn in list(clients.keys()):
            if conn != sender_conn:
                try:
                    conn.send(message)
                except socket.error:
                    # Client is likely disconnected, will be handled in its own thread's finally block
                    pass


def handle_client(conn, addr):
    """
    Handles a single client connection, from handshake to chat loop.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    current_username = None

    try:
        # 1. Handshake
        msg_bytes = conn.recv(1024)
        if not msg_bytes:
            return

        msg_json = json.loads(msg_bytes.decode('utf-8'))

        if msg_json.get("type") == "join":
            current_username = msg_json.get("data")
            with clients_lock:
                clients[conn] = current_username
            print(f"[{addr}] User '{current_username}' has joined the chat.")
        else:
            print(f"[{addr}] Handshake failed.")
            return

        # 2. Chat Loop
        while True:
            msg_bytes = conn.recv(1024)
            if not msg_bytes:
                break

            msg_json = json.loads(msg_bytes.decode('utf-8'))

            if msg_json.get("type") == "chat":
                print(
                    f"[{addr}] Message from '{current_username}': {msg_json['data']}")
                broadcast_msg = {
                    "type": "message", "from": current_username, "data": msg_json["data"]}
                broadcast_bytes = json.dumps(broadcast_msg).encode('utf-8')
                broadcast(broadcast_bytes, conn)

    except (ConnectionResetError, json.JSONDecodeError):
        # This happens if a client disconnects unexpectedly
        print(
            f"[INFO] Client {addr} ('{current_username}') disconnected unexpectedly.")
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
    finally:
        # 3. Cleanup and Broadcast Leave Message
        with clients_lock:
            if conn in clients:
                # Retrieve username before deleting
                current_username = clients.get(conn)
                del clients[conn]

        if current_username:
            leave_msg = {"type": "server_message",
                         "data": f"{current_username} has left the chat."}
            leave_bytes = json.dumps(leave_msg).encode('utf-8')
            broadcast(leave_bytes, conn)  # Inform others

        conn.close()
        print(
            f"[DISCONNECTED] {addr} ('{current_username}') connection closed.")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[STARTING] Server is listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\n[STOPPING] Server is shutting down...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
