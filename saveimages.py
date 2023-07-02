import random
import requests
from PIL import Image
from io import BytesIO
import csv
"""
def is_region_white(image, left, top, right, bottom):
    rgbvals = image.convert('RGB')
    #print(rgbvals.getpixel((left,top)))
    for i in range(left, right):
        for j in range(top,bottom):
            r, g , b = rgbvals.getpixel((i,j))
            print(r,g,b)
            if  r<250 or g <250 or b <250:
                return False
    return True

image = Image.open("no_background/no_background163.jpg")
width, height = image.size

# Check the four corners of the image
p = 3
top_left = is_region_white(image, 0, 0, p, p)
top_right = is_region_white(image, width - p, 0, width, p)
bottom_left = is_region_white(image, 0, height - p, p, height)
bottom_right = is_region_white(image, width - p, height - p, width, height)
# Print the results
if (top_left and top_right) or (bottom_left and bottom_right):
    print("white")
else:
    print("no")
"""
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
