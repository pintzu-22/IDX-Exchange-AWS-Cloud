# IDX Exchange AWS Cloud Engineering Internship

This repository documents my learning and hands-on labs during the
IDX Exchange AWS Cloud Engineering Internship.

---

## Week 01 — Cloud Fundamentals & Account Setup

The AWS root user is the original account identity and has full access to all AWS services, resources, billing, and account settings. Because it has the highest level of access, it should only be used when necessary and should be protected with MFA. IAM (Identity and Access Management) is an AWS service that controls who can access AWS and what they are allowed to do. Instead of using the root user for everyday tasks, I can use IAM users with appropriate permissions. The Shared Responsibility Model explains how security responsibilities are divided between AWS and the customer. AWS is responsible for securing the physical infrastructure and services that run the cloud, while the customer is responsible for securing their accounts, access, data, and AWS resources.

---

## Week 02 — IAM & Security Foundations

## S3 Uploader Policy

**Policy:** `S3UploaderOnly-pintzu`

**Policy file:** `week-02/policies/pintzu-aws-policies.json`

This policy allows `s3:PutObject` and `s3:GetObject` for objects in `my-training-bucket-pintzu`.

This policy only gives the test user access to one specific S3 bucket. The user can upload and retrieve objects, but does not have full S3 access. This follows the principle of least privilege.

I tested the policy using the `s3test` AWS CLI profile. Running `aws s3 ls --profile s3test` returned `AccessDenied` because the test user does not have permission to list all S3 buckets.

## IAM Access Analyzer

I created an IAM Access Analyzer to monitor AWS resources for external access. The analyzer showed 0 active findings.

---

## Week 03 — EC2 Deployment and EBS Snapshot

This week, I deployed the PropertyLite Flask API to an Amazon EC2 instance using a bootstrap script in EC2 User Data.

I configured SSH access on port 22, opened port 8080 for the PropertyLite API, connected to the instance using SSH, and verified the API from my local laptop using `curl`.

I also practiced troubleshooting an SSH timeout caused by an outdated `My IP` Security Group rule.

After the deployment was working, I created an EBS snapshot of the instance's root volume and completed the required cleanup by terminating the EC2 instance and confirming that the root EBS volume was deleted.

### Key Tasks
- Launched and configured an Amazon Linux EC2 instance
- Used User Data to automatically deploy PropertyLite
- Configured Security Group rules for ports 22 and 8080
- Connected to EC2 using SSH
- Verified PropertyLite from my laptop
- Troubleshot an SSH timeout
- Created an EBS snapshot
- Cleaned up the EC2 instance and root volume

## Week 04 — Storage & Databases

This week, I learned about AWS storage and database services, including S3, EBS, EFS, RDS, and DynamoDB. I also learned about S3 storage classes, lifecycle rules, RDS Multi-AZ, and DynamoDB partition keys and capacity modes.

**What I Did:**

- **Amazon S3:** Created an S3 bucket, uploaded my Week 3 runbook, and configured a lifecycle rule to move files to Glacier Flexible Retrieval after 30 days.
- **Amazon RDS:** Created a MySQL database and connected to it through an EC2 instance in the same VPC. Imported 55,212 property records, removed 17 sensitive columns, and checked the listing IDs. I also used SQL to calculate property counts and average prices by city.
- **Amazon DynamoDB:** Created a `Properties` table using AWS CLI, set `L_ListingID` as the partition key, and used `put-item` and `get-item` to add and retrieve a record.
- **Cleanup:** Deleted the DynamoDB table, terminated the EC2 instance, and initiated deletion of the RDS database to avoid unnecessary AWS charges.


I learned that different AWS services are used for different types of data. S3 is useful for storing files, EBS works like a hard drive for EC2, and EFS lets multiple servers share files. RDS is useful for structured data and SQL queries, while DynamoDB is useful for fast lookups using keys.

**Deliverable:**
- [Week 04 — Storage & Database Decision Guide](week-04/decision-guide.md)

## Week 05 — VPC Networking

This week, I learned how AWS networking works by creating a custom VPC and connecting to a private EC2 instance through a bastion host.

### Lab 5.1 — Create a Custom VPC

I created a VPC using the AWS Console with the following settings:

- VPC name: `training-vpc`
- IPv4 CIDR: `10.0.0.0/16`
- Availability Zones: 2
- Public subnets: 2
- Private subnets: 2
- NAT Gateway: 1

This helped me understand the difference between public and private subnets and how AWS manages network traffic.

### Lab 5.2 — Bastion Host

I launched two EC2 instances:

- `training-bastion` in a public subnet
- `training-private` in a private subnet

The bastion host had a public IP address and allowed SSH access from my IP.

The private instance had no public IP address. Its security group allowed SSH only from the bastion host's security group.

#### SSH Connection

First, I connected to the bastion host from my Mac:

```bash
ssh -A -i ~/.ssh/training-key.pem ec2-user@98.92.142.178
```

Then, from the bastion host, I connected to the private instance:

```bash
ssh ec2-user@10.0.142.67
```

At first, I got a `Permission denied (publickey)` error.

I fixed this by adding my SSH key to the SSH agent on my Mac using `ssh-add`.

After that, I successfully connected to the private instance through the bastion host.

### Lab 5.3 — Network Debugging

I ran the following command on the private instance:

```bash
sudo yum update -y
```

The command completed successfully and showed `Nothing to do` and `Complete!`.

This showed that the instance could access the package repositories even without a public IP address.

### Traffic Path

My Mac connects to the bastion host using its public IP address through SSH.

The bastion host then connects to the private EC2 instance using its private IP address.

This setup allows me to manage the private instance without exposing it directly to the internet.

### VPC Diagram

![VPC Diagram](vpc-diagram.png)
