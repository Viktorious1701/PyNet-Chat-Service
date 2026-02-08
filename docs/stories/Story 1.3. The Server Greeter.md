# Story 1.3: The Server "Greeter" (Concurrency)

### Status
- [ ] Draft
- [ ] Approved
- [ ] InProgress
- [ ] Review
- [ ] Done

### Story
**As a** Developer,
**I want** to update `server.py` to accept incoming connections and spawn a dedicated thread for each client,
**so that** the server can handle multiple users chatting simultaneously without blocking.

### Acceptance Criteria
1.  The `server.py` script is updated to include a `handle_client` function.
2.  The main loop calls `server.socket.accept()` to accept new connections.
3.  Upon acceptance, the server prints: `[NEW CONNECTION] Connected to {address}`.
4.  For every new connection, a new `threading.Thread` is started, targeting the `handle_client` function.
5.  **Verification:** I can open **two separate terminal windows**, run `client.py` in both, and the server prints "Connected" for both of them.

### Dev Notes
*   **Concept:** `socket.accept()` returns a *new* socket object (`conn`) specifically for that client. The original `server_socket` keeps listening for *new* people.
*   **Threading:** We need to import `threading`.
*   **Function Signature:** `def handle_client(conn, addr):`
*   **Loop:** The `handle_client` function needs a `while True` loop to keep listening for messages from that specific client (we will implement the message receiving logic later; for now, just keep the connection open).