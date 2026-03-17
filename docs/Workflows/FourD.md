---
layout: default
title: 4D Timeliner
parent: Workflows
nav_order: 5
---

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

### Application

Colour elements based on their start/end dates or construct/demolish actions.