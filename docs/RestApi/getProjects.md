---
layout: default
title: Projects
parent: Rest API
nav_order: 3
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


licenseUuid = "..."
license_projects= "https://api.sydney.revizto.com/v5/project/list/{licenseUuid}/paged"

response = requests.get(license_projects.format(licenseUuid=licenseUuid), headers=data,verify=False )


entities = response.json().get('data', {}).get('data', [])

filtered_entities = [
    {
        "id": e.get("id"),
        "uuid": e.get("uuid"),
        "title": e.get("title")
    }
    for e in entities
]

# Prettify the entities array
pretty_entities = json.dumps(filtered_entities, indent=4)

print(pretty_entities)


filename = 'projects.json'
with open(filename, "w") as f:
    f.write(pretty_entities)
    print ("File saved")
```