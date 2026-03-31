from dataclasses import dataclass
from datetime import datetime
import blackboxprotobuf
import csv


path2 = 'Federated Model All Searchsets.vimsst'

# Read and decode the data
with open(path2, "rb") as f:
    data = f.read()
    decdata, typeof = blackboxprotobuf.decode_message(data)


searchSets = {}

# Open CSV file for writing
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
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