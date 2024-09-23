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

# Get and print the current working directory
#current_working_directory = os.getcwd()
#print(current_working_directory)

#path_morisien = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Morisien/"
path_morisien = "./../data/Morisien/"

# 2022DabreMorisienMT 
###############################################################################
# Morisien
##########

# Read data from json file (jsonl is just a "long json")
#with open(path_morisien+'Datasets/2022DabreMorisienMT/cr/cr_train.jsonl', 'r') as file:
    #data = json.load(file) # ERROR: json.decoder.JSONDecodeError: Extra data: line 2 column 1 (char 28)
    # → Having multiple objects that are not wrapped in an array is not valid JSON.

# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
input_lines = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/cr/cr_train.jsonl', 'r', encoding='utf-8')]

# The input is on the format:   {"input": "morisien_text_here", "target": ""}
# Extracting the Morisien texts and store them in data
data = [input_lines[index]['input']
        for index in range(len(input_lines))]

# Removing the first (empty) element from the list of text lines
data.pop(0)

#print(data[3]) # Debugging to check content

# Write the Morisien text into a new file
with open(path_morisien+'Temp/2022DabreMorisienMT-mor.txt', 'w') as file:
    for line in data:
        file.write(line)
        file.write('\n')

# Morisien - English 
####################
# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
input_lines_dev = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
input_lines_test = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
input_lines_train = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
input_lines = input_lines_dev + input_lines_test + input_lines_train

# The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
# Extracting the English and Morisien texts and store them in data
data_eng_mor = [input_lines[index]['input']
        for index in range(len(input_lines))]
data_mor_eng = [input_lines[index]['target']
        for index in range(len(input_lines))]

# Write the English and Morisien text into a new file
with open(path_morisien+'Temp/2022DabreMorisienMT-eng_mor.txt', 'w') as file:
    for line in data_eng_mor:
        file.write(line)
        file.write('\n')
with open(path_morisien+'Temp/2022DabreMorisienMT-mor_eng.txt', 'w') as file:
    for line in data_mor_eng:
        file.write(line)
        file.write('\n')

# Morisien - French
###################
# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
input_lines_dev = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
input_lines_test = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
input_lines_train = [json.loads(line)
        for line in open(path_morisien+'Datasets/2022DabreMorisienMT/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
input_lines = input_lines_dev + input_lines_test + input_lines_train

# The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
# Extracting the English and Morisien texts and store them in data
data_fra_mor = [input_lines[index]['input']
        for index in range(len(input_lines))]
data_mor_fra = [input_lines[index]['target']
        for index in range(len(input_lines))]

# Write the English and Morisien text into a new file
with open(path_morisien+'Temp/2022DabreMorisienMT-fra_mor.txt', 'w') as file:
    for line in data_fra_mor:
        file.write(line)
        file.write('\n')
with open(path_morisien+'Temp/2022DabreMorisienMT-mor_fra.txt', 'w') as file:
    for line in data_mor_fra:
        file.write(line)
        file.write('\n')

