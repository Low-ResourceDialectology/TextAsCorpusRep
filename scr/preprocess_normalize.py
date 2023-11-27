# -*- coding: utf-8 -*-
# Python Script for normalizing and sorting text in collected data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

"""
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/scr

source ./../../venvTextAsCorpusRep/bin/activate

python preprocess_normalize.py
"""

import os
import string # Transform strings (i.e. string.translate())
import re # Regular expressions (i.e. replace leading whitespaces)

"""

"""
def main():
	preprocessed_path = './../data/data_preprocessed/'
	normalized_path = './../data/data_normalized/' #TODO
	info_path = './../data/data_info/' #TODO

	file_mor_eng = preprocessed_path + '2022DabreMorisienMT-mor_eng.txt'	# Morisien Text
	file_eng_mor = preprocessed_path + '2022DabreMorisienMT-eng_mor.txt' 	# English Text
	file_mor_eng_n = normalized_path + '2022DabreMorisienMT-mor_eng.txt'	# Morisien Text (normalized & sorted) 
	file_eng_mor_n = normalized_path + '2022DabreMorisienMT-eng_mor.txt' 	# English Text (normalized & sorted)

	file_kur_eng = preprocessed_path + '2022AhmadiInterdialect-kur_eng.txt'	# Kurmanji Text
	file_eng_kur = preprocessed_path + '2022AhmadiInterdialect-eng_kur.txt'	# English Text
	file_kur_eng_n = normalized_path + '2022AhmadiInterdialect-kur_eng.txt'	# Kurmanji Text (normalized & sorted)
	file_eng_kur_n = normalized_path + '2022AhmadiInterdialect-eng_kur.txt'	# English Text (normalized & sorted)

	file_eng_multi30 = preprocessed_path + '2016ElliottMulti30k-eng.txt'	# English Text
	file_eng_multi30_n = normalized_path + '2016ElliottMulti30k-eng.txt'	# English Text (normalized & sorted)

	file_eng_phoMT = preprocessed_path + '2021DoanPhoMT-eng_vie.txt'	# English Text
	file_eng_phoMT_n = normalized_path + '2021DoanPhoMT-eng_vie.txt'	# English Text (normalized & sorted)

	file_eng_NgoSyn = preprocessed_path + '2022NgoSynthetic-eng_vie.txt'	# English Text
	file_eng_NgoSyn_n = normalized_path + '2022NgoSynthetic-eng_vie.txt'	# English Text (normalized & sorted)

	# If the directory does not already exist
	if not os.path.exists(normalized_path):
		# Create the directory
		os.makedirs(normalized_path)


	"""
	Helper function turning to lower-case
	"""
	#def string_to_lower_case(input_string):
	#	return input_string.lower()

	"""
	Normalization of text strings
	Following: https://spotintelligence.com/2023/01/25/text-normalization-techniques-nlp/
	 - To lower case
	 - Remove punctuation
	 - TODO: Remove stop words
	 - TODO: Stemming
	 - TODO: Lemmatization
	 - TODO: Tokenization
	 - TODO: Replace synonyms and abbreviation
	 - TODO: Remove numbers and symbols
	 - TODO: Remove any non-textual elements
	"""
	def normalize_text_file(input_file, output_file):
		# Read English text (aligned to target language)
		input_lines = []

		# Read the .txt file line-by-line
		with open(input_file) as file:
			input_lines = file.readlines()

		# Change each lino lower-case
		input_lines_lower = [line.lower() for line in input_lines]

		# Remove punctuation
		input_lines_punct = [line.translate(line.maketrans("","",string.punctuation)) for line in input_lines_lower]

		# Remove leading white space
		#input_lines_white = [line[1:] for line in input_lines_punct if line.startswith(' ')]
		input_lines_white = [re.sub('^\s','', line) for line in input_lines_punct] # ^ signals the start of line in regex and \s matches whitespace characters

		# Sort textlines alphabetically
		#input_lines_lower = sorted(input_lines)
		input_lines_white.sort()

		# Mark "mor" for each line in info file
		with open(output_file, 'w') as file:
			for line in input_lines_white:
				file.write(line)
	
	normalize_text_file(file_eng_kur, file_eng_kur_n)
	normalize_text_file(file_eng_mor, file_eng_mor_n)
	normalize_text_file(file_eng_multi30, file_eng_multi30_n)
	normalize_text_file(file_eng_phoMT, file_eng_phoMT_n)
	normalize_text_file(file_eng_NgoSyn, file_eng_NgoSyn_n)
  

if __name__ == "__main__":
	main()