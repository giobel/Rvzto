---
layout: default
title: Sheets
parent: Rest API
nav_order: 4
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

license_projects= "https://api.sydney.revizto.com/v5/project/{projectUuid}/sheet/list"


response = requests.post(license_projects.format(projectUuid=projectUuid), headers=data, verify=False)

entities = response.json().get('data', {}).get('entities', [])

# Prettify the entities array
pretty_entities = json.dumps(entities, indent=4)

filename = 'reviztoSheets.json'
with open(filename, "w") as f:
    f.write(pretty_entities)
    print ("File saved")
```