# PyNet Chat Service Product Requirements Document (PRD) - Phase 1

## 1. Goals and Background Context

### Goals
*   **Educational Goal:** Master Python `socket` programming and understanding the flow of data at OSI Layers 4 (Transport) and 7 (Application).
*   **Technical Goal:** Deliver a functional CLI (Command Line Interface) chat application where multiple users can join a server and exchange messages in real-time.
*   **Professional Goal:** Create clean, documented code that can serve as the "core" module for the future Microservice refactor.

### Background Context
Most modern developers rely on heavy frameworks (like Socket.IO or Django Channels) that hide the complexity of networking. To pass the target interview, it is essential to understand what happens *under the hood*. This Phase 1 project strips away the "magic" to expose the raw mechanics of TCP handshakes, byte streams, and thread management for concurrency.

### Scope for Phase 1 (MVP)
*   **In Scope:**
    *   A central `server.py` that listens for TCP connections.
    *   A `client.py` that connects to the server.
    *   Handling multiple clients simultaneously using Threading.
    *   Broadcasting a message from one client to all other connected clients.
    *   A defined JSON message protocol.
*   **Out of Scope (Saved for Phase 2):**
    *   Database storage (messages will be held in server memory for now).
    *   User authentication (Login/Register).
    *   Docker/Containerization.

## 2. Requirements

### Functional Requirements (FR)
1.  **FR1 (Connection):** The Server must accept TCP connections on a specific port (e.g., 5050) from multiple Clients simultaneously.
2.  **FR2 (Identification):** Upon connecting, the Client must send a "Join" message containing their `username`.
3.  **FR3 (Messaging):** Users must be able to type a message in their CLI and send it to the Server.
4.  **FR4 (Broadcasting):** When the Server receives a message from User A, it must immediately send that message to *all* other connected users (User B, User C...).
5.  **FR5 (Protocol):** All data exchange must use JSON format strings (serialized to bytes) to ensure structure.

### Non-Functional Requirements (NFR)
1.  **NFR1 (Concurrency):** The Server must use Python `threading` to handle blocking I/O. One thread per client connection so the server doesn't "freeze" while waiting for one user to type.
2.  **NFR2 (Robustness):** The Server must handle abrupt disconnections (e.g., Client presses Ctrl+C) without crashing. It should gracefully remove that user from the active client list.
3.  **NFR3 (Standard Library):** The implementation must strictly use Python's built-in `socket`, `threading`, and `json` libraries. No third-party frameworks are allowed in this phase.

## 3. Technical Assumptions
*   **Language:** Python 3.x
*   **Interface:** Command Line Interface (CLI).
*   **Network:** Localhost (127.0.0.1) for testing.