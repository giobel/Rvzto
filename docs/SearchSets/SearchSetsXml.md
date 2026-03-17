---
layout: default
title: Create Search Sets with xml
parent: Search Sets
nav_order: 5
---

# Create Search Sets with xml

Revizto uses the same xml schema that Navisworks uses to create Search Sets:

```xml
<?xml version="1.0" ?>
    <exchange xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance" xsi_noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd" units="m" filename="" filepath="">
        <selectionsets>
            <viewfolder name="XML Search Sets" guid="1a062305-0bb7-4758-9954-b11d3f49eaff">
                <selectionset name="Search Set 1" guid="8d52f6e9-a8c6-4659-a491-2093e79241ee">
                    ...
                </selectionset>
                <selectionset name="Search Set 2" guid="8d52f6e9-a8c6-4659-a491-2093e79241ee">
                    ...
                </selectionset>
            </viewfolder>
        </selectionsets>
    </exchange>
```

`exchange`: the root element.

`selectionsets`: container for all imported search sets.

`viewfolder`: folder grouping search sets (optional)

`selectionset`: individual named search set

Each `selectionset` contains the filter's conditions:

```xml
    <findspec mode="all" disjoint="0">
    <conditions>
        <condition test="less_than" flags="10">
        <category>
            <name internal="TimeLiner+">TimeLiner +</name>
        </category>
        <property>
            <name internal="Actual End Date">Actual End Date</name>
        </property>
        <value>
            <data type="time">639167328000000000</data>
        </value>
        </condition>
        <condition test="equals" flags="10">
        <category>
            <name internal="TimeLiner+">TimeLiner +</name>
        </category>
        <property>
            <name internal="Task Type">Task Type</name>
        </property>
        <value>
            <data type="wstring">Demolition</data>
        </value>
        </condition>
    </conditions>
    <locator>/</locator>
    </findspec>
```
![](/Rvzto/assets/searchSetsXml.png)

We can use python xml.etree.ElementTree module to automatically generate the XML file.

```python
def WriteXML(searchset_name,start_end, date_type,operator,task_type):
    root = ET.Element("exchange", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
                  xsi_noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd",
                  units="m", filename="", filepath="")
    selectionsets = ET.SubElement(root, "selectionsets")
    viewfolderId = str(uuid.uuid4())
    viewfolder = ET.SubElement(selectionsets, "viewfolder", name=searchset_name, guid=viewfolderId)


```










One importatnt thing to remember is Datetime values are stored in nanoseconds starting from 01-01-0001 (.NET DateTime counts the number of ticks since midnight, January 1, 0001).

We can create a function to convert datetime to Revizto nanoseconds time:

```python
def to_revizto_time(dt: datetime.datetime) -> int:
    """
    Convert a Python datetime to Revizto nanosecond time.
    """
    nanoseconds = 1_000_000_000
    #revizto timestamp (time at 31-12-2023 23:00)
    reviztoStartTime = 638396604*nanoseconds
    #revizto start date in project timezone (+8 hours)
    reviztoStartDate = datetime.strptime("20240101 07:00", "%Y%m%d %H:%M")
    delta = dt - reviztoStartDate
    return int(reviztoStartTime + (delta.total_seconds() * nanoseconds / 100))
```

