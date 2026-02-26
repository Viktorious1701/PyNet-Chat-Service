# Phase 2: Dockerizing on EC2

Currently, you are running `python3 server.py`. We are going to switch to running a **Docker Container**. This prepares you for the final step (ECS).

## Step 1: Install Docker on EC2

You are still logged into your AWS terminal (`ubuntu@ip-172-31...`). Run these commands:

1.  **Install Docker:**
    ```bash
    sudo apt update
    sudo apt install docker.io -y
    ```
2.  **Start Docker:**
    ```bash
    sudo systemctl start docker
    sudo systemctl enable docker
    ```
3.  **Check it:**
    ```bash
    sudo docker --version
    ```

## Step 2: Build the Image

We need to turn your `server.py` and `Dockerfile` into a runnable image.

1.  **Build command:**
    *(Make sure you are inside the `PyNet-Chat-Service` folder)*
    ```bash
    sudo docker build -t pynet-chat .
    ```
    *   `-t pynet-chat`: Names the image "pynet-chat".
    *   `.`: Look for the Dockerfile in the current directory.

2.  **Verify:**
    ```bash
    sudo docker images
    ```
    You should see `pynet-chat` in the list.

## Step 3: Run in the Background (Detached)

This is the magic step.

1.  **Stop your old Python server:**
    If `python3 server.py` is still running, press **Ctrl+C** to stop it.

2.  **Run the Container:**
    ```bash
    sudo docker run -d -p 5050:5050 --restart always --name chat-server pynet-chat
    ```

    **What do these flags do?**
    *   `-d`: **Detached**. Run in the background. It won't close when you close the terminal.
    *   `-p 5050:5050`: **Port Mapping**. Connects EC2 Port 5050 to Container Port 5050.
    *   `--restart always`: **Resilience**. If the app crashes or the server reboots, Docker will automatically start it again.
    *   `--name`: Gives it a friendly name.

## Step 4: Verify It Works

1.  **Check running containers:**
    ```bash
    sudo docker ps
    ```
    You should see your container running.

2.  **Check the logs:**
    Since it's in the background, you can't see the "New Connection" text anymore. Use this:
    ```bash
    sudo docker logs -f chat-server
    ```
    *(Press Ctrl+C to exit logs, this won't stop the server)*

3.  **Test your Client:**
    Run `client.py` on your local laptop again. It should connect exactly as before!

## Step 5: The Ultimate Test

1.  **Close your AWS SSH Terminal.** (Type `exit` or close the window).
2.  Run `client.py` on your laptop.
3.  **It still works!** You have successfully deployed a resilient background service.