
from selenium import webdriver
import time
import csv
import webbrowser
from webdriver_manager.chrome import ChromeDriverManager


csvpath = "/Users/murat/Downloads/br_videos.csv"
with open( csvpath, newline='') as csvfile:
    data = list(csv.reader(csvfile))

data = data [1:]
interval = 10
print(data[3])

# Create a new Chrome browser window
driver = webdriver.Chrome(ChromeDriverManager().install())

for i in range(100):
    # reload the tab to show the latest changes
    driver.get(data[i][0])
    print(i)
    time.sleep(interval)
