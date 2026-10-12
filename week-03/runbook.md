# Week 03 — EC2 Deployment and EBS Snapshot

---

This week focused on deploying the PropertyLite Flask API to an Amazon EC2 instance and learning how EC2 networking and EBS storage work.

The main goal was to use the PropertyLite from Week 0 and deploy it to an AWS EC2 instance using a bootstrap script.

## Lab 3.1 — Deploy PropertyLite to EC2 with a Bootstrap Script

---

### 1. Launch the EC2 Instance

I opened the AWS Console and went to:

`EC2 → Instances → Launch instance`

I created a new EC2 instance with the following settings:

- Name: `property-api-01`
- AMI: `Amazon Linux 2023`
- Instance type: `t3.micro`
- Key pair: `training-key`

The private key file was stored locally at:

`~/.ssh/training-key.pem`

### 2. Configure the Security Group

Under Network settings, I created a new Security Group.
I added the following inbound rules:
- SSH: Port: 22, Source: My IP
- Custom TCP: Port: 8080, Source: Anywhere-IPv4

Port 22 allows SSH access to the EC2 instance.
Port 8080 allows external access to the PropertyLite Flask API.

### 3. Add the User Data Bootstrap Script

Under:

`Advanced details → User data`

I added a bootstrap script that included the PropertyLite files from Week 0.

Instead of manually copying the application files to the EC2 instance after launch, I embedded the Week 0 `app.py` code and sample CSV data directly into the User Data script.

When the instance started, the script automatically:

- Updated the system packages
- Installed Python and pip
- Installed Flask
- Created the `/opt/property-api` directory
- Created `app.py` using the PropertyLite code from Week 0
- Created the sample property CSV file
- Started the Flask application on port `8080`

This made the EC2 instance self-contained at launch, so I did not need to manually upload the PropertyLite files after connecting to the server.

### 4. Launch the Instance

After completing the configuration, I launched the EC2 instance.
I waited until the instance state showed: `Running`

Then I copied the instance's Public IPv4 address.

### 5. Connect to EC2 and Verify PropertyLite From My Laptop

Before connecting to the EC2 instance, I restricted the permissions of the private key:
`chmod 400 ~/.ssh/training-key.pem`

Then I connected to the EC2 instance using SSH:
`ssh -i ~/.ssh/training-key.pem ec2-user@52.90.224.100`

After the SSH connection succeeded, I confirmed that the PropertyLite application was running correctly.
From my local Mac terminal, I tested the application using the EC2 public IP:
`curl http://52.90.224.100:8080/health`

The response was:
`{"status":"ok"}`

I also tested:
`curl http://52.90.224.100:8080/properties/R100234`

This returned the Sacramento property listing.
These tests confirmed that the PropertyLite Flask API was successfully running on the EC2 instance and could be accessed from my laptop over the internet.

## Lab 3.2 — EBS Snapshot Practice

---

I created a snapshot of the root EBS volume attached to `property-api-01`.

The snapshot is a backup copy of the EBS volume at the time I created it.

After creating the snapshot, I went to `EC2 → Snapshots` and waited until its status changed to `completed`.

If I created a new EBS volume from this snapshot, the new volume would contain the data from the original volume at the time the snapshot was created.

## Debug Lab 3.3 — SSH Connection Timeout

---

My SSH connection initially timed out because the `My IP` rule in the Security Group did not match my current public IP.

I tested the connection by temporarily allowing SSH from `Anywhere-IPv4`, which confirmed that the Security Group source was the issue.

I then updated the SSH rule to my current IP and changed it back to `My IP`.

(The `My IP` value does not automatically update when my public IP changes.)

## Cleanup

---

After completing the labs and saving the required screenshots, I terminated the `property-api-01` EC2 instance.

I went to:

`EC2 → Instances → property-api-01 → Instance state → Terminate`

After the instance was terminated, I checked:

`EC2 → Volumes`

to confirm that the root EBS volume was deleted as well.

This cleanup step helps avoid leaving unused AWS resources running.