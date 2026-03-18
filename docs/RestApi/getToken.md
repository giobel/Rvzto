---
layout: default
title: Tokens
parent: Rest API
nav_order: 1
---


## Get Token

```python
import requests

region = "sydney" 
base_url = f"https://api.{region}.revizto.com/v5/oauth2"
access_code = "" #navigate to https://ws.revizto.com/login?request=accessCode and get the temporary auth code

# For the Authorization Code flow:
data = {
    "grant_type": "authorization_code",
    "code": access_code
}

# Configure corporate proxy
proxy_url = "..."
proxies = {
    "http": proxy_url,
    "https": proxy_url
}


try:
    # Use proxy without SSL verification
    response = requests.post(base_url, data=data, verify=False)
    
    print(response.status_code)
    
    if (response.status_code == 200):
        token_info = response.json()
        print("Token response:", token_info)
        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)

        #save the token locally
        filename = 'access.txt'
        with open(filename, "w") as f:
            f.write(access_token)
            print ("File saved")
        #save the refresh token locally. valid for 1 month
        filename = 'refresh.txt'
        with open(filename, "w") as f:
            f.write(refresh_token)
            print ("File saved")
            
except requests.exceptions.ProxyError as e:
    print(f"Proxy Error: {e}")
    print("Unable to connect through proxy")
except requests.exceptions.SSLError as e:
    print(f"SSL Certificate Error: {e}")
except Exception as e:
    print(f"Error: {e}")

```


## Refresh Token

```python
import requests

region = "sydney"  
base_url = f"https://api.{region}.revizto.com/v5/oauth2"

path = "refresh.txt"

with open(path, "r") as f:
    refresh_token = f.read().strip()

path = "access.txt"

with open(path, "r") as f:
    access_token = f.read().strip()

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
}

# For the Authorization Code flow:
data = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
}


response = requests.post(base_url, data=data, headers=headers, verify=False)

token_info = response.json()
print("Token response:", token_info)
access_token = token_info.get("access_token")
refresh_token = token_info.get("refresh_token")
print("Access Token:", access_token)
print("Refresh Token:", refresh_token)

if access_token != None:
    filename = 'access.txt'
    with open(filename, "w") as f:
        f.write(access_token)
        print ("File saved")

if refresh_token != None:
    filename = 'refresh.txt'
    with open(filename, "w") as f:
        f.write(refresh_token)
        print ("File saved")
```