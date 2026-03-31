import inspect
from unittest import case
import zlib
import blackboxprotobuf
from datetime import datetime, timedelta
import csv
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class AppearanceRule:
    schedule_name: str
    filter_name: str
    filter_id: str
    action: str
    value: str


def color_to_int(r, g, b, a=255, order='RGBA'):
    """
    Convert RGBA components (0–255) to a 32-bit integer.
    order = 'RGBA' or 'ARGB' (Revizto-like).
    """
    if order.upper() == 'RGBA':
        return (r << 24) | (g << 16) | (b << 8) | a
    elif order.upper() == 'ARGB':
        return (a << 24) | (r << 16) | (g << 8) | b
    else:
        raise ValueError("order must be 'RGBA' or 'ARGB'")
    

def printStars(message):
    try:
        print (f"********{varName(message).upper()}**********\n", message)
    except:
        print('**************\n',message)
        
def varName(var):
    lcls = inspect.stack()[2][0].f_locals
    for name in lcls:
        if id(var) == id(lcls[name]):
            return name
    return None

typeOf =  {'1': {'type': 'message', 'message_typedef': {'8': {'type': 'fixed64', 'name': ''}}, 'name': ''}, '2': {'type': 'int', 'name': ''}, '3': {'type': 'int', 'name': ''}, '4': {'type': 'message', 'message_typedef': {'2': {'type': 'int', 'name': ''}, '3': {'type': 'int', 'name': ''}, '4': {'type': 'bytes', 'name': ''}, '5': {'type': 'int', 'name': ''}, '6': {'type': 'message', 'message_typedef': {'1': {'type': 'int', 'name': ''}, '2': {'type': 'fixed64', 'name': ''}, '3': {'type': 'bytes', 'name': ''}}, 'name': ''}, '7': {'type': 'message', 'message_typedef': {'1': {'type': 'message', 'message_typedef': {'1': {'type': 'bytes', 'name': ''}, '2': {'type': 'bytes', 'name': ''}}, 'name': ''}}, 'name': ''}}, 'name': ''}, '5': {'type': 'message', 'message_typedef': {'1': {'type': 'message', 'message_typedef': {'1': {'type': 'bytes', 'name': ''}, '2': {'type': 'int', 'name': ''}}, 'name': ''}}, 'name': ''}}

decdata =  {'1': {'8': 8387201631772831856}, '2': 1, '3': 0, '4': {'2': 639047359173842779, '3': 639047359173842779, '4': b'123', '5': 0, '6': {'1': 0, '2': 11855818848412014350, '3': b'x\x9cu\xcc;\n\x021\x10\x00\xd0\xb5\x91\x90j\xd9F\xb0Ja;\x90\x99d\x93\t\x08*\nV[y\x82L>\x07\x90\xdc\x1f-ml^\xf9\xf4\xa6\xf6\xf3\xf5\xf8T\xd3r\xd77}\xd1\xa7Ju\xe5\xc6\x0c\xcef\x01\x1fs\x82\x84l\xbf\xf4^J\x0f=\x06\xb7\x1c^#\xbf\x87y\xe4\xd1\xcc\xd9\x90%\x0f\x96\x01Ioj7O\xbf\x1d\xb9T\xd0\xa5\x15(\xf4\x02^Z\x01\x11l\x10+\x16\x16d\x92 \x7f:\n\x1f\xa1\xbf$\x00'}, '7': {'1': []}}, '5': {'1': {'1': b'e89e600e-e40d-4229-932f-6e670fff5389', '2': 0}}}

outputData = {'1': {'8': 8387201631772831856}, '2': 1, '3': 0, '4': [], '5': {'1': {'1': b'e89e600e-e40d-4229-932f-6e670fff5389', '2': 0}}}

# Path to your Excel file
file_path = r"C:\Repos\TC access\Outputs\Appearance Template Master.csv"


inputs = []
# Read CSV and create AppearanceRule instances
with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    # Read header
    header = next(reader)
    print('header', header)
    clean_header = [col for col in header if col.strip()]
    printStars(clean_header)
    empty_column_indices = [i for i, col in enumerate(header) if not col.strip()]
    
    # Read rows
    for row in reader:
        row = [cell for i, cell in enumerate(row) if i not in empty_column_indices]
        print (row)
        inputs.append(AppearanceRule(*row))



printStars(inputs)

grouped_by_schedule = defaultdict(list)

for rule in inputs:
    grouped_by_schedule[rule.schedule_name].append(rule)



#inputs = ['name1, id, searchName1', 'name2, id2, search_name2']
#inputs = ['928f394d-bb1e-4bcf-a874-3a7b79bb217b, Start Date < 2024-08-26','505f9cb6-60d7-4063-966e-d743e4125875, Start Date < 2024-08-19','505f9cb6-60d7-4063-966e-d743e4125875, Start Date < 2024-08-19']
print (grouped_by_schedule)

