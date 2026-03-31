import uuid

import blackboxprotobuf
from datetime import datetime, timedelta, timezone

def from_revizto_time(revizto_time: int) -> datetime:

    nanoseconds = 1_000_000_000

    #revizto timestamp (time at 31-12-2023 23:00)
    reviztoStartTime = 638396604*nanoseconds

    #revizto start date in project timezone (+8 hours)
    reviztoStartDate = datetime.strptime("20240101 07:00", "%Y%m%d %H:%M")

    # Compute the difference in seconds
    seconds_delta = (revizto_time - reviztoStartTime) * 100 / nanoseconds
    
    # Add to the base datetime
    return reviztoStartDate + timedelta(seconds=seconds_delta)


def ticks_to_datetime(ticks):
    # .NET ticks start from 0001-01-01, 1 tick = 100 ns
    epoch = datetime(1, 1, 1)
    return epoch + timedelta(microseconds=ticks / 10)

def searchsetIterator(_decdata):
    if isinstance(_decdata.get('4'), list):
        print("searchsets are inside a folder")
        for sset in _decdata['4']:
            if '8' not in sset:
                print (f"id: {sset['1']}, folder name: {sset['7'].decode('utf-8')}")
            else:
                #print (sset)
                print (f"id: {sset['1']}, searchset name: {sset['7'].decode('utf-8')}")
                print ("conditions")
                print (f"id: {sset['1']}, name: {sset['7'].decode('utf-8')}")
                for c in sset['8']['2']:
                    print (c)
    else:
        print("only one searchset found")
        #searchset id and name
        print (f"id: {_decdata['4']['1']}, name: {_decdata['4']['7'].decode('utf-8')}")
        #print (decdata['4']['8'])
        print ("conditions")
        for c in _decdata['4']['8']['2']:
            print (c)
            try:
                time = c['2']['2']['4']['3']
                print (time)
                #print (f"date: {from_revizto_time(time).strftime('%Y-%m-%d %H:%M')}")
            except Exception as e:
                print (e)

#path = r'.\Revizto buffer\TEST.vimsst'
path = 'TestSearchSet.vimsst'   

print ('path')

folder_guid = uuid.uuid4()
folder_guid_string = str(folder_guid)

sset_guid = uuid.uuid4()
sset_guid_string = str(sset_guid)

# Read and decode the data
with open(path, "rb") as f:
    generated_guid = uuid.uuid4()
    guid_string = str(generated_guid)

    data = f.read()
    print ('data read')
    #print (data)
    decdata, typeof = blackboxprotobuf.decode_message(data)
    print ('data decoded')
    #print (decdata)

    decdata = {'1': b'MarkerSearchSets', '2': 1, '3': 0, '4': {'1': folder_guid_string.encode(), '2': 639093218503073627, '3': 639093218768708912, '4': sset_guid_string.encode(), '5': 0, '6': 1, '7': b'UpdateFolderName', '8': {'1': 0, '2': {'1': 0, '2': {'2': {'1': 10, '2': {'2': b'IDENTITY DATA'}, '3': {'2': b'Assembly Code'}, '4': {'1': 5, '2': b'A1010100'}, '5': 6}}}, '3': 1}}}

    print ('updated decdata', decdata)
    encItem = blackboxprotobuf.encode_message(decdata, typeof)
    #print (encItem)

filename = '.\Revizto buffer\output.vimsst'
with open(filename, "wb") as f:
    f.write(encItem)
    print ("File saved")

