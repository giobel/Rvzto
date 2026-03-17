---
layout: default
title: Create Search Sets with xml
parent: Search Sets
nav_order: 2
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
def WriteXML(searchset_name,category_name, property_name,property_value,property_type, operator):
    generated_guid = str(uuid.uuid4())
    root = ET.Element("exchange", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
                  xsi_noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd",
                  units="m", filename="", filepath="")
    selectionsets = ET.SubElement(root, "selectionsets")
    viewfolderId = str(uuid.uuid4())
    viewfolder = ET.SubElement(selectionsets, "viewfolder", name=searchset_name, guid=viewfolderId)
    selectionset = ET.SubElement(viewfolder, "selectionset", name=searchset_name, guid=generated_guid)
    #mode = all or selected or below disjoint = 1 for "Prune below results"
    findspec = ET.SubElement(selectionset, "findspec", mode="all", disjoint="0")
    conditions = ET.SubElement(findspec, "conditions")
    condition = ET.SubElement(conditions, "condition", test=operator, flags="10")
    category = ET.SubElement(condition, "category")
    name = ET.SubElement(category, "name", internal=category_name)
    name.text = category_name
    property_element = ET.SubElement(condition, "property")
    property = ET.SubElement(property_element, "name", internal=property_name)
    property.text = property_name
    value = ET.SubElement(condition, "value")
    data = ET.SubElement(value, "data", type=property_type)
    data.text = property_value
    locator = ET.SubElement(findspec, "locator")
    locator.text = "/"

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(tree.getroot(), encoding='utf-8').decode('utf-8')
    dom = xml.dom.minidom.parseString(xml_str)
    pretty = dom.toprettyxml(indent="  ")

    filePath = searchset_name + '.xml'
    with open(filePath, 'w') as file:
        file.write(pretty)

WriteXML("TestSearchSet", "IDENTITY DATA", "Name", "Elevator Pit", "wstring","equals")
```

XML Data Types can be found by exporting Search Sets from Navisworks. So far I have encountered:

- `wstring`: string values
- `double`: numeric property values
- `bool`: boolean conditions
- `time`: datetime values
- `area`: area values
- `linear`: length values

Same applies for operators:

- `equals`
- `less_than`
- `greater_than`

Flags:

- `10`: AND
- `74`: OR

### 4D Timeliner Example

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

If we want to generate multiple searchsets at one go, we can write our search sets names and dates in a .csv file and batch generate them.

Let's consider the below list of activities taken from P6 data:

```python
#Activity Name, Start Date, End Date
FRP 1A - T2 Pour,11-06-2026 08:00,11-06-2026 17:00
FRP 1B - T2 Pour,21-07-2026 08:00,21-07-2026 17:00
FRP 1C - T2 Pour,03-07-2026 08:00,03-07-2026 17:00
FRP 2A - T1 Pour,11-06-2026 08:00,11-06-2026 17:00
FRP 2B - T1 Pour,14-06-2026 08:00,14-07-2026 17:00
FRP 2C - T1 Pour,27-06-2026 08:00,27-06-2026 17:00
FRP 3 - A2 Pour,08-08-2026 08:00,08-08-2026 17:00
FRP 4 - A1 Pour,10-08-2026 08:00,10-08-2026 17:00
FRP 5 - Mid-Span Pour,18-08-2026 08:00,18-08-2026 17:00
```

We can convert the rows in the .csv file into a list of python objects:

```python
file_path = r"C:\Temp\troffs_dates.csv"

@dataclass
class AppearanceRule:
    activity: str
    start_date: str
    end_date: str

inputs =[]

with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row = [cell for i, cell in enumerate(row)]
        #print (row)
        inputs.append(AppearanceRule(*row))
