# AWS & DevOps Deployment Plan (PyNet Chat Service)

## 1. Project Analysis: The "Stateful" Challenge

Before deploying, we must understand the nature of `server.py`.

*   **Protocol:** Raw TCP Sockets (Layer 4).
*   **State:** **Stateful**. The server keeps an in-memory dictionary `clients = {}`.
*   **Implication:** If you run two copies of the server (scaling out), Client A on Server 1 **cannot** talk to Client B on Server 2 because the servers don't share memory.
*   **DevOps Strategy:** For this "Phase 1" learning, we will deploy a **Single Instance** service to keep it simple, or use a **Network Load Balancer** with sticky sessions if we scale later (though Redis would be needed for true scaling).

## 2. Target AWS Architecture

We will use a **Container-based** architecture, as you already have a `Dockerfile`.

### A. Compute: AWS Fargate (ECS)
Instead of managing a raw EC2 Virtual Machine (patching OS, installing Docker), we will use **AWS Fargate**. It is "Serverless for Containers." We just say "Run this Docker image with 0.5 CPU and 256MB RAM," and AWS handles the rest.

### B. Networking: Network Load Balancer (NLB)
Standard Application Load Balancers (ALB) are for HTTP/HTTPS. Since your app uses raw TCP on port 5050, we should use a **Network Load Balancer (NLB)**.
*   **Health Checks:** The NLB will ping port 5050 to ensure the server is alive.
*   **Traffic Routing:** It passes TCP packets directly to your container.

### C. Registry: AWS ECR
We need a place to store your Docker images securely within AWS. **Amazon Elastic Container Registry (ECR)** is the AWS equivalent of Docker Hub.

### D. Logging: AWS CloudWatch
Your `print()` statements in `server.py` will automatically be captured by Fargate and sent to **CloudWatch Logs**, allowing you to debug remote connection issues.

## 3. The DevOps Pipeline (CI/CD)

We will automate the deployment using **GitHub Actions**.

**Trigger:** Push to `main` branch.

**Steps:**
1.  **Checkout Code:** Get the latest python scripts.
2.  **Login to AWS:** Authenticate with AWS credentials.
3.  **Build Docker Image:** Run `docker build`.
4.  **Push to ECR:** Upload the image to AWS private registry.
5.  **Update ECS Service:** Tell AWS Fargate to pull the new image and replace the old running container.

## 4. Implementation Checklist

To achieve this, you will need to:

1.  [ ] **AWS Setup:** Create an AWS Account and an IAM User with permissions.
2.  [ ] **Infrastructure Creation (IaC):**
    *   Create a VPC (Virtual Private Cloud) or use default.
    *   Create an ECR Repository.
    *   Create an ECS Cluster.
3.  [ ] **Pipeline Config:**
    *   Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to GitHub Secrets.
    *   Update `.github/workflows/deploy.yml` to target AWS instead of Docker Hub.

## 5. Security Groups (Firewall)

Since this is a custom TCP port (5050), you must configure the **Security Group** assigned to your Fargate task:
*   **Inbound Rule:** Allow TCP Port `5050` from `0.0.0.0/0` (Anywhere).
*   **Outbound Rule:** Allow All Traffic (to fetch updates/packages).