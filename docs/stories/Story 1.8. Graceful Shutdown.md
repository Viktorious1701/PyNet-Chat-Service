# Story 1.8: Graceful Shutdown

### Status
- [ ] Draft
- [ ] Approved
- [ ] InProgress
- [ ] Review
- [ ] Done

### Story
**As a** Developer,
**I want** the server to handle a client disconnecting unexpectedly without crashing,
**so that** the chat service remains stable for all other users.

### Acceptance Criteria
1.  **No Crash:** If a client script is forcibly closed (e.g., using Ctrl+C), the server does **not** crash or raise an unhandled exception.
2.  **Client Removal:** The disconnected client is correctly removed from the server's internal list of active clients.
3.  **Notification:** The server broadcasts a "user has left" message to all *remaining* clients.
4.  **Verification:**
    *   Start the server.
    *   Connect Client A ("Alice") and Client B ("Bob").
    *   Forcibly close Client B's terminal.
    *   Client A's terminal should display a message like `[SERVER]: Bob has left the chat.`
    *   The server's active connection count should decrease by one.

### Dev Notes
*   **Implementation:** Most of this logic is already present in the `try...except` and `finally` blocks in `server.py`. This story is about refining it and adding the broadcast notification.
*   **Protocol Addition:** We need a new message type for this. When broadcasting, the server should send: `{"type": "server_message", "data": "Username has left the chat."}`.
