import csv
from dataclasses import dataclass
import xml.etree.cElementTree as ET
import uuid
import xml.dom.minidom
import datetime
from datetime import time, timedelta

#CHANGE THE NUMBER OF YEARS TO GENERATE MORE SEARCH SETS
#years = 3
file_path = r"C:\Repos\TC access\Inputs\troffs_dates.csv"
#C:\Repos\openShell\troffs_dates.csv

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


def to_revizto_time(dt: datetime.datetime) -> int:
    """
    Convert a Python datetime to Revizto nanosecond time.
    """
    delta = dt - reviztoStartDate
    return int(reviztoStartTime + (delta.total_seconds() * nanoseconds / 100))

#mondays = 52 * years
mondays = 1
nanoseconds = 1_000_000_000

# revizto time at date 01/01/2024
reviztoStartDate = datetime.datetime.strptime("20240101 07:00", "%Y%m%d %H:%M")

#revizto time at date 01/01/2024 This come from Paul's XML file
reviztoStartTime = 638396604*nanoseconds

print (reviztoStartTime)

def WriteXML(searchset_name,start_end, date_type,operator,task_type):
    # we set our project start day at 30/09/2024 
    #projectStartDate = datetime.datetime.strptime("20260201", "%Y%m%d")
    #print (projectStartDate.time())

    folder  = r"C:\Repos\TC access\Outputs"
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
    


        print (currentDate.date())
        generated_guid = str(uuid.uuid4())
        #weekAheadDate = currentDate - datetime.timedelta(days = 7)
        #print (weekAheadDate.date())

        #CURRENT DATE
        selectionset = ET.SubElement(viewfolder, "selectionset", name=searchset_name+"_"+str(currentDate), guid=generated_guid)
        #WEEK AHEAD DATE
        #selectionset = ET.SubElement(viewfolder, "selectionset", name=str(weekAheadDate.date()), guid=generated_guid)

        findspec = ET.SubElement(selectionset, "findspec", mode="all", disjoint="0")
        conditions = ET.SubElement(findspec, "conditions")
        #condition = ET.SubElement(conditions, "condition", test="contains", flags="10")
        #condition = ET.SubElement(conditions, "condition", test="less_equal", flags="10"
        
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


def WriteXMLinBetween(searchset_name):

    folder = r"C:\Repos\TC access\Outputs"

    root = ET.Element(
        "exchange",
        xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
        xsi_noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd",
        units="m",
        filename="",
        filepath=""
    )

    selectionsets = ET.SubElement(root, "selectionsets")
    viewfolder = ET.SubElement(
        selectionsets,
        "viewfolder",
        name=searchset_name,
        guid=str(uuid.uuid4())
    )

    for rule in inputs:

        currentStartDate = datetime.datetime.strptime(rule.start_date, "%d-%m-%Y %H:%M")
        currentEndDate = datetime.datetime.strptime(rule.end_date, "%d-%m-%Y %H:%M")

        print("Start:", currentStartDate)
        print("End:  ", currentEndDate)

        selectionset = ET.SubElement(
            viewfolder,
            "selectionset",
            name=f"{searchset_name}_{currentStartDate}_{currentEndDate}",
            guid=str(uuid.uuid4())
        )

        findspec = ET.SubElement(selectionset, "findspec", mode="all", disjoint="0")
        conditions = ET.SubElement(findspec, "conditions")

        start = "Actual Start Date"
        end = "Actual End Date"
        # -------- Actual Start Date >= --------
        condition_start = ET.SubElement(conditions, "condition", test="greater_equal", flags="10")
        category = ET.SubElement(condition_start, "category")
        name = ET.SubElement(category, "name", internal="TimeLiner+")
        name.text = "TimeLiner +"

        prop = ET.SubElement(condition_start, "property")
        prop_name = ET.SubElement(prop, "name", internal=start)
        prop_name.text = start

        value = ET.SubElement(condition_start, "value")
        data = ET.SubElement(value, "data", type="time")
        data.text = str(to_revizto_time(currentStartDate))

        # -------- Actual End Date <= --------
        condition_end = ET.SubElement(conditions, "condition", test="less_equal", flags="10")
        category2 = ET.SubElement(condition_end, "category")
        name2 = ET.SubElement(category2, "name", internal="TimeLiner+")
        name2.text = "TimeLiner +"

        prop2 = ET.SubElement(condition_end, "property")
        prop_name2 = ET.SubElement(prop2, "name", internal=start)
        prop_name2.text = start

        value2 = ET.SubElement(condition_end, "value")
        data2 = ET.SubElement(value2, "data", type="time")
        data2.text = str(to_revizto_time(currentEndDate))

        locator = ET.SubElement(findspec, "locator")
        locator.text = "/"

        print("✔ done")

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(tree.getroot(), encoding="utf-8")
    dom = xml.dom.minidom.parseString(xml_str)
    pretty = dom.toprettyxml(indent="  ")

    filePath = folder + "\\" + searchset_name + ".xml"
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(pretty)




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

WriteXMLinBetween("Tasks Starts in Between")


#GO TO REVIZTO IMPORT THE SEARCHEST AND EXPORT THE CREATED SEARCH SETS TO .VIMMS TO THE INPUT FOLDER BEFORE STEP 2