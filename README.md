```
                                              +-+-+-+-+-+-+
                                              |s|3|s|c|a|n|
                                              +-+-+-+-+-+-+
```
S3scan is a tool that scans S3 buckets for permissions, object listing. Also checks if a bucket exists or not.


Version 0.1.1 changes
---
- New feature: Supports file input containing multiple buckets now (-f, --file)
- Bug fixes: fixed a few errors in the obj deletion from device part
- Improvements: Added colored output messages for clear distinguishing (no extra module required)
- Extra changes: changed the banner art to more minimal


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
(venv) PS C:\Users\puruj\Documents\git\s3scan> python.exe s3scan.py -h

 +-+-+-+-+-+-+
 |s|3|s|c|a|n|
 +-+-+-+-+-+-+

usage: s3scan.py [-h] [-u URL | -b BUCKET_NAME | -f FILE] [--profile PROFILE] [--enumerate]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Accepts S3 bucket URL as an argument
  -b BUCKET_NAME, --bucket-name BUCKET_NAME
                        Accepts S3 bucket name as an argument
  -f FILE, --file FILE  Accepts a file containing S3 bucket names as an argument
  --profile PROFILE     Used to specify an AWS profile on your system (like awscli), Uses default
                        credentials if not specified any.
  --enumerate           Further enumerates the bucket by Checking if upload, download and deletion are        
                        allowed and displays all objects on the bucket.    
```


Examples
---
```bash
python S3scan.py -b flaws.cloud --profile root --enumerate
python S3scan.py -f buckets.txt --enumerate
```


Todo
---
- [x] Add file input for scanning multiple buckets
- [ ] Add multhreading
- [ ] Add save output to file functionality


Screenshots
---
![image](https://github.com/Pyr0sec/S3scan/assets/74669749/b350ebb8-1614-456a-ad44-2c4920f9db23)
![image](https://github.com/Pyr0sec/S3scan/assets/74669749/071e8e1f-b55d-4d51-88f4-236afbac8928)
![image](https://github.com/Pyr0sec/S3scan/assets/74669749/a8885005-dc8a-4edb-9262-e4948ebea562)


[!["Support a caffeine addict"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/Pyrosec)
