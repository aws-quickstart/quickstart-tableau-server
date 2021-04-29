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

## Deploying with Control Tower
This QuickStart can be deployed in a Control Tower environment. To accomplish this, we make use of [Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/?did=sl_card&trk=sl_card) solution. A folder labeled "ct" has been provided in the repository for this Quick Start to aid in the deployment.

After the [Customization for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/?did=sl_card&trk=sl_card) solution has been deployed, use the contents of the "ct" folder (located in the root of the GitHub repositoy) to customize your deployment.
```
└── ct
   ├── custom-control-tower-configuration
   │   └── manifest.yaml
   └── custom-control-tower-configuration.zip
```
The manifest.yaml file has been customized for this Quick Start. 

### Review the manifest file.

Open and review the *manifest.yaml* file

**region:** Ensure the _region_ attribute references the region where the Customization for AWS Control Tower has been deployed. (The default region is "us-east-1")

NOTE: There is a second _region_ attribute located under the _resources_ section, that attribute is used to define the region where the Quick Start will be deployed. 

#### Review the _resources_ section
**resource_file:** The _resource_file_ attribute points to the public S3 bucket for this Quick Start, if you are deploying from your own s3 bucket, update this reference appropriately.

NOTE: There are other methods for deploying this QuickStart using Customization for AWS Control Tower, we have chosen to make use of the public s3 repository to ensure a consistent code base across the different deployment options. Visit the [Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/?did=sl_card&trk=sl_card) solution page for additional information.

**parameters:** Update The _parameters_ attribute to suit your deployment. 

NOTE: Carefuly review and update these attributes, to ensure the deployment is successful.

**deployment_targets:** Ensure your _deployment_targets_ is configured for either your target account(s) or target OU(s)

**region:** Enter the _region_ where you wish to deploy the Quick Start. (The default region is "us-east-1")

### Upload the manifest file
Compress the "manifest.yaml" file and name it *custom-control-tower-configuration.zip*
Upload the *custom-control-tower-configuration.zip* to the s3 bucket that was created by the Customization for AWS Control Tower solution. (custom-control-tower-configuration-_accountnumber_-_region_)
The file upload will trigger the customized pipeline that will deploy the Quick Start to your target accounts.

Visit the [Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/?did=sl_card&trk=sl_card) solution page for additional information.


To post feedback, submit feature ideas, or report bugs, use the **Issues** section of this GitHub repo.
If you'd like to submit code for this Quick Start, please review the [AWS Quick Start Contributor's Kit](https://aws-quickstart.github.io/).

