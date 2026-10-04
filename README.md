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
