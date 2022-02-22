#!/bin/bash

# Initialize variables
TODAY=`date '+%Y_%m_%d__%H_%M_%S'`;
BUCKET_NAME=$1;
S3_PREFIX=$2;
TSM_PATH=$(realpath /opt/tableau/tableau_server/packages/customer-bin*);

# Start the log entry
echo ""; echo "Starting backup at $TODAY";

# Cleanup old log files
"$TSM_PATH"/tsm maintenance cleanup;

# Backup tableau repository
"$TSM_PATH"/tsm maintenance backup -f "$TODAY.tsbak";
aws s3 cp /var/opt/tableau/tableau_server/data/tabsvc/files/backups/$TODAY.tsbak s3://$BUCKET_NAME/$S3_PREFIX/$TODAY-backup.tsbak;
rm "/var/opt/tableau/tableau_server/data/tabsvc/files/backups/$TODAY.tsbak";

# Backup site settings
"$TSM_PATH"/tsm settings export -f "/tmp/backup/$TODAY.json";
aws s3 cp "/tmp/backup/$TODAY.json" s3://$BUCKET_NAME/$S3_PREFIX/$TODAY-settings.json;
rm "/tmp/backup/$TODAY.json";