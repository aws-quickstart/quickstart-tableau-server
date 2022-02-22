#!/bin/bash

# Initialize variables
TODAY=`date '+%Y_%m_%d__%H_%M_%S'`;
BUCKET_NAME=$1;
S3_PREFIX=$2;
TSM_PATH=$(realpath /opt/tableau/tableau_server/packages/customer-bin*);

# Start the log entry
echo ""; echo "Starting Restore process at $TODAY";

# Look for the newest backup in S3
LatestConfig=$(aws s3 ls $BUCKET_NAME/$S3_PREFIX --recursive | grep '.*settings.json' | sort | tail -n 1 | awk '{print $4}')
LatestTsbak=$(aws s3 ls $BUCKET_NAME/$S3_PREFIX --recursive | grep '.*tsbak' | sort | tail -n 1 | awk '{print $4}')

# Restore from S3 config file
if [ -z "$LatestConfig" ]
then
    aws s3 cp $LatestConfig "/tmp/config-$TODAY.json";
    "$TSM_PATH"/tsm settings import -f "/tmp/config-$TODAY.json";
    rm "/tmp/config-$TODAY.json"
fi

# Restore from S3 backup file
if [ -z "$LatestTsbak" ]
then
    aws s3 cp $LatestTsbak "/var/opt/tableau/tableau_server/data/tabsvc/files/backups/$TODAY.tsbak";
    "$TSM_PATH"/tsm maintenance restore -f "$TODAY.tsbak";
    rm "/var/opt/tableau/tableau_server/data/tabsvc/files/backups/$TODAY.tsbak";
fi
