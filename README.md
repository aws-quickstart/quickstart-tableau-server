# quickstart-tableau-server

This Quick Start helps you deploy a fully functional Tableau Server environment on the AWS Cloud, following best practices from AWS and Tableau Software.

Tableau Server is an online solution for sharing, distributing, and collaborating on business intelligence content created in Tableau. Tableau Server users can create workbooks and views, dashboards, and data sources in Tableau Desktop, and then publish this content to the server.

![Quick Start Tableau Server Design Architecture](https://d3ulk6ur3a3ha.cloudfront.net/partner-network/QuickStart/datasheets/tableau-server-architecture-on-aws-cluster.png)

The Tableau Server standalone (single-node) deployment installs Tableau Server on an EC2 m4.4xlarge instance running Windows Server 2012 R2 with a 100-GiB EBS volume in the default VPC of the AWS Region specified in the AWS CloudFormation template.

The Tableau Server cluster (multi-node) deployment installs Tableau Server on three EC2 m4.4xlarge instances: a primary server and two worker servers. Each instance runs Windows Server 2012 R2 and is configured with a 100-GiB EBS volume. In addition, if you use the end-to-end (new VPC) deployment option, this stack also creates a bastion host on an EC2 t2.micro instance. Optionally, you can use an SSL certificate with this stack for enhanced security.


Deployment Guide: https://s3.amazonaws.com/quickstart-reference/tableau/server/latest/doc/tableau-server-on-the-aws-cloud.pdf
