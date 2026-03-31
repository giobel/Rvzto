from dataclasses import dataclass
from datetime import datetime
import blackboxprotobuf
import csv



#path2 = r'C:\Repos\TC access\production\Ex Bridge Demo Hidden.vimsst'
path2 = r'C:\Repos\TC access\Inputs\Deck Pour Sequence.vimsst'

# Read and decode the data
with open(path2, "rb") as f:
    data = f.read()
    decdata, typeof = blackboxprotobuf.decode_message(data)


searchSets = {}

# Open CSV file for writing
with open(r'C:\Repos\TC access\Outputs\SarchSetsExport.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Optional header
    writer.writerow(['Name','ID'])

    # Loop through entries
    for e in decdata['4']:
        # Decode byte strings safely
        id_decoded = e['1'].decode('utf-8') if isinstance(e['1'], bytes) else str(e['1'])
        name_decoded = e['7'].decode('utf-8') if isinstance(e['7'], bytes) else str(e['7'])

        # Print to console
        #print(name_decoded,id_decoded)
        searchSets[name_decoded] = id_decoded

        # Write to CSV
        writer.writerow([name_decoded,id_decoded])
        print("Done")



file_path = r'C:\Repos\TC access\Inputs\troffs_dates.csv'

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
        print (row)
        inputs.append(AppearanceRule(*row))


with open('C:\Repos\TC access\Outputs\Appearance Template Master.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['TEMPLATE NAME','SEARCH SET NAME','SEARCH SET ID','ACTION','PARAMETERS'])
    start = 'Actual Start Date'
    end = 'Actual End Date'
    tag = '800-'
    for i in inputs:
        exBridgeDemoContext = 'Deck Pour Sequence Context'
        search_set_id = searchSets.get(exBridgeDemoContext, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", exBridgeDemoContext, search_set_id, 'Isolate', ''])

        exBridgeDemoHide = 'Deck Pour Sequence Hidden'
        search_set_id = searchSets.get(exBridgeDemoHide, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", exBridgeDemoHide, search_set_id, 'Hide', ''])
        formatted_start = datetime.strptime(i.start_date, "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
        formatted_end = datetime.strptime(i.end_date, "%d-%m-%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")

        demo_less_than_start = end +' Demo less_than Start_' + formatted_start
        search_set_id = searchSets.get(demo_less_than_start, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", demo_less_than_start, search_set_id, 'Hide', ''])

        build_greater_than_end = start +' Construct greater_than End_' + formatted_end
        search_set_id = searchSets.get(build_greater_than_end, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", build_greater_than_end, search_set_id, 'Hide', ''])

        build_greater_than_start = start +' Construct greater_than Start_' + formatted_start
        search_set_id = searchSets.get(build_greater_than_start, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", build_greater_than_start, search_set_id, 'Color', '255-116-10'])

        demo_less_than_end = end +' Demo less_than End_' + formatted_end
        search_set_id = searchSets.get(demo_less_than_end, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", demo_less_than_end, search_set_id, 'Color', '241-14-38'])

        tasks_starts_in_between = "Tasks Starts in Between_" + formatted_start + "_" + formatted_end
        search_set_id = searchSets.get(tasks_starts_in_between, 'Not Found')
        writer.writerow([f"{tag}{i.activity}-{i.start_date}_{i.end_date}", tasks_starts_in_between, search_set_id, 'Color', '79-134-255'])

print("Done")

