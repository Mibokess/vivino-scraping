'''
Usage: python scrape_imagelinks.py --url <url of the race album you want to scrape>
'''

# import the necessary packages
from selenium import webdriver
import datetime
import time
import argparse
import os
from pip._vendor import requests

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

time.sleep(2)


dir_name = 'wine'
if not os.path.exists(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print ("[INFO] Creation of the directory {} failed".format(os.path.abspath(dir_name)))
    else:
        print ("[INFO] Successfully created the directory {} ".format(os.path.abspath(dir_name)))

rating_tags = driver.find_elements_by_tag_name('div')
rating_tag = None

for potential_rating_tag in rating_tags:
    if ("vivinoRatingWide__averageValue--1zL_5" in potential_rating_tag.get_attribute("class")):
        rating_tag = potential_rating_tag
        break


print(rating_tag.text)

i = 0
current_rating = 1000
for j in range(1000):
    try:
        link_tag = rating_tag.find_element_by_xpath('../../../../../div/div/a/div/img')
    except:
        continue
    
    response = requests.get(link_tag.get_attribute('src'))

    if (float(rating_tag.text) < current_rating):
        current_rating = float(rating_tag.text)
        os.mkdir("wine/" + rating_tag.text)

    file = open("wine/" + rating_tag.text + "/" + str(i) + ".png", "wb")
    file.write(response.content)
    file.close()    

    i = i + 1
    
    rating_tag = rating_tag.find_element_by_xpath('../../../../../..')

    driver.execute_script("""
        var element = document.querySelector('.explorerCard__explorerCard--3Q7_0');
        console.log(element)
        if (element)
            element.parentNode.removeChild(element);
        """) 

    rating_tag = rating_tag.find_element_by_class_name('vivinoRatingWide__averageValue--1zL_5')