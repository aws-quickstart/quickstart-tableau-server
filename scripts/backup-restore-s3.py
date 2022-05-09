from ast import arg
import boto3
from botocore.exceptions import ClientError
import argparse, os, glob, logging, json, sys
from subprocess import check_output
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

#   Get TSM's full path
def get_tsm_path():
    
    #   Define the glob expression, based on the OS
    glob_exp = ""
    if is_windows():
        glob_exp = "C:\\tableau\\packages\\[b][i][n][.]*\\[t][s][m][.]*"
    else: 
        glob_exp = "/opt/tableau/tableau_server/packages/[b][i][n][.]*/[t][s][m]*"
    
    #   Evaluate the path
    path = glob.glob(glob_exp)

    #   Return a safe result path
    return path[0]

#   Execute a tsm command
def exec_tsm(*args):

    # #   Create a subprocess, and execute the given command
    log(level="Info", message=f"Running the following tsm command: {' '.join(args)}")
    tsm_output = check_output(args).decode('UTF-8')
    
    # #   Log, then return the output of the TSM command
    log(message=tsm_output, level="Info")
    return tsm_output

    #print(" ".join(args))
    #return ""

#   Get the path for the backups, based on the OS
def backup_full_path(tsm):

    #   Get the path to backup files from TSM
    path = exec_tsm(tsm, "configuration", "get", "-k", "basefilepath.backuprestore")

    #   Clean up the response text
    clean_path = path.replace("\r","").replace("\n","")

    #if is_windows():
    #    return os.path.join("C:\\ProgramData", "Tableau", "Tableau Server", "data", "tabsvc", "files", "backups",filename)
    #else:
    #    return os.path.join("/var","opt","tableau","tableau_server","data","tabsvc","files","backups",filename)

    return clean_path

#########################
#   Business Logic      #
#########################

#   Backup Tableau Server, and save to S3
def backup(tsm, bucket_name, s3_prefix):

    #   Generate a filename for the tsbak
    today = datetime.now().strftime('%Y-%m-%d')

    #   cleanup the server first
    exec_tsm(tsm, "maintenance", "cleanup", "--all")

    #   export the tsm settings
    settings_filename = f"{today}-settings.json"
    settings_fullpath = os.path.join(get_tmp_path(),settings_filename)
    exec_tsm(tsm, "settings", "export", "--output-config-file", settings_fullpath)

    #   perform the backup
    tsbak_filename = f"{today}-backup.tsbak"
    exec_tsm(tsm, "maintenance", "backup", "--file",tsbak_filename , "--ignore-prompt")

    #   Get the full path to the backup file
    tsbak_fullpath = os.path.join(backup_full_path(tsm=tsm),tsbak_filename)

    #   Upload the backup files to S3 bucket
    s3_client = boto3.client('s3')
    try:
        key = f"{s3_prefix}{settings_filename}"
        response_settings = s3_client.upload_file(settings_fullpath, bucket_name, key)
        key =  f"{s3_prefix}{tsbak_filename}"
        response_tsbak = s3_client.upload_file(tsbak_fullpath, bucket_name,key)
    except ClientError as e:
        log(message=f"Error uploading ${key} to {bucket_name}", details_json=e, level="error")
        return False

    #   Cleanup backup files locally
    os.remove(settings_fullpath)
    os.remove(tsbak_fullpath)

    return True

#   Restore Tableau Server, from a backup in S3
def restore(tsm, bucket_name, s3_prefix):

    #   Upload the backup files to S3 bucket
    s3_client = boto3.client('s3')
    try:
        #   Look for existing backup files
        list = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
        tsbaks = []
        settings = []

        #   Loop through all files, and sort out tsbaks and setting.jsons
        for file in list.get("Contents",[]):
            if file.get("Key","").endswith('tsbak'):
                tsbaks.append(file)
            if file.get("Key","").endswith('settings.json'):
                settings.append(file)

        #   Sort both lists based on last updated date
        def sort_key(obj):
            return obj.get("LastModified")
        tsbaks.sort(key=sort_key)
        settings.sort(key=sort_key)

        #   Get an S3 resource reference
        s3_resource = boto3.resource('s3')

        #   Download/Restore from tsbak
        if len(tsbaks)>0:
            #   Get the local and remote paths
            local_backup_path = os.path.join(backup_full_path(tsm=tsm), "backup.tsbak")
            s3_backup_path = tsbaks[0]['Key']
            #   Download the file
            s3_resource.Bucket(bucket_name).download_file(s3_backup_path, local_backup_path)
            #   Restore from the backup
            exec_tsm(tsm, "maintenance", "restore", "--file", "backup.tsbak")
            #   Cleanup file
            os.remove(local_backup_path)
        
        #   Download/Restore from settings.json
        if len(settings)>0:
            #   Get the local and remote paths
            local_backup_path = os.path.join(get_tmp_path(), "settings.json")
            s3_backup_path = settings[0]['Key']
            #   Download the file
            s3_resource.Bucket(bucket_name).download_file(s3_backup_path, local_backup_path)
            #   Restore from the backup
            exec_tsm(tsm, "settings", "import", "--config-only", "--force-keys", "-f", local_backup_path)
            exec_tsm(tsm, "pending-changes", "apply", "--ignore-prompt")
            #   Cleanup file
            os.remove(local_backup_path)

        #   Ensure Tableau Server has started
        exec_tsm(tsm, "start")

    except ClientError as e:
        log(message=f"Error restoring backups from {bucket_name}", details_json=e, level="error")
        return False
    return True

#########################
#   Main Executable     #
#########################
def main():

     #   Setup logging
    setup_logging(log_file_path="tableau-backup-restore-s3.log",additional_modules=["boto3","botocore"])

    #   Parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", help="Options are 'backup' or 'restore'", type=str, required=True)
    parser.add_argument("--region", help="The AWS region", type=str, required=True)
    parser.add_argument("--s3bucket", help="The S3 bucket, where the backup files live", type=str,required=True)
    parser.add_argument("--s3prefix", help="The prefix used to query for backup files in S3", type=str,required=True)
    args = parser.parse_args()
    command = args.command.lower()
    region=args.region
    s3_bucket=args.s3bucket.lower()
    s3_prefix=args.s3prefix.lower()

    #   Get a reference to tsm
    tsm = get_tsm_path()

    #   Execute the command
    if command == 'backup':

        #   Take a backup using TSM and upload to S3
        status = backup(tsm=tsm, bucket_name=s3_bucket, s3_prefix=s3_prefix)

    elif command == 'restore':

        #   Find the latest backup in S3 and use TSM to restore from it
        status = restore(tsm=tsm, bucket_name=s3_bucket, s3_prefix=s3_prefix)

main()