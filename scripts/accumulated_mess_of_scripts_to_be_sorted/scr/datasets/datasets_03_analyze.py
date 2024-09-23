# -*- coding: utf-8 -*-
# Python Script for exploring collected text data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 
import json
import logging
import os
import re
import shutil
import sys

from PyPDF2 import PdfReader 
import utilities as util

# Explore Text Data #
#####################

"""
Main Script
"""
def main(languages, input_path, output_path, dataset_list):

	download_path = input_path+'01_download/'
	transform_path = output_path+'02_transform/'
	analyze_path = output_path+'03_analyze/'
	sort_path = output_path+'04_sort/'
	clean_path = output_path+'05_clean/'

	analyze_path_all = analyze_path + 'all/'
	# Create directory if not existing
	util.create_directory(analyze_path_all)


	def analyze_morisien_compare():

		with open(analyze_path_all+'all_boukie_banane.json', 'r') as f:
			data_boukiebanane = json.load(f)

		with open(analyze_path_all+'all_dabreMT.json', 'r') as f:
			data_dabre = json.load(f)

		# Boukie Banane
		boukie_but_not_dabre = []

		for key in data_boukiebanane.keys():
			if not key in data_dabre:
				boukie_but_not_dabre.append(key)

		with open(analyze_path_all+'diff_boukie_but_not_dabre.json', "w") as outfile:
			for word in boukie_but_not_dabre:
				outfile.write(word)
				outfile.write('\n')

		# DabreMT
		dabre_but_not_boukie = []

		for key in data_dabre.keys():
			if not key in data_boukiebanane:
				dabre_but_not_boukie.append(key)

		with open(analyze_path_all+'diff_dabre_but_not_boukie.json', "w") as outfile:
			for word in dabre_but_not_boukie:
				outfile.write(word)
				outfile.write('\n')


		# DabreMT AND Boukie Banane
		dabre_and_boukie = []

		for key in data_dabre.keys():
			if key in data_boukiebanane:
				dabre_and_boukie.append(key)

		with open(analyze_path_all+'diff_dabre_and_boukie.json', "w") as outfile:
			for word in dabre_and_boukie:
				outfile.write(word)
				outfile.write('\n')


	analyze_morisien_compare()


	def analyze_morisien_dabre():

		# Combine all lines into one
		one_line = ""

		all_texts = []
		filenames = ['2022DabreMorisienMT/Monolingual/Words/mor.mor','2022DabreMorisienMT/Monolingual/Sentences/mor.mor','2022DabreMorisienMT/Bilingual/Words/eng.mor','2022DabreMorisienMT/Bilingual/Words/fra.mor','2022DabreMorisienMT/Bilingual/Sentences/eng.mor','2022DabreMorisienMT/Bilingual/Sentences/fra.mor']
		for filename in filenames:
			current_file_in = sort_path+filename
			text_lines = util.read_text_file(current_file_in)
			print(text_lines[0])
			for line in text_lines:
				# Also remove all line breaks
				one_line = one_line + line

		# Replace all line breaks with a space
		one_line_no_breaks = re.sub('\n', ' ', one_line)
		
		# Replace all special characters with a space
		one_line_no_special = re.sub('[^A-Za-z0-9]+', ' ', one_line_no_breaks)

		# Replace all single characters with a space
		one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
		
		# Replace all double spaces with one space
		one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
		
		# Remove leading and trailing spaces
		one_line_stripped = one_line_no_doublespace.strip()

		# Make all text lower case
		one_line_no_uppercase = one_line_stripped.lower()

		words = one_line_no_uppercase.split(" ")

		word_count = {}

		for word in words:
			if word not in word_count:
				word_count[word] = 1
			elif word in word_count:
				word_count[word] += 1
			
		#current_content.append(sentence)

		# Sort dictionary 
		sorted_word_count = sorted(word_count.items(), key=lambda x:x[1], reverse = True)
		sorted_word_count_dict = dict(sorted_word_count)

		# Serializing json
		json_object = json.dumps(sorted_word_count_dict, indent=4)
		
		# Writing to sample.json
		with open(analyze_path_all+'all_dabreMT.json', "w") as outfile:
			outfile.write(json_object)

		#with open(analyze_path_pdf+filename, 'w') as file:
		#	for count in word_count:
		#		file.write(str(count))
		#		file.write('\n')

	#analyze_morisien_dabre()




	def analyze_morisien_boukiebanane():

		# Combine all lines into one
		one_line = ""

		all_texts = []
		filenames = ['DataSet-boukiebanabe.txt','liv-e_01.txt','liv-e_02.txt','liv-e_03.txt','liv-e_04.txt','liv-e_05.txt','liv-e_06.txt','liv-e_07.txt','liv-e_08.txt','liv-e_09.txt','liv-e_10.txt','liv-e_11.txt','liv-e_12.txt','liv-e_13.txt','liv-e_14.txt','liv-e_15.txt','liv-e_16.txt','BILENGISM-OTANTIK-PA-PAR-PA.txt','LITERESI-BILENG-PREVOK.txt','LIV_E_APRENOV19.txt','MERSI-BONDIE-EBOOK.txt','OUPANISHAD-livE.txt','UNIVERSAL-BILINGUAL-FUNCTIONAL-LITERACY.txt']
		for filename in filenames:
			current_file_in = sort_path+'2023BoukieBanane_pdf/'+filename
			text_lines = util.read_text_file(current_file_in)

			for line in text_lines:
				# Also remove all line breaks
				one_line = one_line + line

		# Replace all line breaks with a space
		one_line_no_breaks = re.sub('\n', ' ', one_line)
		
		# Replace all special characters with a space
		one_line_no_special = re.sub('[^A-Za-z0-9]+', ' ', one_line_no_breaks)

		# Replace all single characters with a space
		one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
		
		# Replace all double spaces with one space
		one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
		
		# Remove leading and trailing spaces
		one_line_stripped = one_line_no_doublespace.strip()

		# Make all text lower case
		one_line_no_uppercase = one_line_stripped.lower()

		words = one_line_no_uppercase.split(" ")

		word_count = {}

		for word in words:
			if word not in word_count:
				word_count[word] = 1
			elif word in word_count:
				word_count[word] += 1
			
		#current_content.append(sentence)

		# Sort dictionary 
		sorted_word_count = sorted(word_count.items(), key=lambda x:x[1], reverse = True)
		sorted_word_count_dict = dict(sorted_word_count)

		# Serializing json
		json_object = json.dumps(sorted_word_count_dict, indent=4)
		
		# Writing to sample.json
		with open(analyze_path_all+'all_boukie_banane.json', "w") as outfile:
			outfile.write(json_object)

		#with open(analyze_path_pdf+filename, 'w') as file:
		#	for count in word_count:
		#		file.write(str(count))
		#		file.write('\n')

	#analyze_morisien_boukiebanane()



	def old_analyze_part():
		print("This is the explore_data script.")


		# Path to directory containing preprocessed data and output for explored data 
		#datasets_path = "./../data/data_datasets/"
		preprocessed_path = './../data/data_preprocessed/'
		explored_path = "./../data/data_explored/"

		# Dictionary holding the dataset entries to later be saved as json file
		dataset_json = {}
		dataset_counter = 0

		# Iterate over files in that directory
		for filename in os.listdir(preprocessed_path):
			filepath = os.path.join(preprocessed_path, filename)
			# Checking if it is a file
			if os.path.isfile(filepath):
				current_dataset = {
					"Name": "",
					"Source": "",
					"Target": "None",
					"Size": ""
					}

				#print(filepath) # Debugging

				# Split and get the name of the dataset from the name of the text file
				split_name = filepath.split("-")

				# Get the start of the file path
				#current_dataset["Name"] = split_name[0] # = "./../data/data_preprocessed/2021DoanPhoMT"

				# Take the last split to get the dataset name 
				current_dataset["Name"] = split_name[0].split("/")[4]
				
				# Split and get the end of the name of the text file
				#dataset_language = split_name[1] # = "kur.txt" or "eng_vie.txt" 
				
				# Split and get the language(s) identifier from the name of the text file
				dataset_language = split_name[1].split(".")[0]
				
				# If the length is 3, then this dataset is monolingual and there is only one language
				if len(dataset_language) == 3:
					#print("Length is 3 for: "+str(dataset_language)) # Debugging

					current_dataset["Source"] = dataset_language

				# If the length is not 3, then it is a multilingual dataset with a source- and a target-language
				else:
					#print("Length is not 3 for: "+str(dataset_language)) # Debugging

					dataset_languages = dataset_language.split("_")
					current_dataset["Source"] = dataset_languages[0]
					current_dataset["Target"] = dataset_languages[1]

				# Read the dataset textfile and count the number of lines
				with open(filepath, 'r') as fp:
					num_lines = sum(1 for line in fp)
					#print('Total lines:', num_lines) # Debugging
					current_dataset["Size"] = num_lines

				# Add the current dataset with the counter as key
				dataset_json[dataset_counter] = current_dataset

				# Serializing dictionary object into json 
				json_object = json.dumps(dataset_json, indent = 4)  

				# Increase the dataset_counter for the next file
				dataset_counter = dataset_counter + 1

		# TODO: Create directory prior to execution in order to create the json-file
		# Writing to sample.json
		with open(explored_path+'datasets_basic.json', "w") as outfile:
			outfile.write(json_object)



	# Alternative structure for forced layout #
	###########################################
	""""
	# Dictionary holding the dataset entries to later be saved as json file
	dataset_json = {
		"nodes": 
		[
			{
				"id": "Chinese",
				"group": "1"
			},
			{
				"id": "English",
				"group": "2"
			},
			{
				"id": "French",
				"group": "3"
			},
			{
				"id": "German",
				"group": "4"
			},
			{
				"id": "Kobani",
				"group": "5"
			},
			{
				"id": "Kurmanji",
				"group": "6"
			},
			{
				"id": "Morisien",
				"group": "7"
			},
			{
				"id": "Russian",
				"group": "8"
			},
			{
				"id": "Ukrainian",
				"group": "9"
			},
			{
				"id": "Vietnamese",
				"group": "10"
			}
		],
		"links":
		[

		]
	}
	dataset_counter = 0

	# Iterate over files in that directory
	for filename in os.listdir(preprocessed_path):
		filepath = os.path.join(preprocessed_path, filename)
		# Checking if it is a file
		if os.path.isfile(filepath):
			current_dataset_node = {
				"id": "",
				"group": ""
				}
			current_dataset_link = {
				"source": "",
				"target": "",
				"value":""
				}
			current_dataset_link_two = {
				"source": "",
				"target": "",
				"value":""
				}

			#print(filepath) # Debugging

			# Split and get the name of the dataset from the name of the text file
			split_name = filepath.split("-")
			current_dataset_node["id"] = split_name[0]
			
			# Split and get the end of the name of the text file
			#dataset_language = split_name[1] # = "kur.txt" or "eng_vie.txt" 
			
			# Split and get the language(s) identifier from the name of the text file
			dataset_language = split_name[1].split(".")[0]
			
			 # Read the dataset textfile and count the number of lines
			with open(filepath, 'r') as fp:
				num_lines = sum(1 for line in fp)
				#print('Total lines:', num_lines) # Debugging

			# If the length is 3, then this dataset is monolingual and there is only one language
			if len(dataset_language) == 3:
				#print("Length is 3 for: "+str(dataset_language)) # Debugging

				current_dataset_link["source"] = split_name[0]
				current_dataset_link["target"] = dataset_language
				current_dataset_link["value"] = num_lines

			# If the length is not 3, then it is a multilingual dataset with a source- and a target-language
			else:
				#print("Length is not 3 for: "+str(dataset_language)) # Debugging

				dataset_languages = dataset_language.split("_")

				current_dataset_link["source"] = split_name[0]
				current_dataset_link["target"] = dataset_languages[0]
				current_dataset_link["value"] = num_lines

				current_dataset_link_two["source"] = split_name[0]
				current_dataset_link_two["target"] = dataset_languages[1]
				current_dataset_link_two["value"] = num_lines

			dataset_json["nodes"]

			# Serializing dictionary object into json 
			json_object = json.dumps(dataset_json, indent = 4)  


	# Writing to sample.json
	with open(explored_path+'datasets_forced_layout.json', "w") as outfile:
		outfile.write(json_object)

	"""


if __name__ == "__main__":
	main()
