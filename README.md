# Deploy a Dockerized Flask Application On AWS EC2 With Github Action CICD
![image](https://github.com/user-attachments/assets/4dd0d065-b2cc-416f-a049-589d4dfd71ed)



This guide continues from Day 1, focusing on automating the build and deployment process using GitHub Actions. It covers setting up workflows to build Docker images, push them to AWS ECR, and deploy the application to an AWS EC2 instance. The guide also includes detailed steps and explanations for each part of the workflow.

---

## Table of Contents

1. **GitHub Actions Workflow Overview**
   - Workflow Structure
   - Events and Triggers
   - Jobs and Steps

2. **Build and Push Workflow**
   - Workflow Configuration
   - Steps Explained
   - AWS ECR Integration

3. **Deploy Workflow**
   - Workflow Configuration
   - Steps Explained
   - EC2 Deployment

4. **Important Commands and Tips**
   - Docker Commands
   - AWS CLI Commands
   - GitHub Actions Tips

---

## 1. GitHub Actions Workflow Overview

GitHub Actions allows you to automate your software development workflows directly within your GitHub repository. This section provides an overview of the workflow structure, events, and jobs.

### Workflow Structure

- **Workflow File**: A YAML file that defines the automation process.
- **Events**: Triggers that start the workflow (e.g., push, pull request).
- **Jobs**: A set of steps that run on the same runner (e.g., build, deploy).
- **Steps**: Individual tasks within a job (e.g., checkout code, build Docker image).

### Events and Triggers

- **`on`**: Specifies the events that trigger the workflow.
  - `push`: Triggers when code is pushed to a specific branch.
  - `workflow_dispatch`: Allows manual triggering of the workflow.

### Jobs and Steps

- **Jobs**: Each job runs in a separate environment (e.g., Ubuntu VM).
- **Steps**: Each step performs a specific task, such as checking out code, configuring AWS credentials, or building a Docker image.

---

## 2. Build and Push Workflow

This workflow automates the process of building a Docker image and pushing it to AWS ECR.

### Workflow Configuration

```yaml
name: Build and Push

on:
  workflow_dispatch:  # Manual trigger

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        run: |
          aws ecr get-login-password --region us-east-1 | \
          docker login --username AWS --password-stdin 816069150653.dkr.ecr.us-east-1.amazonaws.com

      - name: Build Docker image
        run: |
          docker build -t 816069150653.dkr.ecr.us-east-1.amazonaws.com/flaskrepo:v1 ./day1
          docker push 816069150653.dkr.ecr.us-east-1.amazonaws.com/flaskrepo:v1
```

### Steps Explained

1. **Checkout Code**: Copies the code from the repository to the runner.
2. **Configure AWS Credentials**: Sets up AWS credentials using GitHub Secrets.
3. **Login to Amazon ECR**: Logs into AWS ECR to allow Docker to push images.
4. **Build Docker Image**: Builds the Docker image and pushes it to ECR.

---

## 3. Deploy Workflow

This workflow automates the deployment of the Docker image to an AWS EC2 instance.

### Workflow Configuration

```yaml
name: Deploy

on:
  push:
    branches:
      - master
    paths:
      - day1/**

env:
  AWS_REGION: "us-east-1"
  AWS_EC2: "flask_app"
  ECR_REPO: "flaskrepo"
  GIT_SHA: ${{ github.sha }}
  AWS_ACCOUNT_ID: "816069150653"

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        run: |
          aws ecr get-login-password --region ${{ env.AWS_REGION }} | \
          docker login --username AWS --password-stdin ${{ env.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com

      - name: Build Docker image
        run: |
          docker build -t ${{ env.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com/${{ env.ECR_REPO }}:${{ env.GIT_SHA }} ./day1
          docker push ${{ env.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com/${{ env.ECR_REPO }}:${{ env.GIT_SHA }}

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Get Public IP and SHA
        run: |
          echo "EC2_PUBLIC_IP=$(aws ec2 describe-instances --filters "Name=tag:Name,Values=${{ env.AWS_EC2 }}" --query 'Reservations[*].Instances[*].PublicIpAddress' --output text)" >> "$GITHUB_ENV"
          echo "SHA: $GITHUB_SHA"

      - name: Execute Remote SSH Commands using SSH Key
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ env.EC2_PUBLIC_IP }}
          username: ec2-user
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          port: 22
          script: |
            echo "Cleaning up the VM"
            docker rm -f $(docker ps -aq)
            docker rmi -f $(docker images -q)
            
            echo "Running container"
            aws ecr get-login-password --region ${{ env.AWS_REGION }} | docker login --username AWS --password-stdin ${{ env.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com  
            docker run -td -p 3002:5000 ${{ env.AWS_ACCOUNT_ID }}.dkr.ecr.${{ env.AWS_REGION }}.amazonaws.com/${{ env.ECR_REPO }}:${{ env.GIT_SHA }}
```

### Steps Explained

1. **Checkout Code**: Copies the code from the repository to the runner.
2. **Configure AWS Credentials**: Sets up AWS credentials using GitHub Secrets.
3. **Login to Amazon ECR**: Logs into AWS ECR to allow Docker to push images.
4. **Build Docker Image**: Builds the Docker image and pushes it to ECR.
5. **Get Public IP and SHA**: Retrieves the EC2 instance's public IP and sets the SHA.
6. **Execute Remote SSH Commands**: Connects to the EC2 instance via SSH, cleans up existing containers, and runs the new Docker container.

---

## 4. Important Commands and Tips

### Docker Commands

- **Delete All Docker Images**:
  ```bash
  docker rmi $(docker images -q)
  ```
- **Delete All Docker Containers**:
  ```bash
  docker rm $(docker ps -aq)
  ```

### AWS CLI Commands

- **Configure AWS CLI**:
  ```bash
  aws configure
  ```
- **Login to ECR**:
  ```bash
  aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com
  ```

### GitHub Actions Tips

- **Secrets Management**: Store sensitive information like AWS credentials and SSH keys in GitHub Secrets.
- **Environment Variables**: Use `env` to define reusable variables in your workflow.
- **Debugging**: Use `echo` to print variables and debug your workflow.


---

## Conclusion

This guide provides a comprehensive overview of setting up and deploying a Flask-based application using GitHub Actions, Docker, and AWS. By following these steps, you can automate your build and deployment process, making it more efficient and scalable. Whether you're deploying locally or to the cloud, this guide ensures a smooth and consistent workflow.

--- 
