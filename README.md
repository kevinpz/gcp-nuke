# gcp-nuke
> Nuke your entire GCP project with a Python script.

❌ **DO NOT USE THIS SCRIPT IN A PRODUCTION ACCOUNT. IT WILL DESTROY EVERYTHING. USE IT AT YOUR OWN RISK.**

## Supported services
Right now, the following services are supported:
* Cloud Storage

## Script usage

### Requirements
This script require at least `Python 3.6`.

To install the script dependencies, run:
```bash
pip3 install -r source/requirements.txt
``` 

### Authenticate to GCP

Execute the following command:
```bash
gcloud auth application-default login
```

It'll open a browser tab, select the account you want to use, and validate the permission.

Once the process is over, the gcloud tool will create a credential file located to `~/.config/gcloud/application_default_credentials.json`

### Script helper
```bash
python3 gcp_nuke.py --help
usage: gcp_nuke.py [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] --project-id
                   PROJECT_ID [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        select log level
  --project-id PROJECT_ID
                        GCP project ID
  --dry-run             Dry run mode
```

### Script parameters

| Name          | Type   | Required | Description          | Example                           |
|:--------------|:-------|:---------|:---------------------|:----------------------------------|
| `--log-level` | string | no       | Script logging level | DEBUG,INFO,WARNING,ERROR,CRITICAL |
| `project-id`  | string | yes      | GCP Project ID       | my-awesome-project-1              |

### Script example

```bash
python3 gcp_nuke.py --project-id my-awesome-project-1
```

### Script output

```
[2020-08-02 17:32:41,668] - [INFO] - Checking auth for Project ID = my-awesome-project-1
[2020-08-02 17:32:43,702] - [INFO] - Auth successfully validated
[2020-08-02 17:32:43,702] - [CRITICAL] - /!\ Everything will be deleted in the Project ID = my-awesome-project-1!
Are you sure? (yes/no)
yes
[2020-08-02 17:32:46,545] - [INFO] - Deleting all GCP resources
[2020-08-02 17:32:46,545] - [INFO] - Deleting Google Storage buckets
[2020-08-02 17:32:48,517] - [INFO] - [Storage] Deleting bucket testkpr01
[2020-08-02 17:32:49,131] - [INFO] - [Storage] Deleting bucket testkpr02
[2020-08-02 17:32:49,951] - [INFO] - [Storage] All buckets are deleted
```