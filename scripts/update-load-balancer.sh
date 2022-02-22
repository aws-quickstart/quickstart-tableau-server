
#!/bin/bash
#######################################################################
# To call, use the following syntax
# update-load-balancer.sh "my-target-group-arn", "us-west-2", "true" #
#######################################################################

# Initialize variables
TARGET_GROUP=$1;   # ARN of the load balancer's target group
REGION=$2;         # Name of the AWS Region
STOP_INSTANCES=$3; # should be set to "true", if you want to stop the instance

# Find existing instances
IFS=' ' read -ra INSTANCES <<< $(aws elbv2 describe-target-health --target-group-arn $TARGET_GROUP --region $REGION --query "TargetHealthDescriptions[?TargetHealth.State=='healthy'].Target.Id" | tr -dt '[],\"')

# Loop through each instance
for INSTANCE in ${INSTANCES[@]}
do
  # de-register the target
  aws elbv2 deregister-targets --target-group-arn $TARGET_GROUP --region $REGION --targets Id=$INSTANCE
  
  # optionaly stop the instance
  if [ "$STOP_INSTANCES" = "true" ]; then
    aws ec2 stop-instances --region $REGION --instance-ids $INSTANCE;
  fi
done

# Find this instance's id
NEW_INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id)

# Add this new instance to the load balancer
aws elbv2 register-targets --target-group-arn $TARGET_GROUP --region $REGION --targets Id=$NEW_INSTANCE_ID