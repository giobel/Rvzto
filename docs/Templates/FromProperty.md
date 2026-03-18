---
layout: default
title: AppTempl from Item Prop
parent: Appearance Templates
nav_order: 2
---

# Create Appearance Template from items property

Appearance Templates can be created by defining rules in the Appearence Profiler window (without using predefined Search Sets):

![](/Rvzto/assets/aprofiler.png)

The simplest approach is to create an Appearance Template first, then duplicate it while only modifying its property values.

The `Assembly Code` property in the template we have just created has only 3 possible values:

![](/Rvzto/assets/aprofilerValues.png)

Let's start by defining some helpers functions to generate the colours we will assign to the new property values:

```python
#MODULES
import colorsys
import zlib, blackboxprotobuf, random, copy


def color_to_int(r, g, b, a=255, order='RGBA'):
    if order.upper() == 'RGBA':
        return (r << 24) | (g << 16) | (b << 8) | a
    elif order.upper() == 'ARGB':
        return (a << 24) | (r << 16) | (g << 8) | b

def random_color_int():
    return color_to_int(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        255
    )

def distinct_colors_int(n):
    """Generate n visually distinct colors encoded as 32-bit integers."""
    colors = []
    for i in range(n):
        hue = i / n  # evenly spaced hues around the color wheel
        r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 1.0)  # bright and saturated
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        colors.append(color_to_int(r, g, b))
    return colors

def green_to_red(i, x):
    """
    Returns (R,G,B) color from green→yellow→red for i in 1..x.
    """
    if x <= 1:
        return (0, 255, 0)

    # Normalize position into 0..1
    t = (i - 1) / (x - 1)

    # First half: green → yellow (add red)
    if t <= 0.5:
        r = int(510 * t)       # 0 → 255
        g = 255               # stays max
    # Second half: yellow → red (remove green)
    else:
        r = 255               # stays max
        g = int(510 * (1 - t)) # 255 → 0

    return color_to_int(r, g, 0)
```

Then let's decode our appearance template. In this example we are only considering string or numbers for property values. The same principle applies for other data types (datetime, area, length...).

```python
path = 'TemplateTest.aptmpl'

with open(path, "rb") as f:
    data = f.read()
    print ('data read')
    #print (data)
    decdata, typeof = blackboxprotobuf.decode_message(data)
    # EXTRACT TEMPLATE PROPERTIES
    blob1 = decdata['4']['6']['3']
    #DECOMPRESS TEMPLATE PROPERTIES
    mes1 = zlib.decompress(blob1)
    # DECODE TEMPLATE PROPERTIES
    decItem, itemTypeOf = blackboxprotobuf.decode_message(mes1)
    template = decItem['1']
    templateName = decdata['4']['4'].decode()  # existing template name in the file
    tabName  = template['3']['2']['1']['2']['2']['2']['2']['2']['2'].decode() #we can use the same property tab name or assign a different one
    #tabName = "Item"
    propName = template['3']['2']['1']['2']['2']['2']['2']['3']['2'].decode() #we can use the same property name or assign a different one
    #propName = "Code Name"
    itemType = template['3']['2']['1']['2']['2']['2']['2']['4']
    propertyTypeValue = itemType[list(itemType.keys())[0]] #5 for string 1 for integer
    propertyValueKey = list(itemType.keys())[1]
    propertyType = 'string'

    if propertyTypeValue == 1:
        propertyType = 'integer'
    elif propertyTypeValue == 6:
        propertyType = 'integer'

    decItem['1'] = []
 
    decdata['4']['4'] = templateName.encode('utf-8')
    template['3']['2']['1']['2']['2']['2']['2']['2']['2'] = tabName.encode() 
    template['3']['2']['1']['2']['2']['2']['2']['3']['2'] = propName.encode() 
```

Then let's copy the rule and assign new values and save the encoded data back to .aptmpl:

```python
values = ['A1010100','B1010350','B10']
n_values = len(values)

    for i in range(0, n_values):
        entry = copy.deepcopy(template)
        entry['2'] = random_color_int() #or distinct or green2red
        match propertyType:
            case 'string':
                entry['3']['2']['1']['2']['2']['2']['2']['4'][propertyValueKey] = f"{values[i]}".encode('utf-8')
            case 'integer':
                entry['3']['2']['1']['2']['2']['2']['2']['4'][propertyValueKey] = int(values[i])  # NUMBER: 3
        decItem['1'].append(entry)
    
    compressed = zlib.compress(blackboxprotobuf.encode_message(decItem, itemTypeOf))
    decdata['4']['6']['3'] = compressed
    final = blackboxprotobuf.encode_message(decdata, typeof)

filename = 'output.aptmpl'
with open(filename, "wb") as f:
    f.write(final)
    print ("File saved")
```

If we import the template back into Revizto, the new rules are created and new colours have been automatically assigned:

![](/Rvzto/assets/aprofilerGenerated.png)
