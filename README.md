# quickstart-tableau-server
## Tableau Server on the AWS Cloud

This Quick Start helps you deploy a fully functional Tableau Server environment on the AWS Cloud, following best practices from AWS and Tableau Software. 

This updated Quick Start now provides support for Linux, in addition to Microsoft Windows Server.

Tableau Server is an online solution for sharing, distributing, and collaborating on business intelligence content created in Tableau. Tableau Server users can create workbooks and views, dashboards, and data sources in Tableau Desktop, and then publish this content to the server.

![Tableau Server clustered design architecture on AWS](https://d3ulk6ur3a3ha.cloudfront.net/partner-network/QuickStart/datasheets/tableau-server-architecture-on-aws-clustered.png)

The Quick Start supports two standardized architectures and provides automatic deployment options for Tableau Server:
- Standalone architecture. Installs Tableau Server on an Amazon EC2 m5.4xlarge instance running Microsoft Windows Server 2012 R2, CentOS 7 x86_64 HVM, or Ubuntu Server 16.04-LTS-HVM. This architecture is deployed into a new or existing VPC.
- Cluster architecture. Installs Tableau Server on at least three Amazon EC2 m4.4xlarge instances running Microsoft Windows Server 2012 R2, CentOS 7 x86_64 HVM, or Ubuntu Server 16.04-LTS-HVM. This option builds a new AWS environment consisting of the VPC, subnets, NAT gateways, security groups, bastion host (on an Amazon EC2 t3.micro instance), and other infrastructure components, and then deploys Tableau Server into a new or existing VPC. Optionally, you can use an SSL certificate with this stack for enhanced security. 

This Quick Start provides the following deployment options: 
- Deploy Tableau Server (on Windows Server, CentOS, or Ubuntu Server) into a new VPC (standalone architecture) 
- Deploy Tableau Server (on Windows Server, CentOS, or Ubuntu Server) into an existing VPC (standalone architecture) 
- Deploy Tableau Server on Windows Server into a new VPC (cluster architecture) 
- Deploy Tableau Server on Windows Server into an existing VPC (cluster architecture) 
- Deploy Tableau Server on CentOS or Ubuntu Server into a new VPC (cluster architecture) 
- Deploy Tableau Server on CentOS or Ubuntu Server into an existing VPC (cluster architecture)

For architectural details, best practices, step-by-step instructions, and customization options, see the 
[deployment guide](https://fwd.aws/3yAWN).

## Deploy with Control Tower
You can deploy Tableau Server in a customized AWS Control Tower environment to help you set up a secure, multi-account AWS environment using AWS best practices. For details, see [Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/). 

The root directory of the Tableau Server Quick Start repo includes a `ct` folder with a `manifest.yaml` file to assist you with the AWS Control Tower deployment. This file has been customized for the Tableau Server Quick Start. 

In the following sections, you will review and update the settings in this file and then upload it to the S3 bucket that is used for the deployment.

### Review the manifest.yaml file

1. Navigate to the root directory of the Tableau Server Quick Start, and open the `manifest.yaml` file, located in the `ct` folder.
2. Confirm that the `region` attribute references the Region where AWS Control Tower is deployed. The default Region is us-east-1. You will update the `regions` attribute (located in the *resources* section) in a later step. 
3. Confirm that the `resource_file` attribute points to the public S3 bucket for the Tableau Server Quick Start. Using a public S3 bucket ensures a consistent code base across the different deployment options. 

If you prefer to deploy from your own S3 bucket, update the path as needed.

4. Review each of the `parameters` attributes and update them as needed to match the requirements of your deployment. 
5. Confirm that the `deployment_targets` attribute is configured for either your target accounts or organizational units (OUs). 
6. For the `regions` attribute, add the Region where you plan to deploy the Tableau Server Quick Start. The default Region is us-east-1.

### Upload the manifest.yaml file
1. Compress the `manifest.yaml` file and name it `custom-control-tower-configuration.zip`.
2. Upload the `custom-control-tower-configuration.zip` file to the S3 bucket that was created for the AWS Control Tower deployment (`custom-control-tower-configuration-<accountnumber>-<region>`).

The file upload initiates the customized pipeline that deploys the Quick Start to your target accounts.


To post feedback, submit feature ideas, or report bugs, use the **Issues** section of this GitHub repo.
If you'd like to submit code for this Quick Start, please review the [AWS Quick Start Contributor's Kit](https://aws-quickstart.github.io/).

