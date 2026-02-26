# Deployment Roadmap: From Localhost to AWS

## Phase 1: The Manual Way (Mental Model)
Before using fancy tools, imagine how you would do this manually. This helps understand what the automation tools (DevOps) are actually doing for you.

1.  **The Computer:** You go to AWS and click "Launch Instance" (EC2). This is just a remote Linux computer.
2.  **The Firewall:** You tell AWS "Allow traffic on port 5050." This is a **Security Group**.
3.  **The Code:** You SSH (log in) to that remote computer, run `git clone ...`, and then `python server.py`.
4.  **The Connection:** Your friend runs `client.py` on their laptop, but instead of typing `127.0.0.1`, they type the **Public IP** of that AWS computer.

### The Problem with the Manual Way
*   **It stops when you sleep:** If you close your terminal, the program stops.
*   **It doesn't restart:** If the server crashes, it stays down until you wake up and restart it.
*   **It's hard to update:** To change code, you have to log in, stop the server, `git pull`, and start it again.

## Phase 2: The DevOps Way (Scenario C)
We use tools to automate the manual steps above.

### 1. "The Computer" -> Auto Scaling Group
Instead of manually launching a server, we define a "Launch Template."
*   **Concept:** "Hey AWS, whenever I need a server, please create a `t2.micro` with these exact settings."
*   **Benefit:** If the server dies, AWS automatically creates a new identical one.

### 2. "The Firewall" -> Infrastructure as Code (Terraform)
Instead of clicking buttons in the console to open Port 5050, we write a text file (`main.tf`).
*   **Concept:** "I declare that Port 5050 must be open."
*   **Benefit:** You can't accidentally forget a setting next time. It's saved in a file.

### 3. "Keep it Running" -> ECS (Elastic Container Service)
Instead of running `python server.py` manually, we wrap it in **Docker**.
*   **Docker:** Packages your python version and code into a box.
*   **ECS:** A manager that takes that box and puts it on the server.
*   **Benefit:** ECS watches your app. If `server.py` crashes, ECS says "Oh no!" and instantly restarts the Docker container.

## 4. "Updating Code" -> CI/CD (GitHub Actions)
Instead of SSH-ing in to `git pull`, we use a pipeline.
1.  You push code to GitHub.
2.  GitHub Actions automatically builds a new Docker box.
3.  It tells ECS: "Hey, use this new box version."
4.  ECS stops the old one and starts the new one automatically.

## Summary of Terms

| Your Local Term | AWS/DevOps Term | What it does |
| :--- | :--- | :--- |
| **My Laptop** | **EC2 Instance** | The physical CPU/RAM running the code. |
| **Terminal Window** | **Docker Container** | An isolated environment where the code runs. |
| **Me restarting the script** | **ECS Service** | The robot that ensures the code is always running. |
| **Port 5050** | **Security Group** | The firewall rule allowing connections. |