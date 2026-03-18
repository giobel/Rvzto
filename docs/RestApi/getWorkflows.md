---
layout: default
title: Workflows
parent: Rest API
nav_order: 7
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

license_projects= "https://api.sydney.revizto.com/v5/project/{projectUuid}/issue-workflow/settings"

response = requests.get(license_projects.format(projectUuid=projectUuid), headers=data,verify=False )

print (response.json())

entities = response.json().get('data', {})


# Prettify the entities array
pretty_entities = json.dumps(entities, indent=4)

print(pretty_entities)


filename = 'workflows.json'
with open(filename, "w") as f:
    f.write(pretty_entities)
    print ("File saved")
```