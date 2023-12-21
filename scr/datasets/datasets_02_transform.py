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
from datasets import load_dataset_builder
from datasets import load_dataset


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
		dataset_id = "prajdabre/KreolMorisienMT"

		# Create directory if not existing
		util.create_directory(transform_path)


		# Inspect metadata of datasets from huggingface without needing to download them:
		# TODO: Figure out while it seemingly still does download, even though it should not according to https://huggingface.co/docs/datasets/v1.11.0/loading_datasets.html
		#dataset_builder = load_dataset_builder(dataset_id)
		#print(dataset_builder.cache_dir)
		#print(dataset_builder.info.features)
		#print(dataset_builder.info.splits)
	
		# Load current dataset
		data_morisien = load_dataset(dataset_id, cache_dir=download_path, split='train')

		# Inspect dataset
		#data_morisien.split # AttributeError: 'DatasetDict' object has no attribute 'split'
		#data_morisien.description # AttributeError: 'DatasetDict' object has no attribute 'description'
		#data_morisien.citation
		#data_morisien.homepage
		#data_morisien.license
		#print(data_morisien.features['input'].num_classes) # AttributeError: 'Value' object has no attribute 'num_classes'
		#print(data_morisien.features['input'].names) # AttributeError: 'Value' object has no attribute 'names'
		#print(data_morisien.features['input'].str2int('equivalent'))
		#print(data_morisien.features['input'].str2int('not_equivalent'))
		"""
		print(len(data_morisien)) # → 85415
		print(data_morisien[0]) # → {'input': '', 'target': ''}
		print(data_morisien.shape) # → (85415, 2)
		print(data_morisien.num_columns) # → 2
		print(data_morisien.column_names) # → ['input', 'target']
		print(data_morisien.num_rows) # → 85415
		print(data_morisien.features) # → {'input': Value(dtype='string', id=None), 'target': Value(dtype='string', id=None)}
		"""

		print(len(data_morisien)) # → 85415
		
		""" This is python-logic! We need huggingface-logic!
		for dataset_row in data_morisien[0:45367]:
			with open(transform_path+'dabre_dataset.mor', 'w') as file:
				file.write(str(dataset_row))
				file.write('\n')
		for dataset_row in data_morisien[45367:68677]:
			with open(transform_path+'dabre_dataset.eng', 'w') as file:
				file.write(str(dataset_row))
				file.write('\n')
		for dataset_row in data_morisien[68677:-1]:
			with open(transform_path+'dabre_dataset.fra', 'w') as file:
				file.write(str(dataset_row))
				file.write('\n')
		"""

		data_morisien_mor = data_morisien[0:45366]
		#for dataset_row in data_morisien_mor:
		print(f'Length of Morisien: {len(data_morisien_mor)}')
		#print(transform_path+'mor.mor')
		with open(transform_path+'mor.mor', 'w') as file:
			mormor = data_morisien_mor['input']
			for line in mormor:
				file.write(line)
				file.write('\n')

		data_morisien_eng = data_morisien[45366:68676]
		print(f'Length of English: {len(data_morisien_eng)}')
		#print(transform_path+'mor.eng')
		with open(transform_path+'mor.eng', 'w') as file:
			engeng = data_morisien_eng['input']
			for line in engeng:
				file.write(line)
				file.write('\n')

		with open(transform_path+'eng.mor', 'w') as file:
			engmor = data_morisien_eng['target']
			for line in engmor:
				file.write(line)
				file.write('\n')

		data_morisien_fra = data_morisien[68676:]
		print(f'Length of French: {len(data_morisien_fra)}')
		with open(transform_path+'mor.fra', 'w') as file:
			frafra = data_morisien_fra['input']
			for line in frafra:
				file.write(line)
				file.write('\n')

		with open(transform_path+'fra.mor', 'w') as file:
			framor = data_morisien_fra['target']
			for line in framor:
				file.write(line)
				file.write('\n')


		
		# Write the Morisien text into a new file
		#with open(transform_path+'dabre_dataset', 'w') as file:
		#	for dataset_row in data_morisien:
		#		file.write(str(dataset_row))
		#		file.write('\n')
		

		#print(data_morisien)

		sys.exit()

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

		"""
		Backup due to loading with huggingface instead of downloading files directly now
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
		"""

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
