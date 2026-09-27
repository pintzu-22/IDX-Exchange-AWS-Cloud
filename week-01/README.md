# Week 1 - Cloud Fundamentals & Account Setup

The root user has full control over the AWS account, so I should not use it for everyday tasks.
I enabled MFA on the root account to make it more secure.
For regular work, I created an IAM admin user instead.
IAM lets me manage who can access AWS and what actions they are allowed to perform.
AWS uses a Shared Responsibility Model, which means security is shared between AWS and the customer.
AWS is responsible for protecting the physical data centers, hardware, and cloud infrastructure.
I am responsible for things like my passwords, MFA, IAM permissions, and the security of the resources I create.