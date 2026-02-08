
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
| Connection-oriented | Connectionless |
| Reliable (guarantees delivery) | Unreliable (no delivery guarantee) |
| Ordered (messages arrive in sequence) | Unordered |
| Used for: HTTP, email, chat | Used for: video streaming, gaming |

### OSI Model Layers Used

1. **Layer 4 (Transport)**: TCP protocol ensures reliable data transmission
2. **Layer 7 (Application)**: Custom JSON protocol defines message structure

### The Socket Lifecycle

#### Server Side:
