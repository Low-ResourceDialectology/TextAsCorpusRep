# -*- coding: utf-8 -*-
# Python Script for transforming collected text data from datasets into normalized structure
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 
import json
import logging
import os
import shutil
import sys

import utilities as util


def main(languages, inputPath, outputPath, dataset_list):

	logging.info(f'  Transforming datasets')
	logging.debug(f'languages: {languages}')
	logging.debug(f'inputPath: {inputPath}')
	logging.debug(f'outputPath: {outputPath}')
	logging.debug(f'dataset_list: {dataset_list}')

	# ===========================================
	# Morisien 
	# ===========================================
	if '2022DabreMorisienMT' in dataset_list:

		download_path = inputPath + '2022DabreMorisienMT/'
		transform_path = outputPath + '2022DabreMorisienMT/'

		# Create directory if not existing
		util.create_directory(transform_path)

		# Monolingual
		# Read data from json file (jsonl is just a "long json")
		# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
		input_lines = [json.loads(line)
			for line in open(download_path+'data/cr/cr_train.jsonl', 'r', encoding='utf-8')]

		# The input is on the format:   {"input": "morisien_text_here", "target": ""}
		# Extracting the Morisien texts and store them in data
		data = [input_lines[index]['input']
			for index in range(len(input_lines))]

		# Removing the first (empty) element from the list of text lines
		data.pop(0)

		#print(data[3]) # Debugging to check content

		# Write the Morisien text into a new file
		with open(transform_path+'mor.mor', 'w') as file:
			for line in data:
				file.write(line)
				file.write('\n')

		# Bilingual - English
		# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
		#input_lines_dev = [json.loads(line)
		#		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
		#input_lines_test = [json.loads(line)
		#		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
		input_lines_train = [json.loads(line)
				for line in open(download_path+'data/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
		#input_lines = input_lines_dev + input_lines_test + input_lines_train
		input_lines = input_lines_train

		# The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
		# Extracting the English and Morisien texts and store them in data
		data_eng_mor = [input_lines[index]['input']
				for index in range(len(input_lines))]
		data_mor_eng = [input_lines[index]['target']
				for index in range(len(input_lines))]

		# Write the English text (aligned with Morisien) into a new file
		with open(transform_path+'mor.eng', 'w') as file:
			for line in data_eng_mor:
				file.write(line)
				file.write('\n')
		# Write the Morisien text (aligned with English) into a new file
		with open(transform_path+'eng.mor', 'w') as file:
			for line in data_mor_eng:
				file.write(line)
				file.write('\n')

		# Bilingual - Fench 
		# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
		#input_lines_dev = [json.loads(line)
		#		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
		#input_lines_test = [json.loads(line)
		#		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
		input_lines_train = [json.loads(line)
				for line in open(download_path+'data/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
		#input_lines = input_lines_dev + input_lines_test + input_lines_train
		input_lines = input_lines_train

		# The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
		# Extracting the English and Morisien texts and store them in data
		data_fra_mor = [input_lines[index]['input']
				for index in range(len(input_lines))]
		data_mor_fra = [input_lines[index]['target']
				for index in range(len(input_lines))]

		# Write the French text (aligned with Morisien) into a new file
		with open(transform_path+'mor.fra', 'w') as file:
			for line in data_fra_mor:
				file.write(line)
				file.write('\n')
		# Write the Morisien text (aligned with French) into a new file
		with open(transform_path+'fra.mor', 'w') as file:
			for line in data_mor_fra:
				file.write(line)
				file.write('\n')

	# ===========================================
	# Kurmanji
	# ===========================================
	if '2022AhmadiInterdialect' in dataset_list:
	
		download_path = inputPath + '2022AhmadiInterdialect/'
		transform_path = outputPath + '2022AhmadiInterdialect/'

		# Create directory if not existing
		util.create_directory(transform_path)

		input_lines = []

		# Read the .txt file line-by-line
		with open(download_path+'InterdialectCorpus/KMR-ENG/KMR-ENG.KMR_no_tag.txt') as file:
			input_lines = file.readlines()

		# Write the text into a new file
		with open(transform_path+'eng.kmr', 'w') as file:
			for line in input_lines:
				file.write(line)

		input_lines = []

		# Read the .txt file line-by-line
		with open(download_path+'InterdialectCorpus/KMR-ENG/KMR-ENG.ENG_no_tag.txt') as file:
			input_lines = file.readlines()

		# Write the text into a new file
		with open(transform_path+'kmr.eng', 'w') as file:
			for line in input_lines:
				file.write(line)

	# ===========================================
	# Vietnamese
	# ===========================================
	if '2017LuongNMT' in dataset_list:

		download_path = inputPath + '2017LuongNMT/'
		transform_path = outputPath + '2017LuongNMT/'

		# Create directory if not existing
		util.create_directory(transform_path)
		
		input_lines = []

		# Read the .txt file line-by-line
		with open(download_path+'nmt/nmt/testdata/iwslt15.tst2013.100.en') as file:
			input_lines = file.readlines()

		# Write the text into a new file
		with open(transform_path+'vie.eng', 'w') as file:
			for line in input_lines:
				file.write(line)

		input_lines = []

		# Read the .txt file line-by-line
		with open(download_path+'nmt/nmt/testdata/iwslt15.tst2013.100.vi') as file:
			input_lines = file.readlines()

		# Write the text into a new file
		with open(transform_path+'eng.vie', 'w') as file:
			for line in input_lines:
				file.write(line)