```

Update the previous xml writer function to work with datetime values:

```python
def WriteXML(searchset_name,start_end, date_type,operator,task_type):
    folder  = r"C:\Temp"
    root = ET.Element("exchange", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
                  xsi_noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd",
                  units="m", filename="", filepath="")
    selectionsets = ET.SubElement(root, "selectionsets")
    viewfolderId = str(uuid.uuid4())
    viewfolder = ET.SubElement(selectionsets, "viewfolder", name=searchset_name, guid=viewfolderId)
    #currentDate = projectStartDate   

    for i in range(0,len(inputs)):

        currentDate = datetime.datetime.strptime(inputs[i].start_date, "%d-%m-%Y %H:%M")

        if start_end == 'Start':
            currentDate = datetime.datetime.strptime(inputs[i].start_date, "%d-%m-%Y %H:%M")
        elif start_end == 'End':
            currentDate = datetime.datetime.strptime(inputs[i].end_date, "%d-%m-%Y %H:%M")

        generated_guid = str(uuid.uuid4())

        #CURRENT DATE
        selectionset = ET.SubElement(viewfolder, "selectionset", name=searchset_name+"_"+str(currentDate), guid=generated_guid)

        findspec = ET.SubElement(selectionset, "findspec", mode="all", disjoint="0")
        conditions = ET.SubElement(findspec, "conditions")
        
        condition = ET.SubElement(conditions, "condition", test=operator, flags="10")
        category = ET.SubElement(condition, "category")
        name = ET.SubElement(category, "name", internal="TimeLiner+")
        name.text = "TimeLiner +"
        property_element = ET.SubElement(condition, "property")
        property_name = ET.SubElement(property_element, "name", internal=date_type)
        property_name.text = date_type
        value = ET.SubElement(condition, "value")
        data = ET.SubElement(value, "data", type="time")
        data.text = str(to_revizto_time(currentDate))

        condition2 = ET.SubElement(conditions, "condition", test="equals", flags="10")
        category2 = ET.SubElement(condition2, "category")
        name2 = ET.SubElement(category2, "name", internal="TimeLiner+")
        name2.text = "TimeLiner +"
        property_element2 = ET.SubElement(condition2, "property")
        property_name2 = ET.SubElement(property_element2, "name", internal="Task Type")
        property_name2.text = "Task Type"
        value2 = ET.SubElement(condition2, "value")
        data2 = ET.SubElement(value2, "data", type="wstring")
        data2.text = task_type
        locator = ET.SubElement(findspec, "locator")
        locator.text = "/"
        print ("done")

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(tree.getroot(), encoding='utf-8').decode('utf-8')
    dom = xml.dom.minidom.parseString(xml_str)
    pretty = dom.toprettyxml(indent="  ")
    filePath = folder + "\\" + searchset_name + '.xml'
    with open(filePath, 'w') as file:
        file.write(pretty)
```

And create all the search sets combinations:

```python
start = 'Actual Start Date'
end = 'Actual End Date'

build_greater_than = start +' Construct greater_than Start'
#HIDE all tasks starting strictly after the task end date
WriteXML(build_greater_than, "Start", start,"greater_than", "Construct")

build_greater_than = start +' Construct greater_than End'
#HIDE all tasks starting strictly after the task end date
WriteXML(build_greater_than, "End", start,"greater_than", "Construct")

demo_less_than = end +' Demo less_than Start'
#HIDE all demo strictly finishing before the task start date
WriteXML(demo_less_than, "Start", end,"less_than", "Demolition")

demo_less_than = end +' Demo less_than End'
#HIDE all demo strictly finishing before the task start date
WriteXML(demo_less_than, "End", end,"less_than", "Demolition")
```

![](/Rvzto/assets/timeliner.png)

### Limitations

- Conversion between Imperial and Metrics systems (Revizto takes care of the conversion internally but from my experience the input must be in Imperial units --> Further testing is required)
- From my expereiece, some options specific to Revizto cannot be set from the xml file --> Further testing is required

![](/Rvzto/assets/units.png)

- An area value of 1 in the xml file becomes 0.0929m² in Revizto (1 sq ft = 0.0929 m²)
- `Elements only` checkbox cannot be set from xml tags (this property does not exist in Navisworks)
- `Group` conditions cannot be set from xml (this property does not exist in Navisworks)

Due to these limitations, it is worth exploring the Search Sets creation from Revizto native .vimsst files.