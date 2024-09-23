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

from PyPDF2 import PdfReader 
import utilities as util

"""
 
# Creating a pdf reader object 
reader = PdfReader('example.pdf') 
  
# Printing number of pages in pdf file 
print(len(reader.pages)) 
  
# Getting a specific page from the pdf file 
page = reader.pages[0] 
  
# Extracting text from page 
text = page.extract_text() 
print(text) 

"""


def main(languages, input_path, output_path, dataset_list):

	download_path = input_path+'01_download/'
	transform_path = output_path+'02_transform/'
	analyze_path = output_path+'03_analyze/'
	sort_path = output_path+'04_sort/'
	clean_path = output_path+'05_clean/'

	# ===========================================
	# Morisien - 2023BoukieBanane - PDFs
	# ===========================================
	def transform_pdf():
		transform_path_pdf = transform_path + '2023BoukieBanane_pdf/'

		# Create directory if not existing
		util.create_directory(transform_path_pdf)

		pdf_path = download_path + '2023BoukieBanane_pdf'

		# For each file in the directory
		for filename in os.listdir(pdf_path):
			# Combine the directory path with the filename
			pdf_file = os.path.join(pdf_path, filename)
			
			# Checking if it is a file
			if os.path.isfile(pdf_file):
				
				current_text = []
				current_file = util.get_basename(pdf_file)
				logging.debug(f'  Transform: {pdf_file}')
				# Creating a pdf reader object 
				reader = PdfReader(pdf_file) 
				# Printing number of pages in pdf file 
				logging.debug(f'    Number of Pages: {len(reader.pages)}')
				
				for page in reader.pages:
					text = page.extract_text()
					current_text.append(text)


				with open(transform_path_pdf+f'{current_file}.txt', 'w') as file:
					for line in current_text:
						file.write(line)
						file.write('\n')

	#transform_pdf()

	# ===========================================
	# Morisien - 2023BoukieBanane - TXT
	# ===========================================
	def transform_txt():
		transform_path_txt = transform_path + '2023BoukieBanane_txt/'
		
		# Create directory if not existing
		util.create_directory(transform_path_txt)

		txt_path = download_path + '2023BoukieBanane_txt'

		# For each file in the directory
		for filename in os.listdir(txt_path):
			# Combine the directory path with the filename
			txt_file = os.path.join(txt_path, filename)
			
			# Checking if it is a file
			if os.path.isfile(txt_file):
				
				current_file = util.get_basename(txt_file)
				logging.debug(f'  Transform: {txt_file}')
				
				text_lines = util.read_text_file(txt_file)
				
				# Printing number of lines in txt file 
				logging.debug(f'    Number of Lines: {len(text_lines)}')

				with open(transform_path_txt+f'{current_file}.txt', 'w') as file:
					for line in text_lines:
						file.write(line)

	#transform_txt()

	# ===========================================
	# Morisien - 2023BoukieBanane - TXT
	# ===========================================
	def presort_page_wise(filename):
		transform_path_pdf = transform_path + '2023BoukieBanane_pdf/'
		sort_path_pdf = sort_path + '2023BoukieBanane_pdf/'

		# Create directory if not existing
		util.create_directory(sort_path_pdf)


		current_file_in = transform_path_pdf+filename
		current_file_out = sort_path_pdf+filename
		text_lines = util.read_text_file(current_file_in)

	
		current_content = []
		current_page = []
		current_page_number = 1
		
		for line in text_lines:
			if line == str(current_page_number + 1)+" \n":
				current_page_number = current_page_number + 1
				#print("found next page")
				current_content.append(current_page)
				current_page = []
			else:
				textline = line.replace('\n', ' ')
				current_page.append(textline)

		with open(current_file_out, 'w') as file:
			for page in current_content:
				for line in page:
					file.write(line)
				file.write('\n')

	filename = 'liv-e_03.txt'
	#presort_page_wise(filename)

	# ===========================================
	# Morisien - PRESORT
	# ===========================================
	def presort(filename):
		transform_path_pdf = transform_path + '2023BoukieBanane_pdf/'
		sort_path_pdf = sort_path + '2023BoukieBanane_pdf/'

		# Create directory if not existing
		util.create_directory(sort_path_pdf)

		current_file_in = transform_path_pdf+filename
		current_file_out = sort_path_pdf+filename
		text_lines = util.read_text_file(current_file_in)

		#logging.debug(f'text_lines[0:10] = {text_lines[0:10]}')

		current_content = []

		# Combine all lines into one
		one_line = ""

		for line in text_lines:
			# Also remove all line breaks
			one_line = one_line + line.replace('\n', '')

		#logging.debug(f'one_line[0:100] = {one_line[0:100]}')

		one_line_split = one_line.split('.')
		#logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')


		for sentence in one_line_split:
			current_content.append(sentence)

		with open(current_file_out, 'w') as file:
			for line in one_line_split:
				if util.check_for_non_empty_string(line):
					file.write(line.strip().replace('  ',' '))
					file.write('\n')

	filenames = ['DataSet-boukiebanabe.txt','liv-e_01.txt','liv-e_02.txt','liv-e_03.txt','liv-e_04.txt','liv-e_05.txt','liv-e_06.txt','liv-e_07.txt','liv-e_08.txt','liv-e_09.txt','liv-e_10.txt','liv-e_11.txt','liv-e_12.txt','liv-e_13.txt','liv-e_14.txt','liv-e_15.txt','liv-e_16.txt','BILENGISM-OTANTIK-PA-PAR-PA.txt','LITERESI-BILENG-PREVOK.txt','LIV_E_APRENOV19.txt','MERSI-BONDIE-EBOOK.txt','OUPANISHAD-livE.txt','UNIVERSAL-BILINGUAL-FUNCTIONAL-LITERACY.txt']
	
	#for filename in filenames:
	#	presort(filename)
	#filename = 'liv-e_03.txt'
	#presort(filename)



	# ===========================================
	# Morisien - SORT
	# ===========================================
	def presort_analyze(filename):
		transform_path_pdf = transform_path + '2023BoukieBanane_pdf/'
		sort_path_pdf = sort_path + '2023BoukieBanane_pdf_cleanish/'
		analyze_path_pdf = analyze_path + '2023BoukieBanane_pdf/'

		# Create directory if not existing
		util.create_directory(sort_path_pdf)
		util.create_directory(analyze_path_pdf)

		current_file_in = transform_path_pdf+filename
		current_file_out = sort_path_pdf+filename
		text_lines = util.read_text_file(current_file_in)

		#logging.debug(f'text_lines[0:10] = {text_lines[0:10]}')

		current_content = []

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
		with open(analyze_path_pdf+filename+'.json', "w") as outfile:
			outfile.write(json_object)

		#with open(analyze_path_pdf+filename, 'w') as file:
		#	for count in word_count:
		#		file.write(str(count))
		#		file.write('\n')

	filenames = ['DataSet-boukiebanabe.txt','liv-e_01.txt','liv-e_02.txt','liv-e_03.txt','liv-e_04.txt','liv-e_05.txt','liv-e_06.txt','liv-e_07.txt','liv-e_08.txt','liv-e_09.txt','liv-e_10.txt','liv-e_11.txt','liv-e_12.txt','liv-e_13.txt','liv-e_14.txt','liv-e_15.txt','liv-e_16.txt','BILENGISM-OTANTIK-PA-PAR-PA.txt','LITERESI-BILENG-PREVOK.txt','LIV_E_APRENOV19.txt','MERSI-BONDIE-EBOOK.txt','OUPANISHAD-livE.txt','UNIVERSAL-BILINGUAL-FUNCTIONAL-LITERACY.txt']
	
	for filename in filenames:
		presort_analyze(filename)
	#filename = 'liv-e_03.txt'
	#presort_analyze(filename)


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



	
	
