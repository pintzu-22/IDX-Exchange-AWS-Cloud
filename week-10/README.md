## Week 10 — CI/CD & DevOps Practices

### Objective

This week's lab focused on automating the deployment of the PropertyLite Flask API to Amazon ECS using GitHub Actions and AWS OIDC authentication, without needing to save AWS access keys in GitHub Secrets.

### Environment Setup

Since I deleted all the AWS resources after Week 9, I used the same Terraform configuration to rebuild the environment.

To rebuild the AWS environment, I completed the following steps:

- Turned off the NAT Gateway to save money.
- Fixed a spelling mistake in `portMappings` in the ECS Task Definition.
- Created the ECR repository again.
- Built and uploaded the original PropertyLite Docker image to ECR.
- Used Terraform to rebuild the VPC, Security Group, ECS Cluster, Task Definition, and ECS Service.

Terraform successfully created 23 AWS resources.

**Initial API response:**

```json
{"status":"ok"}
```

### Lab 10.1 — GitHub Actions to AWS via OIDC

#### Step 1 — Create an OIDC Identity Provider

I set up an OIDC identity provider in AWS IAM with the following settings:

- Provider URL: `https://token.actions.githubusercontent.com`
- Audience: `sts.amazonaws.com`

This allows AWS to verify the identity of GitHub Actions without using AWS access keys.

#### Step 2 — Create an IAM Role

I created an IAM role called `github-actions-deploy-role` and added two policies:

- `AmazonECS_FullAccess`
- `AmazonEC2ContainerRegistryPowerUser`

I set up the trust policy so that only my GitHub repository's `main` branch could use this role.

These policies allow GitHub Actions to upload Docker images to ECR and deploy new versions of the application to ECS.

#### Step 3 — Create the GitHub Actions Workflow

I created a `deploy.yml` file in the `.github/workflows/` folder at the root of my repository.

Every time I push code to the `main` branch, GitHub Actions automatically runs the following steps:

1. Download the latest code from GitHub.
2. Get temporary AWS credentials using OIDC.
3. Log in to Amazon ECR.
4. Build and tag the Docker image.
5. Upload the new Docker image to ECR.
6. Update the ECS service to run the new version of the application.

The workflow requires the following permissions:

```yaml
permissions:
  id-token: write
  contents: read
```

- `id-token: write` allows GitHub Actions to request an OIDC token to authenticate with AWS.
- `contents: read` allows GitHub Actions to read the code in my repository.

I also saved a copy of `deploy.yml` in `week-10/.github/workflows/` as part of the lab deliverable.

### Step 4 — Verify the Automated Deployment

I added a version number to the `/health` endpoint in `propertylite/app.py` to check if GitHub Actions could successfully deploy the updated code.

**Before:**

```python
@app.route("/health")
def health():
    return jsonify(status="ok")
```

**After:**

```python
@app.route("/health")
def health():
    return jsonify(status="ok", version="1.1")
```

After committing and pushing the changes to GitHub, GitHub Actions automatically started the deployment process.

Once the new ECS task was running, I used its public IP address to test the API with the `curl` command.

**Before deployment:**

```json
{"status":"ok"}
```

**After deployment:**

```json
{"status":"ok","version":"1.1"}
```

The API returned version 1.1, which confirmed that GitHub Actions successfully built a new Docker image and deployed the updated application to ECS.

I did not need to manually build or push the Docker image or update the ECS service.

### Debug Lab 10.2 — OIDC Authentication Failure

**Issue:** GitHub Actions could not assume the AWS IAM role.

**Error:**

```text
Not authorized to perform sts:AssumeRoleWithWebIdentity
```

**Root Cause:** My IAM trust policy used the old OIDC subject format. My GitHub repository used a newer format that required the Owner ID and Repository ID.

**Fix:** I checked my GitHub Owner ID and Repository ID and added them to the IAM trust policy.

After updating the trust policy, I reran the workflow. GitHub Actions successfully connected to AWS and logged in to ECR.

**Key Takeaway:** The OIDC subject in the IAM trust policy must match the identity information provided by GitHub Actions.

### Additional Debugging

#### Issue 1 — Docker Push Network Failure

