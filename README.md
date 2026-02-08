# PyNet Chat Service

A command-line chat application built with raw Python sockets to demonstrate TCP/IP networking fundamentals and concurrent programming patterns.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Socket Programming Concepts](#socket-programming-concepts)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Models & Protocol](#data-models--protocol)
- [Technical Skills Demonstrated](#technical-skills-demonstrated)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

**PyNet Chat Service** is an educational project designed to master low-level network programming in Python. Unlike modern chat applications that rely on high-level frameworks (Socket.IO, Django Channels, WebSockets), this project implements chat functionality from scratch using Python's built-in `socket` library.

### What This Project Does

- ✅ Allows multiple users to connect to a central chat server
- ✅ Enables real-time message broadcasting between connected clients
- ✅ Handles concurrent connections using threading
- ✅ Implements a custom JSON-based communication protocol over TCP

### Target Audience

- **Developers**: Learn socket programming, threading, and network protocols
- **Interviewers/HR**: Understand the technical skills demonstrated
- **IT Professionals**: See practical implementation of client-server architecture

---

## Features

- 🚀 **Zero Dependencies**: Built entirely with Python standard library
- 🔄 **Real-Time Messaging**: Instant message delivery to all connected clients
- 👥 **Multi-User Support**: Handle unlimited concurrent connections
- 🧵 **Thread-Safe**: Proper synchronization with threading locks
- 📝 **Custom Protocol**: JSON-based application layer protocol
- 🛡️ **Graceful Handling**: Proper connection/disconnection management
- 💬 **User Identification**: Username-based messaging system

---

## Technology Stack

This project uses **only Python standard library** components:

| Technology | Purpose | Why It Matters |
|------------|---------|----------------|
| **Python 3.x** | Programming Language | Industry-standard for network programming and scripting |
| **socket** | TCP/IP Networking | Core library for creating network connections (OSI Layer 4) |
| **threading** | Concurrency | Enables handling multiple clients simultaneously without blocking |
| **json** | Data Serialization | Structures messages in a human-readable, language-agnostic format |

### No External Dependencies

This project intentionally avoids third-party frameworks to demonstrate understanding of networking fundamentals. The `requirements.txt` file is empty because everything runs on Python's built-in libraries.

---

## Project Architecture

### Architecture Pattern: Hub-and-Spoke (Centralized Client-Server)

```
        ┌─────────┐
        │ Client A│────┐
        └─────────┘    │
                       ▼
┌─────────┐      ┌──────────┐      ┌─────────┐
│ Client B│─────▶│  SERVER  │◀─────│ Client C│
└─────────┘      └──────────┘      └─────────┘
                       ▲
        ┌─────────┐    │
        │ Client D│────┘
        └─────────┘
```

**Key Characteristics:**
- **Central Server**: Acts as the single message router and source of truth
- **Direct Client-Server Communication**: Clients never communicate directly with each other
- **Stateful Connections**: The server maintains a list of all active connections
- **Thread-Per-Client Model**: Each client connection runs in its own thread on the server

---

## Socket Programming Concepts

### What is a Socket?

A **socket** is one endpoint of a two-way communication link between two programs running on a network. Think of it like a telephone connection:
- The **server socket** is like a phone number that listens for incoming calls
- Each **client socket** is like a phone that dials that number
- Once connected, both sides can talk (send data) and listen (receive data)

### TCP vs UDP

This project uses **TCP (Transmission Control Protocol)**:

| TCP | UDP |
|-----|-----|
| ✅ Connection-oriented | ❌ Connectionless |
| ✅ Reliable (guarantees delivery) | ❌ Unreliable (no delivery guarantee) |
| ✅ Ordered (messages arrive in sequence) | ❌ Unordered |
| 📧 Used for: HTTP, email, chat | 🎮 Used for: video streaming, gaming |

### OSI Model Layers Used

1. **Layer 4 (Transport)**: TCP protocol ensures reliable data transmission
2. **Layer 7 (Application)**: Custom JSON protocol defines message structure

### The Socket Lifecycle

#### Server Side:
```
socket()  → Create a socket object
   ↓
bind()    → Attach to a specific IP address and port
   ↓
listen()  → Enter "listening" mode for incoming connections
   ↓
accept()  → Accept a connection (blocks until a client connects)
   ↓
recv()    → Receive data from the client
   ↓
send()    → Send data to the client
   ↓
close()   → Close the connection
```

#### Client Side:
```
socket()  → Create a socket object
   ↓
connect() → Connect to the server's IP and port
   ↓
send()    → Send data to the server
   ↓
recv()    → Receive data from the server
   ↓
close()   → Close the connection
```

### Concurrency with Threading

**The Problem**: Network I/O operations like `recv()` and `input()` are **blocking**. This means the program stops and waits until data arrives. Without threading, the server could only handle one client at a time.

**The Solution**: 
- **Server**: Creates a new thread for each client connection
- **Client**: Uses two threads:
  - Main thread: Handles user input
  - Daemon thread: Listens for incoming messages

**Thread Safety**: When multiple threads access shared data (like the client list), we use `threading.Lock()` to prevent race conditions.

---

## Installation

### Prerequisites

- Python 3.6 or higher
- No external packages required

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/PyNetChatService.git
   cd PyNetChatService
   ```

2. That's it! No `pip install` needed.

---

## Usage

### Starting the Server

Open a terminal and run:

```bash
python server.py
```

You should see:

```
[STARTING] Server is listening on 127.0.0.1:5050
```

The server is now ready to accept client connections.

### Connecting Clients

Open separate terminal windows for each client and run:

```bash
python client.py
```

You will be prompted:

```
Enter username: 
```

Type a username (e.g., "Alice") and press Enter. You should see:

```
[SUCCESS] Connected to server. Type 'quit' to exit.
You: 
```

### Chatting

- Type a message and press Enter to send it
- Messages from other users will appear in your terminal
- Type `quit` to disconnect

### Example Session

**Terminal 1 (Server):**

```
[STARTING] Server is listening on 127.0.0.1:5050
[NEW CONNECTION] ('127.0.0.1', 54321) connected.
[('127.0.0.1', 54321)] User 'Alice' has joined the chat.
[NEW CONNECTION] ('127.0.0.1', 54322) connected.
[('127.0.0.1', 54322)] User 'Bob' has joined the chat.
[('127.0.0.1', 54321)] Message from 'Alice': Hello Bob!
[('127.0.0.1', 54322)] Message from 'Bob': Hi Alice!
```

**Terminal 2 (Client - Alice):**

```
Enter username: Alice
[SUCCESS] Connected to server. Type 'quit' to exit.
You: Hello Bob!

[Bob]: Hi Alice!
You: 
```

**Terminal 3 (Client - Bob):**

```
Enter username: Bob
[SUCCESS] Connected to server. Type 'quit' to exit.

[Alice]: Hello Bob!
You: Hi Alice!
You: 
```

---

## Project Structure

```
PyNetChatService/
│
├── server.py                 # Main server application
├── client.py                 # Client application
├── requirements.txt          # Empty (no dependencies)
├── README.md                 # This file
│
└── docs/
    ├── prd.md                # Product Requirements Document
    ├── architecture.md       # Technical architecture specification
    │
    └── stories/              # User stories for iterative development
        ├── 1.1.The-Listening-Server.md
        ├── 1.2.The-Connecting-Client.md
        ├── 1.3.The-Server-Greeter.md
        ├── 1.4.The-Client-Handshake.md
        ├── 1.6.The-Broadcaster.md
        ├── 1.7.The-Receiver.md
        └── 1.8.Graceful-Shutdown.md
```

### Key Files

- **server.py**: Implements the chat server with threading and broadcast logic
- **client.py**: Implements the chat client with dual-threaded architecture
- **docs/prd.md**: Defines project goals, requirements, and scope
- **docs/architecture.md**: Specifies the technical design and protocol
- **docs/stories/**: Contains individual user stories for incremental development

---

## Data Models & Protocol

### Communication Protocol

All messages are exchanged as JSON strings encoded to UTF-8 bytes.

#### Client → Server Messages

**1. Join (Handshake)**

```json
{
  "type": "join",
  "data": "Alice"
}
```

**2. Chat Message**

```json
{
  "type": "chat",
  "data": "Hello World!"
}
```

#### Server → Client Messages

**1. Broadcast Message**

```json
{
  "type": "message",
  "from": "Alice",
  "data": "Hello World!"
}
```

**2. Server Announcement**

```json
{
  "type": "server_message",
  "data": "Bob has left the chat."
}
```

### Network Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Host | `127.0.0.1` | Localhost (local machine only) |
| Port | `5050` | TCP port for server listening |
| Buffer Size | `1024 bytes` | Amount of data read per `recv()` call |
| Encoding | `UTF-8` | Character encoding for text |
| Socket Type | `AF_INET, SOCK_STREAM` | IPv4, TCP |

---

## Technical Skills Demonstrated

- ✅ **Low-level networking**: Direct use of socket APIs
- ✅ **Concurrency**: Thread management and synchronization
- ✅ **Protocol design**: Custom application-layer protocol
- ✅ **Error handling**: Connection failures, unexpected disconnects
- ✅ **State management**: Maintaining shared client registry
- ✅ **Thread safety**: Using locks to prevent race conditions
- ✅ **Clean code**: Modular functions, clear variable names, comments

---

## Testing

### Test Case 1: Single Client Connection
1. Start server
2. Connect one client
3. Verify: Client can send messages (no crash)

### Test Case 2: Multi-Client Chat
1. Start server
2. Connect Client A and Client B
3. Send message from A
4. Verify: Message appears on B's terminal

### Test Case 3: Graceful Disconnect
1. Start server with 2 clients connected
2. Force-close one client (Ctrl+C)
3. Verify: Server doesn't crash, other client receives "user left" message

---

## Future Enhancements

Phase 2 features (currently out of scope):

- 🔐 User authentication (login/register)
- 💾 Message persistence (database storage)
- 💌 Private messaging
- 🐳 Containerization with Docker
- 🌐 RESTful API layer
- 🏗️ Microservices architecture
- 🔒 SSL/TLS encryption
- 📊 Chat history

---

## Development Process

This project was built using Agile user stories, demonstrating professional software development practices:

### Phase 1 Stories (MVP - All Implemented)

- ✅ **Story 1.1**: Create a server that listens for TCP connections
- ✅ **Story 1.2**: Create a client that connects to the server
- ✅ **Story 1.3**: Implement multi-threading on the server to handle multiple clients
- ✅ **Story 1.4**: Implement client handshake with username
- ✅ **Story 1.6**: Implement server broadcast logic
- ✅ **Story 1.7**: Implement client message receiving
- ✅ **Story 1.8**: Handle graceful disconnection

---

## License

This is an educational project. Feel free to use it for learning purposes.

---

## Contributing

This is an educational project, but suggestions and improvements are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## Contact

For questions or feedback about this project, please open an issue on GitHub.

---

**Happy Coding! 🚀**
