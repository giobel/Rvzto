---
layout: default
title: Stamps
parent: Rest API
nav_order: 6
---

```python
import uuid
import requests
import json
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Get current date and time
now = datetime.now()

# Format as string: YYYY-MM-DD HH:MM:SS

path = "access.txt"

with open(path, "r") as f:
    access_token = f.read().strip()

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}
create_issue_url= "https://api.sydney.revizto.com/v5/issue/add"


projectUuid = ""
sheetUuid = ""

def CreateIssue(url, _headers,_externalUuid, _Zoffset):
    issue_uuid = str(uuid.uuid4())
    print ("Generated Issue UUID:", issue_uuid)
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    print("Current Timestamp:", timestamp_str)
    fields_payload =   {
                    "title": {
                        "timestamp": timestamp_str,
                        "value": f"api issue"
                    },
                    "tags": {
                        "value": ["EX UT  - ELECTRICAL"],
                        "timestamp": timestamp_str
                    },
                    "customType": {
                        "timestamp": timestamp_str,
                        "value": "dbbedbc1-0d15-4f96-a37d-1993e8367f73"                  
                    },
                    "reporter": {
                        "timestamp": timestamp_str,
                        "value": "name@company.com"
                    },
                    "assignee": {
                        "timestamp": timestamp_str,
                        "value": "name@compnay.com"
                    },
                    "sheet": {
                                "timestamp": timestamp_str,
                                "value": {
                                "uuid": _externalUuid,
                                "viewCenter": {
                                "x": 0.5,
                                "y": 0.5
                                },
                                "viewMarker": {
                                "x": 0.015,
                                "y": _Zoffset
                                },
                                "viewScale": 1.0,
                                "aspect": 1.0
                                }
                            },
                    "stampScale": {
                            "timestamp": timestamp_str,
                            "value": 0.75
                            },
                                    "stampAbbr": {
                        "value": "ZZZZ",
                        "timestamp": timestamp_str
                    },
                    "stampColor": {
                        "value": 1,
                        "timestamp": timestamp_str
                    },
                    "stampScale": {
                        "value": 0.75,
                        "timestamp": timestamp_str
                    },
                            "pin": {
                                    "timestamp": timestamp_str,
                                    "value": {
                                    "index": 0,
                                    "scale": 0.75,
                                    "visibility": True
                                    }

                            }
                }
    fields_json = json.dumps(fields_payload)
    files = {
    "fields": (None, fields_json,'application/json'),
    "uuid": (None, issue_uuid),
    "project_id": (None, "...")
    }
    response = requests.post(url, headers=_headers, files=files, verify=False)
    print(response.status_code)

with open("reviztoSheets.json", "r", encoding="utf-8") as f:
    sheets = json.load(f)

zOffset = 0.97  # Offset each issue slightly in Z-axis

sheetNumbers = ["xxx-xxx-DRG-6060-ST-00001"]


for i in range(0,len(sheetNumbers)):
    print(f"Creating issue {i+1} for sheet {sheetNumbers[i]} with Z-offset {zOffset}")
    external_uuid = next(
    (e.get("externalUuid")
    for e in sheets if sheetNumbers[i] in e.get("title", "")),
    None
    )
    print (f"Found external UUID: {external_uuid} for sheet number: {sheetNumbers[i]}")

    if external_uuid != None:
        CreateIssue(create_issue_url, headers, external_uuid, zOffset)
```