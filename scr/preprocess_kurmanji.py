# Python Script for preprocessing of text data of target languages
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import json
import os
from bs4 import BeautifulSoup
from lxml import etree

path_kurmanji = "./../data/Kurmanji/"

# 2023AhmadiSouthernCorpus 
###############################################################################
# Kurmanji
##########
input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2023AhmadiSouthernCorpus/KurdishLID/datasets/NorthernKurdish-latn_train.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2023AhmadiSouthernCorpus-kur.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2023AhmadiSouthernCorpus/KurdishLID/datasets/NorthernKurdish-arab_train.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2023AhmadiSouthernCorpus-kur_arab.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# 2022AhmadiInterdialect 
###############################################################################
input_lines = []

# Okay... Reading xml files that are as basic as this one and which also contain duplicated ids is a pain in the butt!
"""
tree = etree.parse(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.kmr.eng.xml')
for graph in tree.xpath('//p'):
    print(graph.xpath('@id')[0])

root = tree.getroot()

topic = root.find(".//*[@id='1:2']").text
print(topic)
"""

"""
# Reading the data inside the xml
# file to a variable under the name 
# data
with open(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.kmr.eng.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag 
# `unique`
b_unique = Bs_data.find_all('unique')
 
print(b_unique)
 
print(value)
"""


# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.kmr.eng.xml') as file:
    input_lines = file.readlines()

# input_lines has this format: 
# Start of file:       <p id="1"><s id="1:1">Hunermendên Kurd wê ji bo yekîtiya neteweyî li Stockholmê konserekê li dar bixin.</s>	<s id="1:1">A joint concert of numerous Kurdish musicians took place in Stockholm.</s>
# And each line contains 2 sentences like this:         <s id="1:2">Hunermendên Kurd ji bo tevkariyê li pêkhatina yekîtiya neteweyî bikin, wê konserekê li dar bixin.</s>	<s id="1:2">The artists want to contribute to Kurdish national unity.</s>

# Cleaning up the lines to extract the Kurmanji and English texts
#for each line in input_lines:
    


data = input_lines

# Write the text into a new file
with open(path_kurmanji+'Temp/2022AhmadiInterdialect-kur-eng.txt', 'w') as file:
    for line in data:
        file.write(line)



# 2023AhmadiSouthernCorpus 
###############################################################################


# 2023AhmadiSouthernCorpus 
###############################################################################
