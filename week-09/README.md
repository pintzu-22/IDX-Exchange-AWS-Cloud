## Week 09 — Containers & Orchestration

### Objective

The week's lab focus on how to containerize the PropertyLite Flask API using Docker and deploy it to AWS ECS Fargate using Terraform.

I also learned how Amazon ECR stores Docker images and how ECS runs containers without requiring me to manage EC2 servers.

### Lab 9.1 — Deploy PropertyLite to ECS Fargate

#### 1. Create a Docker Image

I created a `Dockerfile` using Python and the existing PropertyLite Flask API from previous labs.

The Dockerfile installs the required Python packages, copies the application files, and runs the API on port 8080.

I built the Docker image using:

```bash
docker build -f week-09/Dockerfile -t property-api ./propertylite
```

I used the `linux/amd64` platform option when building the image for ECS Fargate compatibility.

#### 2. Push Docker Image to Amazon ECR

I created an ECR repository named `property-api`.

Then I logged in to Amazon ECR, tagged the Docker image, and pushed it to the repository.

```bash
docker tag property-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/property-api:latest
```

```bash
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/property-api:latest
```

The image was successfully uploaded to Amazon ECR.

#### 3. Deploy ECS Fargate Using Terraform

I created a `main.tf` file to deploy the infrastructure.

The Terraform configuration included:

- VPC with public and private subnets
- Internet Gateway and NAT Gateway
- ECS Cluster (`training-cluster`)
- IAM Task Execution Role
- ECS Task Definition
- ECS Fargate Service (`property-api-service`)
- Security Group for network access

The ECS Task Definition used:

| Setting | Value |
|---|---|
| Launch Type | Fargate |
| CPU | 256 (0.25 vCPU) |
| Memory | 512 MiB |
| Container Port | 8080 |
| Desired Count | 1 |
| Region | us-east-1 |

I deployed the infrastructure using:

```bash
terraform init
terraform plan
terraform apply
```

#### 4. Verify ECS Deployment

I used AWS CLI to check the ECS Service:

```bash
aws ecs describe-services --cluster training-cluster --services property-api-service --query "services[0].runningCount"
```

**Result:**

```text
1
```

This showed that my ECS Task was running successfully.

Next, I found the Task's Public IP and used it to test my Flask API.

```bash
curl http://$PUBLIC_IP:8080/health
```

**Result:**

```json
{"status":"ok"}
```

The API was successfully deployed and accessible through ECS Fargate.

---

### Debug Lab 9.2 — ECS Deployment Issues

#### Issue 1 — Invalid Docker Image URI

**Problem:** Terraform failed to create the ECS Task Definition.

**Error:**

```text
Container.image contains invalid characters
```

**Root Cause:** I forgot to replace `<account-id>` in the Docker image URI with my actual AWS Account ID.

**Fix:** I updated the image URI in `main.tf` and ran `terraform apply` again.

#### Issue 2 — ECS Could Not Connect to Amazon ECR

**Problem:** The ECS Task remained in `PENDING` and failed to start.

**Error:**

```text
ResourceInitializationError:
unable to pull registry auth from Amazon ECR
```

**Root Cause:** The Security Group did not allow outbound HTTPS traffic to Amazon ECR.

**Fix:** I created a Security Group that allowed outbound TCP port 443 and attached it to the ECS Service using Terraform.

After applying the changes, the ECS Task successfully entered the `RUNNING` state.

#### Issue 3 — API Connection Timeout

**Problem:** The ECS Task was running, but I could not access the Flask API.

**Error:**

```text
curl: (28) Failed to connect to port 8080
```

**Root Cause:** The Security Group did not allow inbound traffic on port 8080.

**Fix:** I added an inbound rule allowing TCP port 8080 from my public IP address.

After applying the changes, the API returned:

```json
{"status":"ok"}
```

---

### Cleanup

After completing the deployment tests and saving the required screenshots, I used Terraform to destroy the infrastructure.

