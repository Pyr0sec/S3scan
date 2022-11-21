```
   __________
  / ___/__  /______________ _____
  \__ \ /_ </ ___/ ___/ __ `/ __ \
 ___/ /__/ (__  ) /__/ /_/ / / / /
/____/____/____/\___/\__,_/_/ /_/
```
S3scan is a tool that scans S3 buckets for permissions, object listing. Also checks if a bucket exists or not.


Requirements
---
```
- Python 3.x
- awscli (credentials must be configured)
```


Installation
---
```
git clone https://github.com/Pyr0sec/S3scan
cd S3scan
pip install -r requirements.txt
```


Usage
---
```shell
(venv) C:\Users\puruj\Documents\git\s3scan>python S3scan.py -h                                              

   __________
  / ___/__  /______________ _____
  \__ \ /_ </ ___/ ___/ __ `/ __ \
 ___/ /__/ (__  ) /__/ /_/ / / / /
/____/____/____/\___/\__,_/_/ /_/

usage: S3scan.py [-h] [-u URL | -b BUCKET_NAME] [--profile PROFILE] [--enumerate]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Accepts S3 bucket URL as an argument
  -b BUCKET_NAME, --bucket-name BUCKET_NAME
                        Accepts S3 bucket name as an argument
  --profile PROFILE     Used to specify an AWS profile on your system (like awscli), Uses default credentials if not specified any.
  --enumerate           Further enumerates the bucket by Checking if upload, download and deletion are allowed and displays all objects on the bucket.      
```


Examples
---
```bash
python S3scan.py -b flaws.cloud --profile root --enumerate
```


Screenshots
---
![image](https://user-images.githubusercontent.com/74669749/202524888-acee8716-31f6-48b8-b10b-97a69a86736d.png)
![image](https://user-images.githubusercontent.com/74669749/202555416-e1a93997-3d70-4c28-b616-fc3658f882af.png)

