import csv
from dataclasses import dataclass
import xml.etree.cElementTree as ET
import uuid
import xml.dom.minidom
import datetime
from datetime import time, timedelta



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



WriteXML("TestSearchSet", "GEOMETRY", "Area", "1", "area","equals")