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
import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 

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

# We ignore the arabic script for now, since it is barely used for Kurmanji and usually Sorani (Central Kurdish)
# Read the .txt file line-by-line
#with open(path_kurmanji+'Datasets/2023AhmadiSouthernCorpus/KurdishLID/datasets/NorthernKurdish-arab_train.txt') as file:
#    input_lines = file.readlines()
# Write the text into a new file
#with open(path_kurmanji+'Temp/2023AhmadiSouthernCorpus-kur_arab.txt', 'w') as file:
#    for line in input_lines:
#        file.write(line)

# 2022AhmadiInterdialect 
###############################################################################
# Kurmanji - English
####################
input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.KMR_no_tag.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2022AhmadiInterdialect-kur_eng.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.ENG_no_tag.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2022AhmadiInterdialect-eng_kur.txt', 'w') as file:
    for line in input_lines:
        file.write(line)


# 2020AhmadiKurdishTokenization
###############################################################################
# Kurmanji
##########
input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2020AhmadiKurdishTokenization/KurdishTokenization/data/kmr_sentences.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2020AhmadiKurdishTokenization-kur.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# 2013EsmailiPewan
###############################################################################
# Kurmanji
##########
read_files = glob.glob(path_kurmanji+'Datasets/2013EsmailiPewan/pewan/Pewan/Corpora/Kurmanji/docs2/'+"*.txt")

# Write the text into a new file
with open(path_kurmanji+'Temp/2013EsmailiPewan-kur.txt', 'w') as outfile:
    for file in read_files:
        with open(file, "r") as infile:
            outfile.write(infile.read())
            outfile.write('\n')

# 2020FatihkurtKurdishTwitter
###############################################################################
# Kurmanji
##########
input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2020FatihkurtKurdishTwitter/kurdish-twitter-data/Kurmanji/twitter-data.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2020FatihkurtKurdishTwitter-kur.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# 2020LeichtfußFreeDict
###############################################################################
# German-Kurmanji
#################
input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2020LeichtfußFreeDict/fd-dictionaries/deu-kur/Deutsch-Kurdî.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2020LeichtfußFreeDict-ger_kur.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# Kurmanji-German
#################
# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2020LeichtfußFreeDict/fd-dictionaries/kur-deu/kur-deu.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2020LeichtfußFreeDict-kur_ger.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# Kurmanji-English
##################
# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2020LeichtfußFreeDict/fd-dictionaries/kur-eng/kur-eng.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2020LeichtfußFreeDict-kur_eng.txt', 'w') as file:
    for line in input_lines:
        file.write(line)

# Kurmanji-Turkish
##################
# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2020LeichtfußFreeDict/fd-dictionaries/kur-tur/kur-tur.txt') as file:
    input_lines = file.readlines()

# Write the text into a new file
with open(path_kurmanji+'Temp/2020LeichtfußFreeDict-kur_tur.txt', 'w') as file:
    for line in input_lines:
        file.write(line)


# 2001HaigKurdishNewspaper
###############################################################################
# Kurmanji
##########
input_lines = []

# Read the .txt file line-by-line
with open(path_kurmanji+'Datasets/2001HaigKurdishNewspaper/ccknt.txt', encoding="latin-1") as file:
    input_lines = file.readlines()#.decode("latin-1")

# Write the text into a new file
with open(path_kurmanji+'Temp/2001HaigKurdishNewspaper-kur.txt', 'w', encoding="UTF-8") as file:
    for line in input_lines:
        file.write(line)#.encode("UTF-8")
