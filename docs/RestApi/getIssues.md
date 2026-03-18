---
layout: default
title: Issues
parent: Rest API
nav_order: 5
---

```python
import requests
import json

path = "access.txt"

with open(path, "r") as f:
    access_token = f.read().strip()


data = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

projectUuid = "..."

page = 28

license_projects= "https://api.sydney.revizto.com/v5/project/{projectUuid}/issue-filter/filter"

all_issues = []

for i in range(0 ,page):
    filters_payload = {
    "alwaysFiltersDTO": [
        {   "type": "type",
            "expr": 1,  # 1 = filter for "has any of these
            "value": [1]      
        },
        {
            #"type": "assignee",
            #"expr": 1,  # 1 = filter for "has any of these values"
            #"value": ["name@company.com"]
            # "type": "type",
            # "expr": 1,  # 1 = filter for "has any of these values"
            # "value": ["Drawing Stamp"]         

            # "type": "status",
            # "expr": 1,  # 1 = filter for "has any of these values"
            # "value": ["RL to Model"],

            "type": "customStatus",
            "expr": 1,  # 1 = filter for "has any of these
            "value": ["RLMU In Progress","RL to Model","RL N/A for Model"],        
        }
    ],
    "otherFiltersDTO": [],  # optional
    "page": i,
    }
    
    files = {
    "fields": (None, json.dumps(filters_payload))
    }
    response = requests.post(license_projects.format(projectUuid=projectUuid, page=i), headers=data, json=filters_payload, verify=False)

    entities = response.json().get('data', {}).get('data', [])

    pages = response.json().get('data', {}).get('pages', [])
    print ('pages', pages)
    all_issues.extend(entities)

# Prettify the entities array

pretty_entities = json.dumps(all_issues, indent=4)

#print(pretty_entities)

filename = "issues.json"
with open(filename, "w") as f:
    f.write(pretty_entities)
    print ("File saved")
```