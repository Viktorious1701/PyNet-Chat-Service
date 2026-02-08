# Story 1.7: The Receiver

### Status
- [ ] Draft
- [ ] Approved
- [ ] InProgress
- [ ] Review
- [ ] Done

### Story
**As a** User,
**I want** my client to listen for and display messages broadcast from the server,
**so that** I can see the conversation from other users.

### Acceptance Criteria
1.  **Concurrency:** The `client.py` script must use `threading`.
2.  **Main Thread:** The main thread will be responsible for getting user input (`input()`) and sending messages.
3.  **Receiver Thread:** A new, separate thread will be started that runs a `receive_messages` function. This function's only job is to sit in a `while True` loop and call `client_socket.recv()`.
4.  **Display:** When the receiver thread gets a message, it parses the JSON and prints it to the console in a user-friendly format (e.g., `[Alice]: Hello there!`).
5.  **Verification:**
    *   Start the server.
    *   Start Client A ("Alice").
    *   Start Client B ("Bob").
    *   When Alice types a message, it appears on **Bob's** terminal.
    *   When Bob types a message, it appears on **Alice's** terminal.

### Dev Notes
*   **The Blocking Problem:** We can't put `input()` and `recv()` in the same loop, because they are both blocking. The program would get stuck on one and never reach the other.
*   **Solution:** We put `input()` in the main loop and `recv()` in a separate thread. They run in parallel, solving the problem.