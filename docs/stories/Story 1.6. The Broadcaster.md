# Story 1.6: The Broadcaster

### Status
- [ ] Draft
- [ ] Approved
- [ ] InProgress
- [ ] Review
- [ ] Done

### Story
**As a** Developer,
**I want** the server, upon receiving a message, to broadcast it to all other connected clients,
**so that** users can have a conversation.

### Acceptance Criteria
1.  **Client Management:** The server must maintain a list or dictionary of all active client connections.
2.  **Registration:** When a client sends a `join` message, they are added to this list with their username.
3.  **Broadcast Logic:** When the server receives a `chat` message from "Alice", it iterates through the client list and sends the message to "Bob" and "Charlie" (but not back to "Alice").
4.  **Protocol:** The broadcasted message must follow the `architecture.md` format: `{"type": "message", "from": "Alice", "data": "Hello!"}`.
5.  **Verification:**
    *   Start the server.
    *   Connect Client A ("Alice").
    *   Connect Client B ("Bob").
    *   When Alice types "Hi", the server console should show that it is *sending* the message to Bob's connection. (We can't see it on Bob's client yet, that's the next story).

### Dev Notes
*   **Data Structure:** A dictionary is a good choice to store clients, mapping the connection object (`conn`) to the username. `clients = {conn_a: "Alice", conn_b: "Bob"}`.
*   **Thread Safety:** Accessing this shared `clients` dictionary from multiple threads at the same time can cause a **race condition**. We must use a `threading.Lock()` to protect it. Any time a thread wants to add, remove, or loop over the dictionary, it must `acquire()` the lock first and `release()` it after. This is a critical interview topic.