import random
import requests
from PIL import Image
from io import BytesIO
import csv

with open('br_imagebackgrounds_second.csv') as file:
    contents = file.readlines()
contents = [content.replace('"', '').strip() for content in contents]
whites = 0
contents = [content.split(",") for content in contents]

for content in contents:
    if content[2] == "white_background":
        whites += 1
print(whites)

imcount = 0
while imcount < 200:
    choice = random.randint(1,len(contents))
    if contents[choice][2]=="white_background":
       imcount+=1
       img_data = requests.get(contents[choice][1]).content
       with open('white_background/white_background' + str(imcount) + '.jpg', 'wb') as handler:
           handler.write(img_data)
imcount = 0
while imcount < 300:
    choice = random.randint(1,len(contents))
    if contents[choice][2]=="no_background":
       imcount+=1
       img_data = requests.get(contents[choice][1]).content
       with open('no_background/no_background' + str(imcount) + '.jpg', 'wb') as handler:
           handler.write(img_data)
