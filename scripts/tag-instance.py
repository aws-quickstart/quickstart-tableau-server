from ast import arg
from importlib.resources import Resource
import boto3
from botocore.exceptions import ClientError
import argparse, requests, logging, json, sys
from datetime import datetime

#########################
#   Utility Functions   #
#########################

#   Setup the logging
def setup_logging(log_file_path, additional_modules):
    
    #   Define how to handle logging within this script
    logging.basicConfig(
        format='%(message)s', 
        level=logging.INFO,
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    #   Override the defaults logging settings from modules like boto and docker
    for module in additional_modules:
        logging.getLogger(module).setLevel(logging.CRITICAL)

#   Define a generic logging function
def log(message, details_json=None, level=None):

    #   Determine which script is being run
    source = sys.argv[0] 
    
    #   Build the log message as JSON
    log_message = {
        "message": message,
        "source" : source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    #   Safely parse any JSON object included with the log request
    if details_json is not None:
        if level == "error":
            try:
                test = json.dumps(details_json.response.get("Error"), sort_keys=False)
                details_body = details_json.response.get("Error")
            except:
                details_body = "Could not parse error's response"
        else:
            try:
                test = json.dumps(details_json, sort_keys=False)
                details_body = details_json
            except:
                details_body = "Could not parse details JSON object"
        log_message["details"] = details_body

    #   Log at the specified level
    if level == "warning":
        logging.warning(json.dumps(log_message, sort_keys=False))
    elif level == "critical":
        logging.critical(json.dumps(log_message, sort_keys=False))
    elif level == "error":
        logging.error(json.dumps(log_message, sort_keys=False))
    else:
        logging.info(json.dumps(log_message, sort_keys=False))

    return None


#########################
#   Business Logic      #
#########################

#   Get this EC2 instance's ID
def get_this_instance_id():

    #   Get the ID for this EC2 instance
    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    id = response.text
    
    log(message=f"This instance has an ID of {id}")
    return id

#   Derive the root volume's id from an ec2 instance
def get_instance_volumes(instance_id, region):

    #   Get an EC2 client
    ec2_client = boto3.client('ec2', region_name=region)

    #   Get all volumes associated with this instance
    volumes = ec2_client.describe_instance_attribute(InstanceId=instance_id, Attribute='blockDeviceMapping')

    #   Parse out just the IDs for each volume
    volume_ids = []
    for volume in volumes['BlockDeviceMappings']:
        if volume['Ebs']:
            volume_ids.append(volume['Ebs']['VolumeId'])
    
    #   Return a list of volume IDs
    return volume_ids

#   Apply a tag for a given EC2 instance
def apply_tag(id, tag_name, tag_value, region):

    #   Get an E2 client
    ec2_client = boto3.client('ec2', region_name=region)

    #   Create a tag
    status = ec2_client.create_tags(Resources=[id], Tags=[ { 'Key': tag_name, 'Value': tag_value } ])

    log(message=f"Applying the following tag to {id} - {tag_name}:{tag_value}")


#########################
#   Main Executable     #
#########################
def main():

     #   Setup logging
    setup_logging(log_file_path="tableau-tag-instance.log",additional_modules=["boto3","botocore"])

    #   Parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--tagname", help="What is the name of the tag?", type=str, required=True)
    parser.add_argument("--tagvalue", help="What is the value of the tag?", type=str, required=True)
    parser.add_argument("--region", help="AWS Region the Ec2 instance lives in", type=str, required=True)
    args = parser.parse_args()
    tag_name = args.tagname
    tag_value = args.tagvalue
    region = args.region

    #   Get Instance ID
    instance_id = get_this_instance_id()
    instance_volumes_ids = get_instance_volumes(instance_id=instance_id, region=region)

    #   Apply a Name tag
    status = apply_tag(id=instance_id, tag_name=tag_name, tag_value=tag_value, region=region)
    for volume_id in instance_volumes_ids:
        apply_tag(id=volume_id, tag_name=tag_name, tag_value=tag_value, region=region)

main()