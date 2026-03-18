---
layout: default
title: Licences
parent: Rest API
nav_order: 2
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

user_licence ="https://api.sydney.revizto.com/v5/user/licenses"

response = requests.get(user_licence, headers=data,verify=False )

print (response.json())

entities = response.json().get('data', {}).get('entities', [])

# Prettify the entities array
pretty_entities = json.dumps(entities, indent=4)

print(pretty_entities)


filename = 'licenses.json'
with open(filename, "w") as f:
    f.write(pretty_entities)
    print ("File saved")
```