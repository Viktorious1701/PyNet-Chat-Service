# Phase 3: Storing Docker Images in the Cloud (AWS ECR)

We are moving from "Building on the Server" to "Building Once, Running Anywhere."

## Step 1: Create the Repository

1.  Log in to the **AWS Console**.
2.  Search for **ECR** (Elastic Container Registry).
3.  Click **Get Started** or **Create repository**.
4.  **Visibility settings:** `Private`.
5.  **Repository name:** `pynet-chat`.
6.  Click **Create repository**.

## Step 2: Install AWS CLI on EC2

To upload images, your EC2 instance needs to talk to ECR.
*   *Note: In a real environment, we'd use an IAM Role. For this tutorial, we'll use keys.*

1.  **Go back to your SSH terminal** (on the EC2 instance).
2.  Install the AWS Command Line Interface:
    ```bash
    sudo apt install awscli -y
    ```
3.  Configure it:
    ```bash
    aws configure
    ```
    *   **AWS Access Key ID:** (Enter the Access Key from your IAM user setup)
    *   **AWS Secret Access Key:** (Enter the Secret Key)
    *   **Default region:** `us-east-1` (or whatever region you used for ECR)
    *   **Default output format:** `json`

## Step 3: Log In to ECR

We need to tell Docker to trust AWS.

1.  **Get the Login Password:**
    *   Replace `123456789012` with **your** AWS Account ID (found in top right of console).
    *   Replace `us-east-1` if you are in a different region.
    ```bash
    aws ecr get-login-password --region ap-southeast-2 | sudo docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-southeast-2.amazonaws.com/pynet-chat
    ```
    *   *If successful, it will say: `Login Succeeded`.*

## Step 4: Tag and Push

We need to re-tag our existing image so Docker knows where to send it.

1.  **Find your Image ID:**
    ```bash
    sudo docker images
    ```
    *(Copy the Image ID for `pynet-chat`, e.g., `029dbfdd4dcb`)*

2.  **Tag it:**
    ```bash
    sudo docker tag 029dbfdd4dcb 123456789012.dkr.ecr.us-east-1.amazonaws.com/pynet-chat:latest
    ```

3.  **Push it:**
    ```bash
    sudo docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/pynet-chat:latest
    ```

## Step 5: Verify

1.  Go back to the **AWS Console > ECR > pynet-chat**.
2.  You should see your image listed with the tag `latest`!

---

### Why did we do this?
Now, if you launch 10 new servers (or use ECS), they can all simply run:
`docker run ... 123456789012.dkr.ecr.us-east-1.amazonaws.com/pynet-chat:latest`

They don't need the source code. They don't need to build. They just download and run.