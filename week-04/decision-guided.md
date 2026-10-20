# Week 04 — AWS Storage & Database Decision Guide

## AWS Storage & Database Comparison

| AWS Service | What is it? | Use this when... |
|---|---|---|
| **Amazon S3** | A place to store files like images, CSV files, and backups. | Use this when I need to upload and store files without managing a server. |
| **Amazon EBS** | A virtual hard drive for EC2 instances. | Use this when I need storage for an EC2 instance, like its operating system or application files. |
| **Amazon EFS** | A shared file system that multiple servers can use. | Use this when I have multiple EC2 instances that need to access the same files. |
| **Amazon RDS** | A managed SQL database that supports MySQL, PostgreSQL, and other database engines. | Use this when I need to store structured data and run SQL queries, such as JOIN or GROUP BY. |
| **Amazon DynamoDB** | A managed NoSQL database that stores data as items with attributes. | Use this when I need to quickly find and update data using a key, without managing a database server. |
