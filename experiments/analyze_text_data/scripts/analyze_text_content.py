# -*- coding: utf-8 -*-
# Python Script to process PDF files and text from crawled website
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
from string import digits
import string

import utilities as util
import glot_lid as glid


def main(input_path, script_mode):

	# ===========================================
	# Morisien - ANALYZE INTERMEDIATE - Dataset to one file with sentences and info about them in console
	# ===========================================
	def intermediate_analyze_sentences(data_path, filenames, intermediate_path, datasetname):
		
		logging.debug(f'Analyzing dataset: {datasetname}')
		text_content = []

		# Collect all text from all files into "text_content"
		for filename in filenames:
			current_file_in = data_path+filename
			current_file_name = util.get_basename(current_file_in)
			current_file_out = intermediate_path+datasetname
			text_lines = util.read_text_file(current_file_in)
			text_content.append(text_lines)

		# Create directory if not existing
		util.create_directory(intermediate_path)

		# Combine all lines into one
		one_line = ""

		for document in text_content:
			for line in document:
				one_line = one_line + line

		#logging.debug(f'one_line[0:100] = {one_line[0:100]}')

		#one_line_split = one_line.split('.')
		#logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

		# Replace all line breaks with a space
		one_line_no_breaks = re.sub('\n', ' ', one_line)
			
			# Replace all special characters with a space
			#one_line_no_special = re.sub('[^A-Za-z0-9]+', ' ', one_line_no_breaks)

			# Replace all single characters with a space
			#one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
		
		# Replace all double spaces with one space
		one_line_no_doublespace = re.sub(' +', ' ', one_line_no_breaks)
		
		# Remove leading and trailing spaces
		one_line_stripped = one_line_no_doublespace.strip()

		# Make all text lower case
		#one_line_no_uppercase = one_line_stripped.lower()

		# Split into sentences based on '.'
		sentences = one_line_stripped.split(".")
		number_of_sentences = len(sentences)

		# Remove duplicates
		sentences_unique = set(sentences)
		number_of_sentences_unique = len(sentences_unique)
		logging.debug(f'Number of sentences: {number_of_sentences}')
		logging.debug(f'Number of unique sentences: {number_of_sentences_unique}')

		# Turn set back into list
		sentences_unique = list(sentences_unique)

		# About sentence lengths
		sum_of_list = 0
		for i in range(len(sentences_unique)):
			sum_of_list += len(sentences_unique[i])
		average = sum_of_list / len(sentences_unique)
		logging.debug(f'Average length of unique sentences: {average}') 


		# Writing unique sentences to "Datasetname".txt
		with open(current_file_out+'.txt', "w") as outfile:
			for sentence in sentences_unique[1:]:
				outfile.write(sentence.strip()+'.'+'\n')


	# ===========================================
	# Morisien - ANALYZE OUTPUT - Dataset to words and save info about those
	# ===========================================
	def intermediate_analyze_words(data_path, filename, output_path):
		print("Analyzing 02")

		current_file_in = data_path+filename
		current_file_name = util.get_basename(current_file_in)
		current_file_out = output_path+current_file_name
		text_lines = util.read_text_file(current_file_in)

		# Create directory if not existing
		util.create_directory(output_path)

		# Combine all lines into one
		one_line = ""

		for line in text_lines:
			# Also remove all line breaks
			one_line = one_line + line

		#logging.debug(f'one_line[0:100] = {one_line[0:100]}')

		#one_line_split = one_line.split('.')
		#logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

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
		with open(current_file_out+'.json', "w") as outfile:
			outfile.write(json_object)

	# ===========================================
	# Morisien - ANALYZE COMBINE
	# ===========================================
	def combine_all_data(dataset01, dataset02, dataset03, out_path):

		# Create directory if not existing
		util.create_directory(out_path)

		dataset_path_01 = dataset01[0]
		dataset_files_01 = dataset01[1]

		dataset_path_02 = dataset02[0]
		dataset_files_02 = dataset02[1]

		dataset_path_03 = dataset03[0]
		dataset_files_03 = dataset03[1]

		text_content = []
		# Collect all text from all files into "text_content"
		for filename in dataset_files_01:
			current_file_in = dataset_path_01+filename
			text_lines = util.read_text_file(current_file_in)
			text_content.append(text_lines)

		for filename in dataset_files_02:
			current_file_in = dataset_path_02+filename
			text_lines = util.read_text_file(current_file_in)
			text_content.append(text_lines)

		for filename in dataset_files_03:
			current_file_in = dataset_path_03+filename
			text_lines = util.read_text_file(current_file_in)
			text_content.append(text_lines)

		# Combine all lines into one
		one_line = ""

		for document in text_content:
			for line in document:
				one_line = one_line + line

		#logging.debug(f'one_line[0:100] = {one_line[0:100]}')

		#one_line_split = one_line.split('.')
		#logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

		# Replace all line breaks with a space
		one_line_no_breaks = re.sub('\n', ' ', one_line)
			
			# Replace all special characters with a space
			#one_line_no_special = re.sub('[^A-Za-z0-9]+', ' ', one_line_no_breaks)

			# Replace all single characters with a space
			#one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
		
		# Replace all double spaces with one space
		one_line_no_doublespace = re.sub(' +', ' ', one_line_no_breaks)
		
		# Remove leading and trailing spaces
		one_line_stripped = one_line_no_doublespace.strip()

		# Make all text lower case
		#one_line_no_uppercase = one_line_stripped.lower()

		# Split into sentences based on '.'
		sentences = one_line_stripped.split(".")
		number_of_sentences = len(sentences)

		# Remove duplicates
		sentences_unique = set(sentences)
		number_of_sentences_unique = len(sentences_unique)
		logging.debug(f'Number of sentences: {number_of_sentences}')
		logging.debug(f'Number of unique sentences: {number_of_sentences_unique}')

		# Turn set back into list
		sentences_unique = list(sentences_unique)

		# About sentence lengths
		sum_of_list = 0
		for i in range(len(sentences_unique)):
			sum_of_list += len(sentences_unique[i])
		average = sum_of_list / len(sentences_unique)
		logging.debug(f'Average length of unique sentences: {average}') 


		# Writing unique sentences to "Datasetname".txt
		with open(out_path+'all_text_sentences.txt', "w") as outfile:
			for sentence in sentences_unique[1:]:
				outfile.write(sentence.strip()+'.'+'\n')

	# ===========================================
	# Morisien - ANALYZE IDENTIFY LANGUAGES
	# ===========================================
	def identify_languages(input_path, filename, model_path):

		model_cache_directory = model_path
		language_id_model = glid.main(model_cache_directory)

		current_file_in = input_path+filename
		text_lines_linebreak = util.read_text_file(current_file_in)
		
		text_lines = []
		for line in text_lines_linebreak:
			text_lines.append(line.replace('\n', ''))

		text_lines_predictions = []
		for line in text_lines:
			prediction = language_id_model.predict(line)
			text_lines_predictions.append(prediction)
		
		text_lines_and_predictions = [] # List of lists, where each contained list holds 2 elements: sentence and predictions
		#text_lines_and_predictions = zip(text_lines[0:10], text_lines_predictions)
		for index in range(len(text_lines_predictions)):
			text_lines_and_predictions.append([text_lines[index], text_lines_predictions[index]])


		# Writing language identification predictions to "language_identifications".txt
		with open(input_path+'language_identifications.txt', "w") as outfile:
			for sentence_and_prediction in text_lines_and_predictions:
				outfile.write(str(sentence_and_prediction)+'\n')


	# ===========================================
	# Morisien - SORT OUT ACCORDING TO IDENTIFIED LANGUAGES
	# ===========================================
	def sort_by_identified_languages(input_path, filename, confidence_threshold_1, confidence_threshold_2, confidence_threshold_3):

		current_file_in = input_path+filename
		text_lines_identified = util.read_text_file(current_file_in)
		# Format of lines looks like:
		# line = ['Mo b iznes dan douk.', (('__label__rcf_Latn',), array([0.3120684]))]
		#
		# Lang_Label → line.split('__label__')[1].split(',),')[0][:-1]
		# line.split('__label__')[1] → rcf_Latn',), array([0.3120684]))]
		# line.split('__label__')[1].split(',),')[0][:-1] → rcf_Latn
		#
		# Lang_Sentence → line.split(', ((__label__')[0][2:-1]
		# line.split(', ((__label__')[0] → ['Mo b iznes dan douk.'
		# line.split(', ((__label__')[0][2:-1] → Mo b iznes dan douk.
		#
		# Prediction_Confidence → line.split(',), array([')[1].split(',),')[0][:-1]
		# line.split(',), array([')[1] → 0.3120684]))]
		# line.split(',), array([')[1].split(']))]')[0][:-1] → 0.3120684


		sent_lang_dict_english_conf_1 = []
		sent_lang_dict_english_conf_2 = []
		sent_lang_dict_english_conf_3 = []
		sent_lang_dict_english_conf_4 = []
		sent_lang_dict_morisien_conf_1 = []
		sent_lang_dict_morisien_conf_2 = []
		sent_lang_dict_morisien_conf_3 = []
		sent_lang_dict_morisien_conf_4 = []
		sent_lang_dict_other_conf_1 = []
		sent_lang_dict_other_conf_2 = []
		sent_lang_dict_other_conf_3 = []
		sent_lang_dict_other_conf_4 = []
		sent_lang_counts = {}

		for line in text_lines_identified:
			#print(line)
			#print(type(line)) # → string
			lang_label = line.split('__label__')[1].split(',),')[0][:-1]
			
			# Confidence about made prediction
			prediction_confidence = float(line.split(',), array([')[1].split(']))]')[0][:-1])
			
			# Based on predicted languages, check for confidence and then count occurences
			if lang_label == "mfe_Latn":
				# Highest confidence threshold (90%)
				if prediction_confidence > confidence_threshold_1:
					sent_lang_dict_morisien_conf_1.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_1}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_1}'] = 1
					elif lang_label+f'-{confidence_threshold_1}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_1}'] += 1
				# Second-highest confidence threshold (80%)
				elif prediction_confidence > confidence_threshold_2:
					sent_lang_dict_morisien_conf_2.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_2}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_2}'] = 1
					elif lang_label+f'-{confidence_threshold_2}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_2}'] += 1
				# Thirds-highest confidence threshold (70%)
				elif prediction_confidence > confidence_threshold_3:
					sent_lang_dict_morisien_conf_3.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_3}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_3}'] = 1
					elif lang_label+f'-{confidence_threshold_3}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_3}'] += 1
				# No required confidence threshold - Everything with this label gets in
				else:
					sent_lang_dict_morisien_conf_4.append(line)
					# Count occurences based on confidence
					if lang_label+f'-less-{confidence_threshold_3}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-less-{confidence_threshold_3}'] = 1
					elif lang_label+f'-less-{confidence_threshold_3}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-less-{confidence_threshold_3}'] += 1
			elif lang_label == "eng_Latn":
				# Highest confidence threshold (90%)
				if prediction_confidence > confidence_threshold_1:
					sent_lang_dict_english_conf_1.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_1}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_1}'] = 1
					elif lang_label+f'-{confidence_threshold_1}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_1}'] += 1
				# Second-highest confidence threshold (80%)
				elif prediction_confidence > confidence_threshold_2:
					sent_lang_dict_english_conf_2.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_2}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_2}'] = 1
					elif lang_label+f'-{confidence_threshold_2}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_2}'] += 1
				# Thirds-highest confidence threshold (70%)
				elif prediction_confidence > confidence_threshold_3:
					sent_lang_dict_english_conf_3.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_3}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_3}'] = 1
					elif lang_label+f'-{confidence_threshold_3}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_3}'] += 1
				# No required confidence threshold - Everything with this label gets in
				else:
					sent_lang_dict_english_conf_4.append(line)
					# Count occurences based on confidence
					if lang_label+f'-less-{confidence_threshold_3}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-less-{confidence_threshold_3}'] = 1
					elif lang_label+f'-less-{confidence_threshold_3}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-less-{confidence_threshold_3}'] += 1
			else:
				# Highest confidence threshold (90%)
				if prediction_confidence > confidence_threshold_1:
					sent_lang_dict_other_conf_1.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_1}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_1}'] = 1
					elif lang_label+f'-{confidence_threshold_1}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_1}'] += 1
				# Second-highest confidence threshold (80%)
				elif prediction_confidence > confidence_threshold_2:
					sent_lang_dict_other_conf_2.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_2}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_2}'] = 1
					elif lang_label+f'-{confidence_threshold_2}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_2}'] += 1
				# Thirds-highest confidence threshold (70%)
				elif prediction_confidence > confidence_threshold_3:
					sent_lang_dict_other_conf_3.append(line)
					# Count occurences based on confidence
					if lang_label+f'-{confidence_threshold_3}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_3}'] = 1
					elif lang_label+f'-{confidence_threshold_3}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-{confidence_threshold_3}'] += 1
				# No required confidence threshold - Everything with this label gets in
				else:
					sent_lang_dict_other_conf_4.append(line)
					# Count occurences based on confidence
					if lang_label+f'-less-{confidence_threshold_3}' not in sent_lang_counts:
						sent_lang_counts[lang_label+f'-less-{confidence_threshold_3}'] = 1
					elif lang_label+f'-less-{confidence_threshold_3}' in sent_lang_counts:
						sent_lang_counts[lang_label+f'-less-{confidence_threshold_3}'] += 1

		# Sort dictionary 
		sorted_sent_lang_counts = sorted(sent_lang_counts.items(), key=lambda x:x[1], reverse = True)
		sorted_sent_lang_counts_dict = dict(sorted_sent_lang_counts)

		# Serializing json
		json_object = json.dumps(sorted_sent_lang_counts_dict, indent=4)
		
		# Writing to sample.json
		with open(input_path+'predicted_language_counts.json', "w") as outfile:
			outfile.write(json_object)

		# Writing sentences to file, according to their predictions
		with open(input_path+f'predicted_english-{confidence_threshold_1}.txt', "w") as outfile:
			for sentence in sent_lang_dict_english_conf_1:
				outfile.write(sentence)
		with open(input_path+f'predicted_english-{confidence_threshold_2}.txt', "w") as outfile:
			for sentence in sent_lang_dict_english_conf_2:
				outfile.write(sentence)
		with open(input_path+f'predicted_english-{confidence_threshold_3}.txt', "w") as outfile:
			for sentence in sent_lang_dict_english_conf_3:
				outfile.write(sentence)
		with open(input_path+f'predicted_english-less-{confidence_threshold_3}.txt', "w") as outfile:
			for sentence in sent_lang_dict_english_conf_4:
				outfile.write(sentence)

		with open(input_path+f'predicted_morisien-{confidence_threshold_1}.txt', "w") as outfile:
			for sentence in sent_lang_dict_morisien_conf_1:
				outfile.write(sentence)
		with open(input_path+f'predicted_morisien-{confidence_threshold_2}.txt', "w") as outfile:
			for sentence in sent_lang_dict_morisien_conf_2:
				outfile.write(sentence)
		with open(input_path+f'predicted_morisien-{confidence_threshold_3}.txt', "w") as outfile:
			for sentence in sent_lang_dict_morisien_conf_3:
				outfile.write(sentence)
		with open(input_path+f'predicted_morisien-less-{confidence_threshold_3}.txt', "w") as outfile:
			for sentence in sent_lang_dict_morisien_conf_4:
				outfile.write(sentence)

		with open(input_path+f'predicted_other-{confidence_threshold_1}.txt', "w") as outfile:
			for sentence in sent_lang_dict_other_conf_1:
				outfile.write(sentence)
		with open(input_path+f'predicted_other-{confidence_threshold_2}.txt', "w") as outfile:
			for sentence in sent_lang_dict_other_conf_2:
				outfile.write(sentence)
		with open(input_path+f'predicted_other-{confidence_threshold_3}.txt', "w") as outfile:
			for sentence in sent_lang_dict_other_conf_3:
				outfile.write(sentence)
		with open(input_path+f'predicted_other-less-{confidence_threshold_3}.txt', "w") as outfile:
			for sentence in sent_lang_dict_other_conf_4:
				outfile.write(sentence)


	# ===========================================
	# Morisien - SORT OUT ACCORDING TO IDENTIFIED LANGUAGES
	# ===========================================
	def sort_sentences_alphabetically(input_path, filename, language):

		current_file_in = input_path+filename
		text_lines_identified = util.read_text_file(current_file_in)

		text_lines_cleaned = []
		for line in text_lines_identified:
			# Split to only get the sentence without the prediction
			text_line = line.split(', ((')[0]

			# Replace all special characters with a space
			line_no_special = re.sub('[^A-Za-z0-9]+', ' ', text_line)

			# Replace all single characters with a space
			line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', line_no_special)
		
			# Replace all double spaces with one space
			line_no_doublespace = re.sub(' +', ' ', line_no_singlechar)
		
			# Remove leading and trailing spaces
			line_stripped = line_no_doublespace.strip()

			# Make all text lower case
			line_no_uppercase = line_stripped.lower()

			# Remove leading numbers from string
			line_no_leading_number = line_no_uppercase.lstrip(digits)

			# Remove leading and trailing spaces (that might get introduced by removing digits)
			line_no_leading_number_stripped = line_no_leading_number.strip()

			# Remove leading numbers from line of text
			if line_no_leading_number_stripped.split(' ')[0].isdigit():
				# If first word in text line is purely made of digits, slice it off.
				line_cleaned = line_no_leading_number_stripped[len(line_no_leading_number_stripped.split(' ')[0]):]
				#print(line_no_leading_number_stripped.split(' ')[0]) # Debug which digits are being removed
			else:
				line_cleaned = line_no_leading_number_stripped

			text_lines_cleaned.append(line_cleaned)

		# Sort list alphabetically
		text_lines_sorted = sorted(text_lines_cleaned)

		with open(input_path+f'sorted_{language}.txt', "w") as outfile:
			for sentence in text_lines_sorted:
				outfile.write(sentence+'\n')



	# ===========================================
	# Morisien - SORT OUT ACCORDING TO IDENTIFIED LANGUAGES
	# ===========================================
	def split_files_up(input_path, filename, language):

		current_file_in = input_path+filename
		text_lines_identified = util.read_text_file(current_file_in)

		if language == "Morisien":
			with open(input_path+f'sorted_{language}_01.txt', "w") as outfile:
				for sentence in text_lines_identified[0:10000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_02.txt', "w") as outfile:
				for sentence in text_lines_identified[10000:20000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_03.txt', "w") as outfile:
				for sentence in text_lines_identified[20000:30000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_04.txt', "w") as outfile:
				for sentence in text_lines_identified[30000:40000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_05.txt', "w") as outfile:
				for sentence in text_lines_identified[40000:50000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_06.txt', "w") as outfile:
				for sentence in text_lines_identified[50000:60000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_07.txt', "w") as outfile:
				for sentence in text_lines_identified[60000:70000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_08.txt', "w") as outfile:
				for sentence in text_lines_identified[70000:80000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_09.txt', "w") as outfile:
				for sentence in text_lines_identified[80000:90000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_10.txt', "w") as outfile:
				for sentence in text_lines_identified[90000:95136]:
					outfile.write(sentence)
		elif language == "English":
			with open(input_path+f'sorted_{language}_01.txt', "w") as outfile:
				for sentence in text_lines_identified[0:10000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_02.txt', "w") as outfile:
				for sentence in text_lines_identified[10000:14681]:
					outfile.write(sentence)
		elif language == "Other":
			with open(input_path+f'sorted_{language}_01.txt', "w") as outfile:
				for sentence in text_lines_identified[0:10000]:
					outfile.write(sentence)
			with open(input_path+f'sorted_{language}_02.txt', "w") as outfile:
				for sentence in text_lines_identified[10000:20846]:
					outfile.write(sentence)

	# ===========================================
	# Morisien - ANALYZE RESULT
	# ===========================================
	def result_analyze(data_path, filename, result_path):
		print("Analyzing 03")

		# Create directory if not existing
		util.create_directory(result_path)

	# Dataset paths: /BoukieBanane/ & /DabreMT/ & /SeedNLLB/
	input_boukiebanane = input_path+"input/BoukieBanane/"
	input_dabremt = input_path+"input/DabreMT/"
	input_seednllb = input_path+"input/SeedNLLB/"

	filenames_boukiebanane = ['DataSet-boukiebanabe.txt','liv-e_01.txt','liv-e_02.txt','liv-e_03.txt','liv-e_04.txt','liv-e_05.txt','liv-e_06.txt','liv-e_07.txt','liv-e_08.txt','liv-e_09.txt','liv-e_10.txt','liv-e_11.txt','liv-e_12.txt','liv-e_13.txt','liv-e_14.txt','liv-e_15.txt','liv-e_16.txt','BILENGISM-OTANTIK-PA-PAR-PA.txt','LITERESI-BILENG-PREVOK.txt','LIV_E_APRENOV19.txt','MERSI-BONDIE-EBOOK.txt','OUPANISHAD-livE.txt','UNIVERSAL-BILINGUAL-FUNCTIONAL-LITERACY.txt']
	filenames_dabremt = ['sentences_mor.mor'] # 'sentences_eng.mor','sentences_mor.eng'
	filenames_dabremt_all = ['sentences_eng.mor','sentences_mor.eng','sentences_mor.mor','words_eng.mor','words_mor.eng','words_mor.mor']
	filenames_seednllb = ['eng_Latn']

	intermediate_boukiebanane = input_path+"intermediate/BoukieBanane/"
	intermediate_dabremt = input_path+"intermediate/DabreMT/"
	intermediate_seednllb = input_path+"intermediate/SeedNLLB/"

	output_boukiebanane = input_path+"output/BoukieBanane/"
	output_dabremt = input_path+"output/DabreMT/"
	output_seednllb = input_path+"output/SeedNLLB/"

	result_boukiebanane = input_path+"result/BoukieBanane/"
	result_dabremt = input_path+"result/DabreMT/"
	result_seednllb = input_path+"result/SeedNLLB/"
	
	model_cache_dir_for_glot_lid = input_path+"models/"

	all_data_combined_path = input_path+"combined/"
	# Confidence thresholds for sorting sentences to corresponding language
	confidence_threshold_1 = 0.9
	confidence_threshold_2 = 0.8
	confidence_threshold_3 = 0.7
	
	#
	# All data
	# 
	#combine_all_data([input_boukiebanane, filenames_boukiebanane],[input_dabremt, filenames_dabremt],[input_seednllb, filenames_seednllb],all_data_combined_path)
	#TAKES LONG #identify_languages(all_data_combined_path, "all_text_sentences.txt", model_cache_dir_for_glot_lid)
	# Sort identified sentences
	if "sortIdentified" in script_mode:
		filename = "language_identifications.txt"
		sort_by_identified_languages(all_data_combined_path, filename, confidence_threshold_1, confidence_threshold_2, confidence_threshold_3 )

	# Sort predicted sentences
	if "sortAlphabetically" in script_mode:
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_morisien-{confidence_threshold_1}.txt', f'Morisien-{confidence_threshold_1}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_morisien-{confidence_threshold_2}.txt', f'Morisien-{confidence_threshold_2}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_morisien-{confidence_threshold_3}.txt', f'Morisien-{confidence_threshold_3}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_morisien-less-{confidence_threshold_3}.txt', f'Morisien-less-{confidence_threshold_3}')

		sort_sentences_alphabetically(all_data_combined_path, f'predicted_english-{confidence_threshold_1}.txt', f'English-{confidence_threshold_1}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_english-{confidence_threshold_2}.txt', f'English-{confidence_threshold_2}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_english-{confidence_threshold_3}.txt', f'English-{confidence_threshold_3}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_english-less-{confidence_threshold_3}.txt', f'English-less-{confidence_threshold_3}')

		sort_sentences_alphabetically(all_data_combined_path, f'predicted_other-{confidence_threshold_1}.txt', f'Other-{confidence_threshold_1}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_other-{confidence_threshold_2}.txt', f'Other-{confidence_threshold_2}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_other-{confidence_threshold_3}.txt', f'Other-{confidence_threshold_3}')
		sort_sentences_alphabetically(all_data_combined_path, f'predicted_other-less-{confidence_threshold_3}.txt', f'Other-less-{confidence_threshold_3}')



	# Split large files into smaller files
	#split_files_up(all_data_combined_path, "sorted_Morisien.txt", "Morisien")
	#split_files_up(all_data_combined_path, "sorted_English.txt", "English")
	#split_files_up(all_data_combined_path, "sorted_Other.txt", "Other")


	# 
	# BoukieBanane data
	# 
	"""
	intermediate_analyze_sentences(input_boukiebanane, filenames_boukiebanane, intermediate_boukiebanane, "BoukieBanane")
	for filename in filenames_boukiebanane:
		intermediate_analyze_words(input_boukiebanane, filename, output_boukiebanane)
		result_analyze(input_boukiebanane, filename, result_boukiebanane)
	"""
	
	# 
	# DabreMT data
	# 
	"""
	intermediate_analyze_sentences(input_dabremt, filenames_dabremt, intermediate_dabremt, "DabreMT")
	for filename in filenames_dabremt:
		intermediate_analyze_words(input_dabremt, filename, output_dabremt)
		result_analyze(input_dabremt, filename, result_dabremt)
	"""
		
	# 
	# SeedNLLB data
	# 
	"""
	intermediate_analyze_sentences(input_seednllb, filenames_seednllb, intermediate_seednllb, "SeedNLLB")
	for filename in filenames_seednllb:
		intermediate_analyze_words(input_seednllb, filename, output_seednllb)
		result_analyze(input_seednllb, filename, result_seednllb)
	"""
	

	#intermediate_analyze(input_boukiebanane, filename, intermediate_boukiebanane)
	#output_analyze(input_boukiebanane, filename, output_boukiebanane)
	#result_analyze(input_boukiebanane, filename, result_boukiebanane)

"""
# For each file in the directory
for filename in os.listdir(transform_path_pdf):
	# Combine the directory path with the filename
	txt_file = os.path.join(transform_path_pdf, filename)
	
	
	# Checking if it is a file
	if os.path.isfile(txt_file):
		
		current_file = util.get_basename(txt_file)
		logging.debug(f'  Pre-Sort: {txt_file}')
		
		text_lines = util.read_text_file(txt_file)
		
		# Printing number of lines in txt file 
		logging.debug(f'    Number of Lines: {len(text_lines)}')

		with open(transform_path_txt+f'{current_file}.txt', 'w') as file:
			for line in text_lines:
				file.write(line)
"""



	
	
