# Manual Deployment Guide: Running PyNet Chat on EC2

This guide walks you through launching a virtual server (EC2), opening the firewall (Security Group), and running your Python chat server manually.

## Prerequisites
*   An AWS Account (Free Tier eligible).
*   A terminal/command prompt on your local computer.
*   `git` installed on your local computer (to upload code).

---

## Step 1: Launch the Virtual Computer (EC2)

1.  Log in to the **AWS Console**.
2.  Search for **EC2** and click "Launch Instance" (orange button).
3.  **Name:** ` `
4.  **OS Images:** Select **Ubuntu** (it's user-friendly for Python).
    *   *Tip: Ensure "Free tier eligible" is tagged under the name.*
5.  **Instance Type:** Select **t2.micro** (or t3.micro). This is the free one.
6.  **Key Pair:**
    *   Click "Create new key pair".
    *   Name it `pynet-key`.
    *   Select `.pem` (for Mac/Linux) or `.ppk` (for Windows PuTTY).
    *   **Download it.** Keep this file safe! It is your only way to log in.

## Step 2: The Firewall (Security Group)

This is the most critical step. By default, AWS blocks everything except SSH.

1.  In the "Network settings" section, click **Edit**.
2.  **Security group name:** `pynet-chat-sg`
3.  You will see one rule already: **SSH (TCP 22)**. Leave this.
4.  Click **Add security group rule**.
    *   **Type:** Custom TCP
    *   **Port range:** `5050`
    *   **Source:** `Anywhere` (0.0.0.0/0)
    *   *Why? This allows your local computer to connect to the chat server.*
5.  Click **Launch Instance**.

## Step 3: Log In to the Server (SSH)

1.  Click **Instances** to see your new server.
2.  Wait until "Instance state" is **Running**.
3.  Click the **Instance ID** to see details.
4.  Copy the **Public IPv4 address** (e.g., `54.123.45.67`).
5.  Open your local terminal.
6.  Move your key file to a safe place (e.g., `~/.ssh/`) and change permissions (Mac/Linux only):
    ```bash
    Step 1 — Copy the key to your WSL home folder:
bashcp /mnt/d/Freelance/pynet-key.pem ~/.ssh/pynet-key.pem

Step 2 — Set the correct permissions:

bashchmod 400 ~/.ssh/pynet-key.pem

Step 3 — Connect (replace with your actual IP):
bashssh -i ~/.ssh/pynet-key.pem ubuntu@54.123.45.67


It's recommended to copy it to ~/.ssh/ rather than using it directly from the Windows path, because WSL sometimes has permission issues with files stored on Windows drives, which would cause SSH to reject the key.
    ```
7.  Connect:
    ```bash
    ssh -i path/to/pynet-key.pem ubuntu@<YOUR_PUBLIC_IP>
    ```
    *   *Type "yes" if asked about fingerprints.*

## Step 4: Run the Server

Now you are "inside" the AWS computer!

1.  **Update and Install Git:**
    ```bash
    sudo apt update
    sudo apt install git -y
    ```
2.  **Get Your Code:**
    *   If your code is on GitHub:
        ```bash
        git clone https://github.com/YOUR_USERNAME/PyNetChatService.git
        cd PyNetChatService
        ```
    *   *Alternative (Copy-Paste):*
        ```bash
        nano server.py
        # Paste your server.py code here. Press Ctrl+O, Enter, Ctrl+X to save.
        ```
3.  **Run the Server:**
    **Crucial:** We must tell the server to listen on `0.0.0.0` (all interfaces), not `127.0.0.1` (localhost only).
    ```bash
    export HOST=0.0.0.0
    python3 server.py
    ```
    *   You should see: `[STARTING] Server is listening on 0.0.0.0:5050`

## Step 5: Connect Your Client

Leave the AWS terminal open (don't close it, or the server stops!).

1.  Open a **new** terminal on your **local** computer.
2.  Navigate to your project folder.
3.  Edit `client.py` (or just change the variable momentarily):
    *   Change `HOST = '127.0.0.1'` to `HOST = '<YOUR_AWS_PUBLIC_IP>'`.
4.  Run the client:
    ```bash
    python client.py
    ```
5.  **Success!** You are now chatting over the internet.

## Phase 1 Complete!

You have manually deployed a server.
*   **The downside:** If you close the SSH window, the chat stops.
*   **Next Level:** How do we keep it running forever? (Services/Docker).