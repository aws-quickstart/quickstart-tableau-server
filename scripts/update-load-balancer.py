from ast import arg
import boto3
from botocore.exceptions import ClientError
import argparse, requests, os, logging, json, sys
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

#   Is this code running on windows?
def is_windows():
    return os.name == "nt"

#   Define where the tmp directory is
def get_tmp_path():
    if is_windows():
        return "C:\\tabsetup\\"
    else:
        return "/tmp/"

#########################
#   Business Logic      #
#########################

#   Get this EC2 instance's ID
def get_this_instance_id():

    response = requests.get('http://169.254.169.254/latest/meta-data/instance-id')
    id = response.text

    log(message=f"This instance has an ID of {id}")
    return id

#   Backup Tableau Server, and save to S3
def get_loadbalancer_targets(target_group_arn, region):

    #   Get an ELBv2 client
    elb_client = boto3.client('elbv2', region_name=region)

    #   Query for the target instances of the target group
    targets = elb_client.describe_target_health(TargetGroupArn=target_group_arn)

    #   Get just the instance Ids as an array
    ids = []
    for target in targets['TargetHealthDescriptions']:
        if target['TargetHealth']['Status'] != "draining":
            ids.append(target['Target']['Id'])

    log(message=f"Found {len(ids)} instances registered to the target group ${target_group_arn}")
    return ids

def register_target(instance_id, target_group_arn, region):

    #   Get an ELBv2 client
    elb_client = boto3.client('elbv2', region_name=region)

    #   Define the instance as JSON object
    targets = {
        "Id": instance_id
    }

    #   Register the instance to the target group
    log(message=f"Registering {instance_id} to the target group ${target_group_arn}")
    try:
        elb_client.register_targets(TargetGroupArn=target_group_arn,Targets=[targets])
    except ClientError as e:
        log(message=f"Error while adding {instance_id} to the target group", level="error", details_json=e)
        return False
    return True

def deregister_target(instance_id, target_group_arn, region):

    #   Get an ELBv2 client
    elb_client = boto3.client('elbv2', region_name=region)

    #   Define the instance as JSON object
    targets = {
        "Id": instance_id
    }

    #   Register the instance to the target group
    log(message=f"Deregistering {instance_id} from the target group ${target_group_arn}")
    try:
        elb_client.deregister_targets(TargetGroupArn=target_group_arn,Targets=[targets])
    except ClientError as e:
        log(message=f"Error while removing {instance_id} from the target group", level="error", details_json=e)
        return False
    return True

def stop_instance(instance_id, region):

    #   Get an EC2 client
    ec2_client = boto3.client('ec2', region_name=region)

    log(message=f"Stop instance {instance_id}")
    try: 
        ec2_client.stop_instances( InstanceIds=[ instance_id ])
    except ClientError as e:
        log(message=f"Error while stopping {instance_id} ", level="error", details_json=e)
        return False
    return True

#########################
#   Main Executable     #
#########################
def main():

    #   Setup logging
    setup_logging(log_file_path="tableau-update-load-balancer.log",additional_modules=["boto3","botocore"])

    #   Parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_group_arn", help="The ARN of your load balancer's target group", type=str, required=True)
    parser.add_argument("--region", help="The AWS region", type=str, required=True)
    parser.add_argument("--stop_instances", help="Should we stop any other instances that are attached to the load balancer?", type=str, required=True)
    args = parser.parse_args()
    target_group_arn = args.target_group_arn  
    region=args.region
    stop_instances=args.stop_instances.lower() == 'true'

    #   Check for any existing targets
    existing_targets = get_loadbalancer_targets(target_group_arn=target_group_arn, region=region)

    #   Register our instance to the target group
    this_instance_id = get_this_instance_id()
    register_target(instance_id=this_instance_id, target_group_arn=target_group_arn, region=region)

    #   De-register any old instances from the target group
    for old_target in existing_targets:

        #   De-register
        deregister_target(instance_id=old_target, target_group_arn=target_group_arn, region=region)

        #   If specified, stop the old instances
        if stop_instances:
            stop_instance(instance_id=old_target, region=region)

main()