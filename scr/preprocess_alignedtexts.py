# -*- coding: utf-8 -*-
# Python Script for finding aligned text lines in collected data
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

python preprocess_alignedtexts.py
"""

import os

"""

"""
def main():
	preprocessed_path = './../data/data_preprocessed/'
	normalized_path = './../data/data_normalized/' #TODO
	info_path = './../data/data_info/' #TODO
	aligned_path = './../data/data_aligned/' #TODO


	file_eng_mor = normalized_path + '2022DabreMorisienMT-eng_mor.txt' 		# English Text (normalized & sorted)
	file_eng_kur = normalized_path + '2022AhmadiInterdialect-eng_kur.txt'	# English Text (normalized & sorted)
	file_eng_multi30_n = normalized_path + '2016ElliottMulti30k-eng.txt'	# English Text (normalized & sorted)
	file_eng_phoMT_n = normalized_path + '2021DoanPhoMT-eng_vie.txt'		# English Text (normalized & sorted)
	file_eng_NgoSyn_n = normalized_path + '2022NgoSynthetic-eng_vie.txt'	# English Text (normalized & sorted)

	info_mor_kur = info_path + 'aligned_mor_eng_kur.txt'					# Marking aligned text lines (mor-kur)
	info_mor_all = info_path + 'aligned_mor_all.txt'						# Marking aligned text lines (mor-all)

	aligned_mor_all = aligned_path + 'aligned_mor_all.txt'					# Aligned text lines (mor-all)
	aligned_mor_all_unique = aligned_path + 'aligned_mor_all_unique.txt'	# Aligned text lines (mor-all)

	# If the directory does not already exist
	if not os.path.exists(info_path):
		# Create the directory
		os.makedirs(info_path)
	if not os.path.exists(aligned_path):
		# Create the directory
		os.makedirs(aligned_path)

	"""
	Load the main text for comparison between languages
	"""
	def load_main_text(text_file_path, marker, number):
		# Read English text (aligned to Morisien)
		input_lines_mor = []

		# Read the .txt file line-by-line
		with open(text_file_path) as file:
			input_lines_mor = file.readlines()

		# Marking each line for the main file
		line_marker_main = []
		line_marker_main.append(str(number))
		
		# Mark "mor" for each line
		for line in input_lines_mor:
			line_marker_main.append(marker)

		return input_lines_mor, line_marker_main


	"""
	Load a new text and look for alignable texts
	"""
	def compare_new_text(file_eng_new, marker, number, main_text):
		# Read English text (aligned to Kurmanji)
		input_lines_new = []

		# Read the .txt file line-by-line
		with open(file_eng_new) as file:
			input_lines_new = file.readlines()

		# Marking each line for the new file
		line_marker_new = []
		line_marker_new.append(str(number))

		# For each line of text in the main-file
		for line_main in main_text:
			# Check if current line_main is also in the new text file
			if line_main in input_lines_new:
				# Mark "kur" for each line found in main text
				line_marker_new.append(marker)
				print("Found something! :D ")
			else:
				line_marker_new.append("")

		return line_marker_new
	
	"""
	Counting the number of lines in a textfile
	Each line could be a word, a sentence, a paragraph, a document, ...
	"""
	def count_text_lines(textfile):
		# Read the .txt file line-by-line
		with open(textfile, 'r') as file:
			number_of_lines = sum(1 for line in file)

		return number_of_lines
		
	# (Sanity-Check:) 
	# Counting textlines of the language files and add as first line in info file
	mor_lines = count_text_lines(file_eng_mor)
	#print("Number of lines mor: "+str(mor_lines))
	kur_lines = count_text_lines(file_eng_kur)
	#print("Number of lines kur: "+str(kur_lines))
	multi30_lines = count_text_lines(file_eng_multi30_n)
	#print("Number of lines multi30: "+str(multi30_lines))
	phoMT_lines = count_text_lines(file_eng_phoMT_n)
	#print("Number of lines phoMT: "+str(phoMT_lines))
	NgoSyn_lines = count_text_lines(file_eng_NgoSyn_n)
	#print("Number of lines NgoSyn: "+str(NgoSyn_lines))
	

	"""
	Load "main_text" for a language first and then compare with the new_texts of other languages
	in order to find duplicate sentences, which can then be used to align the languages.
	"""
	def find_aligned_sentence():
		# Storing the main text lines for comparison between languages
		main_text = [] # TODO: Find a more elegant solution that carrying the main_text around like this...

		# First load main text file and initial marker
		main_text, main_marker = load_main_text(file_eng_mor, "mor", mor_lines)

		# Load other text files and compare with main file
		new_marker_01 = compare_new_text(file_eng_kur, "kur", kur_lines, main_text)
		new_marker_02 = compare_new_text(file_eng_multi30_n, "multi30", multi30_lines, main_text)
		new_marker_03 = compare_new_text(file_eng_phoMT_n, "phoMT", phoMT_lines, main_text)
		new_marker_04 = compare_new_text(file_eng_NgoSyn_n, "NgoSyn", NgoSyn_lines, main_text)

		# Combine markers
		line_marker = list(zip(main_marker, new_marker_01, new_marker_02, new_marker_03, new_marker_04))

		# Write marker to info file
		with open(info_mor_all, 'w') as file:
			for line in line_marker:
				file.write(str(line)+'\n')

	# WARNING! Takes a bit of time, especially for the larger files (phoMT and NgoSyn)
	#find_aligned_sentence()


	def extract_aligned_sentences():

		info_lines = []
		# Based on the info_file: info_mor_all
		#   ('mor=21810', 	'kur=1796', 	'multi30=29000', 	'phoMT=2977999', 	'NgoSyn=231004')
		#   ('mor', 		'', 			'', 				'', 				'')
		#   ('mor', 		'kur', 			'', 				'', 				'')
		#   ('mor', 		'', 			'', 				'phoMT', 			'')
		#   ('mor', 		'', 			'', 				'phoMT', 			'')
		#   ('mor', 		'', 			'', 				'phoMT', 			'NgoSyn')
		# ...
		with open(info_mor_all) as info_file:
			info_lines = info_file.readlines()

		# Read English text (aligned to Morisien)
		input_lines_mor = []

		# Read the .txt file line-by-line
		with open(file_eng_mor) as file:
			input_lines_mor = file.readlines()

		# Collect aligned sentences (English)
		aligned_text_kur = []
		aligned_text_multi30 = []
		aligned_text_phoMT = []
		aligned_text_NgoSyn = []

		# Ignoring the first line, which contains the number of lines from the original text files
		# And simultaneously going through the main_text lines one-by-one
		for info, line in zip(info_lines[1:], input_lines_mor):
			#print(str(info))
			if "kur" in info:
				aligned_text_kur.append(line)
				#print("Found kur " + line)
			if "multi30" in info:
				aligned_text_multi30.append(line)
				#print("Found multi30 " + line)
			if "phoMT" in info:
				aligned_text_phoMT.append(line)
				#print("Found phoMT " + line)
			if "NgoSyn" in info:
				aligned_text_NgoSyn.append(line)
				#print("Found NgoSyn " + line)
		
		#print(aligned_text_kur)
		#print(aligned_text_multi30)
		#print(aligned_text_phoMT)
		#print(aligned_text_NgoSyn)

		# Write aligned text to file for each language/data
		with open(aligned_path+'aligned_mor_kur.txt', 'w') as file:
			for line in aligned_text_kur:
				file.write(str(line))
		with open(aligned_path+'aligned_mor_multi30.txt', 'w') as file:
			for line in aligned_text_multi30:
				file.write(str(line))
		with open(aligned_path+'aligned_mor_phoMT.txt', 'w') as file:
			for line in aligned_text_phoMT:
				file.write(str(line))
		with open(aligned_path+'aligned_mor_NgoSyn.txt', 'w') as file:
			for line in aligned_text_NgoSyn:
				file.write(str(line))


	#extract_aligned_sentences()


	"""
	Quick fix to remove duplicate text lines in aligned info_file
	Following: https://stackoverflow.com/questions/66986719/how-to-remove-duplicate-lines-of-a-huge-file-in-python
	Working with hash to be able to handle even very large files
	"""
	def remove_duplicate_lines(input_file, output_file):
		seen = set()
		with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
			for line in fin:
				h = hash(line)
				if h not in seen:
					fout.write(line)
					seen.add(h)

	remove_duplicate_lines(aligned_mor_all, aligned_mor_all_unique)


if __name__ == "__main__":
	main()