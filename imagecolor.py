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