for schedule, rules_in_schedule in grouped_by_schedule.items():
    templatesMould = {'2': 639047359173842779, '3': 639047359173842779, '4': b'123', '5': 0, '6': {'1': 0, '2': 11855818848412014350, '3': b'x\x9cu\xcc;\n\x021\x10\x00\xd0\xb5\x91\x90j\xd9F\xb0Ja;\x90\x99d\x93\t\x08*\nV[y\x82L>\x07\x90\xdc\x1f-ml^\xf9\xf4\xa6\xf6\xf3\xf5\xf8T\xd3r\xd77}\xd1\xa7Ju\xe5\xc6\x0c\xcef\x01\x1fs\x82\x84l\xbf\xf4^J\x0f=\x06\xb7\x1c^#\xbf\x87y\xe4\xd1\xcc\xd9\x90%\x0f\x96\x01Ioj7O\xbf\x1d\xb9T\xd0\xa5\x15(\xf4\x02^Z\x01\x11l\x10+\x16\x16d\x92 \x7f:\n\x1f\xa1\xbf$\x00'}, '7': {'1': []}}
    print(f"\nSchedule: {schedule}")
    templatesMould['4'] = schedule
    #printStars(templatesMould)
    blob1 = templatesMould['6']['3']
    #DECOMPRESS TEMPLATE PROPERTIES
    mes1 = zlib.decompress(blob1)
    # DECODE TEMPLATE PROPERTIES
    decItem, itemTypeOf = blackboxprotobuf.decode_message(mes1)
    decItem = {'1': []}
    
    for r in rules_in_schedule:
        print(f"  {r.filter_name} | {r.action} | {r.value}")

        match r.action.lower():
            case 'hide':
                decItem['1'].append({'1': 1, '2': 0, '3': {'1': 0, '2': {'1': {'1': {'1': r.filter_id.encode(), '2': r.filter_name.encode()}}}}})
            case 'unhide':
                decItem['1'].append({'1': 2, '2': 0, '3': {'1': 0, '2': {'1': {'1': {'1': r.filter_id.encode(), '2': r.filter_name.encode()}}}}})
            case 'isolate': 
                decItem['1'].append({'1': 3, '2': 0, '3': {'1': 0, '2': {'1': {'1': {'1': r.filter_id.encode(), '2': r.filter_name.encode()}}}}})
            case 'color':
                # Map color names to integer values (example values)
                rgbvalue = r.value.split('-')
                color_value = color_to_int(int(rgbvalue[0]), int(rgbvalue[1]), int(rgbvalue[2]))
                decItem['1'].append({'1': 4, '2': color_value, '3': {'1': 0, '2': {'1': {'1': {'1': r.filter_id.encode(), '2': r.filter_name.encode()}}}}})
            case 'transparent':
                # Map transparency percentages to integer values (example values)
                transparency_map = {
                    '25': 192,
                    '50': 128,
                    '75': 64,
                }
                transparency_value = transparency_map.get(r.value.lower(), 0)
                decItem['1'].append({'1': 5, '2': transparency_value, '3': {'1': 0, '2': {'1': {'1': {'1': r.filter_id.encode(), '2': r.filter_name.encode()}}}}})
            case 'reset transparency':
                decItem['1'].append({'1': 8, '2': 0, '3': {'1': 0, '2': {'1': {'1': {'1': r.filter_id.encode(), '2': r.filter_name.encode()}}}}})

    encItem = blackboxprotobuf.encode_message(decItem, itemTypeOf)

    #replaced message
    mes2 = zlib.compress(encItem)

    templatesMould['6']['3'] = mes2

    print('append')
    outputData['4'].append(templatesMould)
    printStars(outputData)

    # data2 = blackboxprotobuf.encode_message(templatesMould, typeOf)
    # filename = schedule.replace('<', '_').replace('>', '_') + '.aptmpl'
    # with open(filename, "wb") as f:
    #     f.write(data2)

    #     print ("Done")



data2 = blackboxprotobuf.encode_message(outputData, typeOf)
filename = r"C:\Repos\TC access\Outputs\AppTemplates.aptmpl"
with open(filename, "wb") as f:
    f.write(data2)

    print ("Done")

    
"""
for input_str in inputs:
    # SET TEMPLATE NAME
    decdata['4']['4'] = input_str.schedule_name

    # EXTRACT TEMPLATE PROPERTIES
    blob1 = decdata['4']['6']['3']
    printStars(blob1)

    #DECOMPRESS TEMPLATE PROPERTIES
    mes1 = zlib.decompress(blob1)
    printStars(mes1)

    # DECODE TEMPLATE PROPERTIES
    decItem, itemTypeOf = blackboxprotobuf.decode_message(mes1)
    printStars (decItem)

    decItem = {'1': []}


    decItem['1'].append({'1': 4, '2': 1325369087, '3': {'1': 0, '2': {'1': {'1': {'1': input_str.filter_id.encode(), '2': input_str.schedule_name.encode()}}}}})


    encItem = blackboxprotobuf.encode_message(decItem, itemTypeOf)

    #replaced message
    mes2 = zlib.compress(encItem)

    decdata['4']['6']['3'] = mes2

    printStars(decdata)

    data2 = blackboxprotobuf.encode_message(decdata, typeOf)
    filename = input_str.schedule_name.replace('<', '_').replace('>', '_') + '.aptmpl'
    with open(filename, "wb") as f:
        f.write(data2)

    print ("Done")
    """