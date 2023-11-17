import re
import os
import argparse
import boto3, botocore

print(r"""
 +-+-+-+-+-+-+
 |s|3|s|c|a|n|
 +-+-+-+-+-+-+
""")

def keys(bucket, prefix='/', delimiter='/'):
    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    return (i.key for i in bucket.objects.filter(Prefix=prefix))

def check_bucket(bucketname):
    if bucketname == "null":
        return False
    try:
        s3.meta.client.head_bucket(Bucket=bucketname)
        return True
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        return error_code

def check_permissions(bucketname, bucket):
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
            if os.path.isfile(obj_name):
                os.remove(obj_name)
        except:
            print("File Download: Not allowed")

    if file_up == 1:
        try:
            s3.Object(bucketname, 'gg.txt').delete()
            print("File Deletion: Allowed")
        except:
            print("File Deletion: Not allowed")
    else:
        print("File deletion: Warning! Please check for deletion manually, Deleting bucket content without permission is unethical.")

    print("\nListing Objects...")
    for i in keys(bucket):
        print(i)

    if os.path.isfile(file):
        os.remove(file)

def print_message(bucketname, bucket_status, enumerate_argument, file_argument, bucket):
    if bucket_status == True and enumerate_argument == True and file_argument:
        print('\33[92m'+f"{bucketname}: Bucket Exists!"+'\33[0m')
        print("\nChecking permissions...")
        check_permissions(bucketname, bucket)
        print('\33[94m' + f"----------------------------------------------" + '\33[0m')
    elif bucket_status == True and enumerate_argument == True:
        print('\33[92m'+f"{bucketname}: Bucket Exists!"+'\33[0m')
        print("\nChecking permissions...")
        check_permissions(bucketname, bucket)
        print('\33[94m' + f"----------------------------------------------" + '\33[0m')
    elif bucket_status == True and file_argument:
        print('\33[92m'+f"{bucketname}: Bucket Exists!"+'\33[0m')
    elif bucket_status == True:
        print('\33[92m'+f"{bucketname}: Bucket Exists!"+'\33[0m')
        print("\nTry '--enumerate' to get more information about this bucket.")
    elif bucket_status == 403 and file_argument and enumerate_argument:
        print('\33[91m'+f"{bucketname}: Private Bucket. Forbidden Access!"+'\33[0m')
        print('\33[94m' + f"----------------------------------------------" + '\33[0m')
    elif bucket_status == 403 and file_argument:
        print('\33[91m'+f"{bucketname}: Private Bucket. Forbidden Access!"+'\33[0m')
    elif bucket_status == 403:
        print('\33[91m'+f"{bucketname}: Private Bucket. Forbidden Access!"+'\33[0m')
        print("Maybe try different access credentials using --profile?")
    elif bucket_status == 404 and file_argument and enumerate_argument:
        print('\33[91m'+f"{bucketname}: Bucket Does Not Exist!"+'\33[0m')
        print('\33[94m' + f"----------------------------------------------" + '\33[0m')
    elif bucket_status == 404:
        print('\33[91m'+f"{bucketname}: Bucket Does Not Exist!"+'\33[0m')
    elif bucket_status == False and file_argument and enumerate_argument:
        print('\33[91m'+f"Error: No bucket specified."+'\33[0m')
        print('\33[94m' + f"----------------------------------------------" + '\33[0m')
    elif bucket_status == False:
        print('\33[91m'+f"Error: No bucket specified."+'\33[0m')
    else:
        if file_argument and enumerate_argument:
            print('\33[91m' + f"{bucketname}: Error code {bucket_status}" + '\33[0m')
            print('\33[94m' + f"----------------------------------------------" + '\33[0m')
        else:
            print('\33[91m' + f"{bucketname}: Error code {bucket_status}" + '\33[0m')

def url_parse(String):
    regex = re.compile(r"https?:\/\/(.*)?\.s3.*\.(\w+)\.com")
    result = regex.search(String)
    return result[1]

def url_parse1(String):
    regex = re.compile(r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)")
    result = regex.search(String)
    return result[1]

def fileparser(filename, enumerate_argument):
    with open(filename) as f:
        buckets = f.readlines()
    buckets = [x.strip() for x in buckets]
    
    for i in buckets:
        bucket = s3.Bucket(i)
        bucket_status = check_bucket(i)
        print_message(i, bucket_status, enumerate_argument, filename, bucket)
    exit()


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument('-u', '--url', help="Accepts S3 bucket URL as an argument", type=str)
group.add_argument('-b', '--bucket-name', help="Accepts S3 bucket name as an argument", type=str)
group.add_argument('-f', '--file', help="Accepts a file containing S3 bucket names as an argument", type=str)
parser.add_argument('--profile', help="Used to specify an AWS profile on your system (like awscli), Uses default credentials if not specified any.", type=str)
parser.add_argument('--enumerate', help="Further enumerates the bucket by Checking if upload, download and deletion are allowed and displays all objects on the bucket.", action='store_true', default=False)
args = parser.parse_args()

bucketname = "null"

if args.profile:
    session = boto3.Session(profile_name=args.profile)
    s3 = session.resource('s3')
else:
    s3 = boto3.resource('s3')

if args.url and "amazonaws" in args.url:
    bucketname = url_parse(args.url)
elif args.url and "amazonaws" not in args.url:
    bucketname = url_parse1(args.url)
    if ".com" in bucketname:
        bucketname = bucketname.replace(".com", "")
    print("checking if %s bucket exists... \nIf you think %s is not the bucket name then you can specify bucket using -b flag." % (bucketname,bucketname))
elif args.bucket_name:
    bucketname = args.bucket_name
elif args.file:
    if os.path.exists(args.file):
        fileparser(args.file, args.enumerate)
        # exit()
    else:
        print("Error: Specified file does not exist")
        exit()
else:
    print("Please enter a bucket name/url or a file containing bucket names... \nUse -h for more information.")
    exit()

bucket = s3.Bucket(bucketname)

print("\nChecking status for bucket: %s" % bucketname)
bucket_status = check_bucket(bucketname)

print_message(bucketname, bucket_status, args.enumerate, args.file, bucket)
