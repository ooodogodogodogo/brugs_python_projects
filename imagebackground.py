import requests
from PIL import Image
from io import BytesIO
import csv
import sys

# Function to check if all pixels in a region are white
def is_region_white(image, left, top, right, bottom):
    rgbvals = image.convert('RGB')
    #print(rgbvals.getpixel((left,top)))
    for i in range(left, right):
        for j in range(top,bottom):
            r, g , b = rgbvals.getpixel((i,j))
            if  r<250 or g <250 or b <250:
                return False
    return True
# Download the image from the URL

try:
    response = requests.get(sys.argv[1])
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
        print("white_background")
    else:
        print("no_background")

except Exception:
    print("error")


