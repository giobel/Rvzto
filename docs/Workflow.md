---
layout: default
title: Workflows
nav_order: 2
---

# Workflows
{: .no_toc }

## Appearance Templates

### Duplicate Appearance Templates conditions for multiple property values

<img width="870" height="728" alt="Image" src="https://github.com/user-attachments/assets/272813b8-967f-405b-9a60-d974ecd80860" />

### Create Appearance Templates from Excel 

<img width="1221" height="517" alt="Image" src="https://github.com/user-attachments/assets/1952b675-75e5-4663-8ebc-55fc25fb3728" />

### Search Sets

### Create Search Sets with multiple conditions from .csv file

<img width="1638" height="345" alt="Image" src="https://github.com/user-attachments/assets/761ebd81-3a58-4c69-a2c4-f7e69ea6aa53" />

## 4D Timeliner

1. Create Search Sets from .csv file exported from P6
   <img width="1240" height="494" alt="Image" src="https://github.com/user-attachments/assets/3b1954d9-bd50-4725-b64d-0259858d1287" />
3. Load the Search Sets into Revizto and export a .vimmsst file
4. Extract Search Sets ids from .vimsst file
   <img width="1930" height="397" alt="Image" src="https://github.com/user-attachments/assets/6c2409a2-6170-4abe-a229-f7d748e4e3d4" />
6. Generate Excel template with Search Sets Conditions
   <img width="3561" height="781" alt="Image" src="https://github.com/user-attachments/assets/1a8b6907-71d9-4806-a9db-d73e93a1b040" />
8. Generate Appearance Templates from Excel

```python
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
```

## Usage

### Automatically colour elements by properties 

https://github.com/user-attachments/assets/b28d6037-7f4f-4a79-8aee-bd23b71033c4

### 4D Timeliner

Colour elements based on their start/end dates or construct/demolish actions.

## Notes

- Search Sets can be created from scratch by compiling a .xml file or a .vimsst file.
- Apperance Templates can be set up using property items or search sets. The starting point can be an existing .vimsst file with one condition that gets replicated or from scratch. Search Sets can be added programatically using their id and name (acquired beforehand). This workflow does not provide a solution for templates that use custom selections.
- Automatically create colour maps by element properties (Distinct, Random or Gradient colours)
- The online web app can be used to generate heat maps or distinct colours views base on items property values. The starting template is required to infer the property conditions type (string, number...), the operator (hide, unhide, isolate, colour...).
- Appereance templates can also be created from scratch using existing Search Sets