**Issue:** I could not finish uploading the Docker image to ECR.

**Error:**

```text
use of closed network connection
write: broken pipe
```

**Root Cause:** The network connection was interrupted during the upload.

**Fix:** I restarted Docker Desktop and changed the proxy settings, but the problem continued. I then switched from Wi-Fi to my phone's personal hotspot, and the upload succeeded.

**Key Takeaway:** If a Docker push fails, check the network connection before changing AWS permissions or Docker settings.

#### Issue 2 — Dockerfile Not Found

**Issue:** GitHub Actions could not build the Docker image.

**Error:**

```text
failed to read dockerfile:
open Dockerfile: no such file or directory
```

**Root Cause:** The Dockerfile was on my local computer, but I had not uploaded it to GitHub.

**Fix:** I added, committed, and pushed `propertylite/Dockerfile` to GitHub. The workflow then successfully built and deployed the updated application to ECS.

**Key Takeaway:** GitHub Actions uses the files in the GitHub repository, not the files on my local computer.

### Why OIDC Is Safer Than AWS Access Keys

Without OIDC, GitHub Actions can use AWS access keys stored in GitHub Secrets. These keys can remain valid for a long time, which creates a security risk if someone gets access to them.

With OIDC, GitHub Actions can use temporary AWS credentials instead of saving AWS access keys in GitHub Secrets.

The benefits of using OIDC include:

- No need to store AWS access keys in GitHub Secrets.
- Temporary credentials expire automatically.
- AWS can control which GitHub repository and branch can access its resources.
- Lower risk of credentials being exposed.
- No need to manually update or rotate long-lived access keys.

This makes OIDC a safer way for GitHub Actions to connect to AWS.

### Blue/Green Deployment

Blue/green deployment is a way to update an application without interrupting the existing service.

- **Blue:** The current version of the application.
- **Green:** The new version of the application.

Once the new version is tested and working properly, users are switched to the new version. If something goes wrong, users can be switched back to the old version.

In this lab, I learned the concept of blue/green deployment, but I used ECS rolling deployment to update my application instead.

### Resource Cleanup

After testing the CI/CD pipeline, I cleaned up the AWS resources to avoid extra costs.

#### Step 1 — Disable GitHub Actions

I disabled the GitHub Actions workflow so that future Git pushes would not trigger another deployment.

#### Step 2 — Destroy Terraform Resources

I ran the following command in the `week-10` directory:

```bash
terraform destroy
```

This deleted the 23 resources created by Terraform, including the VPC, subnets, Security Group, ECS Cluster, Task Definition, ECS Service, and Task Execution Role.

I then checked if any resources were left in the Terraform State:

```bash
terraform state list
```

No resources were listed.

#### Step 3 — Delete the ECR Repository

Since I created the ECR repository manually, I had to delete it separately.

```bash
aws ecr delete-repository \
  --repository-name property-api \
  --region us-east-1 \
  --force
```

The `--force` option deleted both the repository and all Docker images inside it.

#### Step 4 — Clean Up IAM Resources

I deleted the IAM role `github-actions-deploy-role` and the GitHub OIDC identity provider from AWS IAM.

#### Step 5 — Save the GitHub Actions Workflow

I saved a copy of `deploy.yml` in:

`week-10/.github/workflows/deploy.yml`

I removed the original workflow from the repository root to prevent future deployments.

**Result:** All AWS resources created for this lab were deleted. I kept the Terraform configuration, workflow file, README, and screenshots for future use.

**Key Takeaway:** Terraform can only delete the resources it manages. I need to manually delete any resources that I created outside of Terraform.

### Key Takeaways

- I learned how to use GitHub Actions to automate application deployment.
- OIDC allows GitHub Actions to connect to AWS using temporary credentials without saving AWS access keys in GitHub Secrets.
- Terraform makes it easier to rebuild and delete AWS resources.
- Amazon ECR stores Docker images, while Amazon ECS runs the application.
- CI/CD saves time by automating the Docker build, push, and deployment process.
- Adding a version number to the API helps confirm that the new code has been deployed successfully.
- Checking error logs helps identify and fix deployment problems.
- Cleaning up unused AWS resources helps avoid extra costs.