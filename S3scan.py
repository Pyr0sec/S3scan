import re
import os
import argparse
import boto3, botocore

print(r"""
   __________
  / ___/__  /______________ _____
  \__ \ /_ </ ___/ ___/ __ `/ __ \
 ___/ /__/ (__  ) /__/ /_/ / / / /
/____/____/____/\___/\__,_/_/ /_/
""")

def keys(prefix='/', delimiter='/'):
    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    return (i.key for i in bucket.objects.filter(Prefix=prefix))

def check_bucket(bucketname):
    print("\nChecking status for bucket: %s" % bucketname)
    if bucketname == "null":
        print("Error: No bucket specified.")
        return False
    try:
        s3.meta.client.head_bucket(Bucket=bucketname)
        print("Bucket Exists! \n\nTry '--enumerate' to get more information about this bucket.")
        return True
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access! \nMaybe try different access credentials using --profile?")
            return False
        elif error_code == 404:
            print("Bucket Does Not Exist!")
            return False

def url_parse(String):
    regex = re.compile(r"https?:\/\/(.*)?\.s3.*\.(\w+)\.com")
    result = regex.search(String)
    return result[1]

def url_parse1(String):
    regex = re.compile(r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)")
    result = regex.search(String)
    return result[1]

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument('-u', '--url', help="Accepts S3 bucket URL as an argument", type=str)
group.add_argument('-b', '--bucket-name', help="Accepts S3 bucket name as an argument", type=str)
parser.add_argument('--profile', help="Used to specify an AWS profile on your system (like awscli), Uses default credentials if not specified any.", type=str)
parser.add_argument('--enumerate', help="Further enumerates the bucket by Checking if upload, download and deletion are allowed and displays all objects on the bucket.", action='store_true', default=False)

args = parser.parse_args()
bucketname = "null"
if args.url and "amazonaws" in args.url:
    bucketname = url_parse(args.url)
elif args.url and "amazonaws" not in args.url:
    bucketname = url_parse1(args.url)
    if ".com" in bucketname:
        bucketname = bucketname.replace(".com", "")
    print("checking if %s bucket exists... \nIf you think %s is not the bucket name then you can specify bucket using -b flag. \nNote: If you are using a non AWS service (like localstack) then please specify the endpoint url using --endpoint-url flag." % (bucketname,bucketname))
elif args.bucket_name:
    bucketname = args.bucket_name
else:
    print("Please enter a bucket name/url \nUse S3scan.py -h for more information.")
    exit()

if args.profile:
    session = boto3.Session(profile_name=args.profile)
    s3 = session.resource('s3')
else:
    s3 = boto3.resource('s3')

bucket = s3.Bucket(bucketname)

bucket_status = check_bucket(bucketname)

if bucket_status == True and args.enumerate == True:
    print("\nChecking permissions...")
    file = os.getcwd().replace("\\","/")+"/gg.txt"
    open(file, 'a').close()
    KEY = 'gg.txt'
    try:
        s3.meta.client.upload_file(file, bucketname, 'gg.txt')
        print("File upload: Allowed")
        file_up = 1
    except:
        print("File upload: Not allowed")
        file_up = 0

    if file_up == 1:
        try:
            bucket.download_file(KEY, 'gg.txt')
            print("File download: Allowed")
        except:
             print("File Download: Not allowed")
    else:
        size_limit = 8388608
        for i in bucket.objects.all():
            response = s3.Object(bucketname, i.key)
            size = response.content_length
            if  size <= size_limit:
                size_limit = size
                obj_name = i.key
        if size_limit == 8388608:
            print("File sizes are greater than 8MB, Please check for download manually")
        
        try:
            bucket.download_file(obj_name, obj_name)
            print("File download: Allowed")
        except:
             print("File Download: Not allowed")

    if file_up == 1:
        try:
            s3.Object(bucketname, 'gg.txt').delete()
            print("File Deletion: Allowed")
        except:
            print("File Deletion: Not allowed")
    else:
        print("File deletion: 'Warning: Please check for deletion manually, Deleting bucket content without permission is unethical.'")

    print("\nListing Objects...")
    for i in keys():
        print(i)

    if os.path.isfile(file):
        os.remove(file)
    if os.path.isfile(obj_name):
        os.remove(obj_name)