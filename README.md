# quickstart-tableau-server
## Tableau Server on the AWS Cloud

This Quick Start helps you deploy a fully functional Tableau Server environment on the AWS Cloud, following best practices from AWS and Tableau Software. 

This updated Quick Start now provides support for Linux, in addition to Microsoft Windows Server.

Tableau Server is an online solution for sharing, distributing, and collaborating on business intelligence content created in Tableau. Tableau Server users can create workbooks and views, dashboards, and data sources in Tableau Desktop, and then publish this content to the server.

![Tableau Server clustered design architecture on AWS](https://d3ulk6ur3a3ha.cloudfront.net/partner-network/QuickStart/datasheets/tableau-server-architecture-on-aws-clustered.png)

The Quick Start supports two standardized architectures and provides automatic deployment options for Tableau Server:
- Standalone architecture. Installs Tableau Server on an Amazon EC2 m5.4xlarge instance running Microsoft Windows Server 2012 R2, CentOS 7 x86_64 HVM, or Ubuntu Server 16.04-LTS-HVM. This architecture is deployed into a new or existing VPC.
- Cluster architecture. Installs Tableau Server on at least three Amazon EC2 m4.4xlarge instances running Microsoft Windows Server 2012 R2, CentOS 7 x86_64 HVM, or Ubuntu Server 16.04-LTS-HVM. This option builds a new AWS environment consisting of the VPC, subnets, NAT gateways, security groups, bastion host (on an Amazon EC2 t2.micro instance), and other infrastructure components, and then deploys Tableau Server into a new or existing VPC. Optionally, you can use an SSL certificate with this stack for enhanced security. 

This Quick Start provides the following deployment options: 
- Deploy Tableau Server (on Windows Server, CentOS, or Ubuntu Server) into a new VPC (standalone architecture) 
- Deploy Tableau Server (on Windows Server, CentOS, or Ubuntu Server) into an existing VPC (standalone architecture) 
- Deploy Tableau Server on Windows Server into a new VPC (cluster architecture) 
- Deploy Tableau Server on Windows Server into an existing VPC (cluster architecture) 
- Deploy Tableau Server on CentOS or Ubuntu Server into a new VPC (cluster architecture) 
- Deploy Tableau Server on CentOS or Ubuntu Server into an existing VPC (cluster architecture)

For architectural details, best practices, step-by-step instructions, and customization options, see the 
[deployment guide](https://fwd.aws/3yAWN).

To post feedback, submit feature ideas, or report bugs, use the **Issues** section of this GitHub repo.
If you'd like to submit code for this Quick Start, please review the [AWS Quick Start Contributor's Kit](https://aws-quickstart.github.io/).

