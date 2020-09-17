'''
Usage: python scrape_imagelinks.py --url <url of the race album you want to scrape>
'''

# import the necessary packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import time
import argparse
import os
from pip._vendor import requests
import asyncio

#Define the argument parser to read in the URL
parser = argparse.ArgumentParser()
parser.add_argument('-url', '--url', help='URL to the online repository of images')
args = vars(parser.parse_args())
url = args['url']
url = "https://www.vivino.com/explore?"

# Extract the album name
#album_name = url.split('/')[-2]

# Define Chrome options to open the window in maximized mode
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Initialize the Chrome webdriver and open the URL
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

time.sleep(1)

driver.find_element(By.ID, "1").click()
driver.find_element(By.CSS_SELECTOR, ".responsiveDropdownMenu__label--3fijz").click()
driver.find_element(By.ID, "desc__price").click()

time.sleep(5)

dir_name = 'wine'
if not os.path.exists(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print ("[INFO] Creation of the directory {} failed".format(os.path.abspath(dir_name)))
    else:
        print ("[INFO] Successfully created the directory {} ".format(os.path.abspath(dir_name)))

for i in range(50, 34, -1):
    dir_name = "wine/" + str((i / 10.0))

    try:
        os.mkdir(dir_name)
    except:
        pass

async def save_image(rating, link, i):
    try:
        response = requests.get(link)
    except:
        time.sleep(1)
    
    try:
        file = open("wine/" + rating + "/" + str(i) + ".png", "wb")
        file.write(response.content)
        file.close()    
    except:
        pass

tasks = []

def process_element(i):
    worked = False
    while (not worked):
        try:
            rating_tag = driver.find_element_by_class_name('vivinoRatingWide__averageValue--1zL_5')
            link_tag = driver.find_element_by_xpath('//div/div/a/div/img')

            worked = True
        except:
            pass

    return asyncio.create_task(save_image(rating_tag.text, link_tag.get_attribute('src'), i))

async def gatherTasks(number, stepSize):
    tasks = []

    for j in range(number):
        print(str(j))
        tasks.append(process_element(j))
        
        worked = False
        while (not worked):
            try:
                driver.execute_script("""
                    var element = document.querySelector('.explorerCard__explorerCard--3Q7_0');
                    console.log(element)
                    if (element) element.parentNode.removeChild(element);
                    """) 
                worked = True
                time.sleep(0.01)
            except:
                time.sleep(1)

        if (j != 0 and j % stepSize == 0):
            for l in range(stepSize):
                await tasks[l]
            
            tasks = []
            time.sleep(0.5)

asyncio.run(gatherTasks(27000, 20))