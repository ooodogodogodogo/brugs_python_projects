import requests
from PIL import Image
from io import BytesIO
import csv
import time
import numpy as np
from scipy.spatial import distance
import time
import sys
import json
import os
# Function to check if all pixels in a region are white
minimumpercentage = int(sys.argv[2])
maxcolor = int(sys.argv[3])
with open(os.path.join(os.path.realpath(os.path.dirname(__file__))  ,'br_colors.csv')) as file:
    contents = file.readlines()
contents = [content.replace('"', '').strip() for content in contents]
contents = contents[1:]
contents = [content.split(",") for content in contents]
results = []
integers = []
hexmap = {}
idmap = {}
for colors in contents:
    hexcode = colors[3]
    integers.append((int(hexcode[1:3],16),int(hexcode[3:5],16),int(hexcode[5:7],16)))
    hexmap[colors[1]] = colors[3]
    idmap[colors[1]] = colors[0]
palette = np.array(integers)
#print(palette)

# get some image

im = Image.open(requests.get(sys.argv[1], stream=True).raw)
pixels = list(im.getdata())


width, height = im.size
pixels=list(im.resize((width//4,height//4),Image.LANCZOS).getdata())

#print(integers[0])


y = distance.cdist(pixels,integers,'cityblock')
minindexs = np.argmin(y, axis=1)
unique, counts = np.unique(minindexs, return_counts=True)
countdict = dict(zip(unique, counts))
colorpctg= {contents[key][1]:(value/len(pixels)) for (key,value) in countdict.items()}
maincolors = {k:v for (k,v) in colorpctg.items() if v > minimumpercentage/100}
maincolors =  dict(sorted(maincolors.items(), key=lambda x:x[1],reverse= True))

while maxcolor < len(maincolors):
    maincolors.popitem()

responselist = [dict([("id", idmap[key]),("hexcode",hexmap[key]) ,("colorname",key) ,("percentage",value)]) for (key,value) in maincolors.items()]
print(json.dumps(responselist))

"""
for content in contents:
    url = content[1]
    try:
        response = requests.get(url)
        print(content[1])
        # Load the image and get its dimensions
        image = Image.open(BytesIO(response.content))
        width, height = image.size

        # Check the four corners of the image
        p = 3
        top_left = is_region_white(image, 0, 0, p, p)
        top_right = is_region_white(image, width - p, 0, width, p)
        bottom_left = is_region_white(image, 0, height - p, p, height)
        bottom_right = is_region_white(image, width - p, height - p, width, height)
        # Print the results
        if (top_left and top_right) or (bottom_left and bottom_right):
            results.append([content[0], content[1],"white_background"])
        else:
            results.append([content[0], content[1],"no_background"])
            Break
    except Exception:
        pass

with open('br_imagebackgrounds.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    for result in results:
        data = [result[0], result[1],result[2]]
        writer.writerow(data)
"""