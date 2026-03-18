---
layout: default
title: Create Search Sets with .vimsst
parent: Search Sets
nav_order: 3
---

# Create Search Sets with vimsst

We have already seen how to read the content of a search sets .vimsst file. Let's now see how we can recreate it.

Let's use this search set as an example:

![](/Rvzto/assets/vim1.png)

If we decode the search set created with the xml writer, the output looks like:

```python
{'1': b'MarkerSearchSets', '2': 1, '3': 0, '4': {'1': b'17dd4b8d-9202-43df-a446-00f5ac131a86', '2': 639093218503073627, '3': 639093218768708912, '4': b'462d5e6f-939a-4106-b543-b1cb5ff5f836', '5': 0, '6': 1, '7': b'TestSearchSet', '8': {'1': 0, '2': {'1': 0, '2': {'2': {'1': 10, '2': {'2': b'IDENTITY DATA'}, '3': {'2': b'Name'}, '4': {'1': 5, '2': b'Elevator Pit'}, '5': 6}}}, '3': 0}}}
```

If we make some changes to the property names or values

```python
{'1': b'MarkerSearchSets', '2': 1, '3': 0, '4': {'1': b'17dd4b8d-9202-43df-a446-00f5ac131a86', '2': 639093218503073627, '3': 639093218768708912, '4': b'462d5e6f-939a-4106-b543-b1cb5ff5f836', '5': 0, '6': 1, '7': b'UpdateFolderName', '8': {'1': 0, '2': {'1': 0, '2': {'2': {'1': 10, '2': {'2': b'IDENTITY DATA'}, '3': {'2': b'Assembly Code'}, '4': {'1': 5, '2': b'A1010100'}, '5': 6}}}, '3': 1}}}
```

The full script is:

```python
path = 'TestSearchSet.vimsst'   
# Read and decode the data
with open(path, "rb") as f:
    data = f.read()
    print ('data read')
    decdata, typeof = blackboxprotobuf.decode_message(data)
    
    decdata = {'1': b'MarkerSearchSets', '2': 1, '3': 0, '4': {'1': b'17dd4b8d-9202-43df-a446-00f5ac131a86', '2': 639093218503073627, '3': 639093218768708912, '4': b'462d5e6f-939a-4106-b543-b1cb5ff5f836', '5': 0, '6': 1, '7': b'UpdateFolderName', '8': {'1': 0, '2': {'1': 0, '2': {'2': {'1': 10, '2': {'2': b'IDENTITY DATA'}, '3': {'2': b'Assembly Code'}, '4': {'1': 5, '2': b'A1010100'}, '5': 6}}}, '3': 1}}}

    encItem = blackboxprotobuf.encode_message(decdata, typeof)

filename = 'output.vimsst'
with open(filename, "wb") as f:
    f.write(encItem)
    print ("File saved")
```

The Search Set in Revizto will be updated:

![](/Rvzto/assets/vim2.png)


Search Sets folders and individual Search Sets all require an uuid.

To generate one we can use the in-built python module:

```python
generated_guid = uuid.uuid4()
guid_string = str(generated_guid)
```

and add it to our decdata wherever we need it by encoding it:

```python
guid_string.encode()
```

Combining them:

```python
folder_guid = uuid.uuid4()
folder_guid_string = str(folder_guid)

sset_guid = uuid.uuid4()
sset_guid_string = str(sset_guid)

decdata = {'1': b'MarkerSearchSets', '2': 1, '3': 0, '4': {'1': folder_guid_string.encode(), '2': 639093218503073627, '3': 639093218768708912, '4': sset_guid_string.encode(), '5': 0, '6': 1, '7': b'UpdateFolderName', '8': {'1': 0, '2': {'1': 0, '2': {'2': {'1': 10, '2': {'2': b'IDENTITY DATA'}, '3': {'2': b'Assembly Code'}, '4': {'1': 5, '2': b'A1010100'}, '5': 6}}}, '3': 1}}}
```