# Story 1.4: The Client "Handshake"

### Status
- [ ] Draft
- [ ] Approved
- [ ] InProgress
- [ ] Review
- [ ] Done

### Story
**As a** User,
**I want** the client to prompt me for a username and send a `join` JSON message to the server,
**so that** the server knows who I am.

### Acceptance Criteria
1.  **Input:** When `client.py` starts, it prompts: `Enter username: `.
2.  **Format:** After connecting, the client automatically sends a JSON string: `{"type": "join", "data": "Alice"}`.
3.  **Encoding:** The JSON string is encoded to `utf-8` bytes before sending.
4.  **Verification:**
    *   Run `server.py`.
    *   Run `client.py` and enter "Bob".
    *   The Server console should show the raw received bytes (we will add a print statement to the server to verify this).

### Tasks
- [ ] Import `json` in `client.py`.
- [ ] Add `input()` to get the username.
- [ ] Create a dictionary: `{"type": "join", "data": username}`.
- [ ] Use `json.dumps()` to convert the dict to a string.
- [ ] Use `.encode('utf-8')` to convert the string to bytes.
- [ ] Send bytes using `client_socket.send()`.