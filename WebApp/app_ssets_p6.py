import datetime
from flask import Flask, request, render_template, send_file
import xml.etree.cElementTree as ET
import uuid
import xml.dom.minidom
import io

nanoseconds = 1_000_000_000
# revizto time at date 01/01/2024
reviztoStartDate = datetime.datetime.strptime("20240101", "%Y%m%d")
reviztoStartTime = 638396604*nanoseconds


def WriteXML(fileName):
    mondays = int(request.form["duration"].strip()) * 52
    projectStartDate = datetime.datetime.strptime(request.form["projectStartDate"].strip(), "%Y%m%d")
    folderName = request.form["folderName"].strip()
    prefix = request.form["prefix"].strip()

    # Get lists of criteria
    categoryNames = request.form.getlist('categoryName[]')
    propertyNames = request.form.getlist('propertyName[]')
    conditionTests = request.form.getlist('conditionTest[]')
    flags = request.form.getlist('flag[]')
    intervals = request.form.getlist('interval[]')
    interval = int(intervals[0].strip()) if intervals else 7  # Use first interval or default

    delta = projectStartDate-reviztoStartDate
    startDateTime = reviztoStartTime + delta.days *24*60*60/100*nanoseconds
    root = ET.Element("exchange", xmlns_xsi="http://www.w3.org/2001/XMLSchema-instance",
                  xsi_noNamespaceSchemaLocation="http://download.autodesk.com/us/navisworks/schemas/nw-exchange-12.0.xsd",
                  units="m", filename="", filepath="")
    selectionsets = ET.SubElement(root, "selectionsets")
    viewfolderId = str(uuid.uuid4())
    viewfolder = ET.SubElement(selectionsets, "viewfolder", name=folderName, guid=viewfolderId)
    currentDate = projectStartDate   
    for i in range(0,mondays):
        print (currentDate.date())
        generated_guid = str(uuid.uuid4())
        selectionset = ET.SubElement(viewfolder, "selectionset", name=prefix+'_'+str(currentDate.date()), guid=generated_guid)
        findspec = ET.SubElement(selectionset, "findspec", mode="all", disjoint="0")
        conditions = ET.SubElement(findspec, "conditions")
        
        # Loop through search criteria
        for j in range(len(categoryNames)):
            condition = ET.SubElement(conditions, "condition", test=conditionTests[j].strip(), flags=flags[j].strip())
            category = ET.SubElement(condition, "category")
            name = ET.SubElement(category, "name", internal=categoryNames[j].strip())
            name.text = categoryNames[j].strip()
            property_element = ET.SubElement(condition, "property")
            property_name = ET.SubElement(property_element, "name", internal=propertyNames[j].strip())
            property_name.text = propertyNames[j].strip()
            value = ET.SubElement(condition, "value")
            data = ET.SubElement(value, "data", type="time")
            
            delta = currentDate - projectStartDate
            currentTime = int(startDateTime + delta.days*24*60*60/100*nanoseconds)
            data.text = str(currentTime)

        #GENERATE A SEARCH SET EVERY interval DAYS
        currentDate = datetime.timedelta(days = interval) + currentDate

        locator = ET.SubElement(findspec, "locator")
        locator.text = "/"
        print ("done")

    tree = ET.ElementTree(root)
    xml_str = ET.tostring(tree.getroot(), encoding='utf-8').decode('utf-8')
    dom = xml.dom.minidom.parseString(xml_str)
    pretty = dom.toprettyxml(indent="  ")
    return pretty

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("ssetP6.html")

# AJAX endpoint to process & return aptmpl file
@app.route("/process_ajax", methods=["POST"])
def process_ajax():
    # Process the data (this is a placeholder for actual processing logic)
    processed_data = WriteXML("SearchSets")  # Placeholder for actual processing

    # Return the processed data as a downloadable file
    return send_file(
        io.BytesIO(processed_data.encode()),
        as_attachment=True,
        download_name="SearchSet.xml"
    )

if __name__ == "__main__":
    print("Running on http://127.0.0.1:5000")
    app.run(debug=True)



