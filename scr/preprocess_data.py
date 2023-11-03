# -*- coding: utf-8 -*-
# Python Script for preprocessing collected text data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

import os
import shutil

import json
from bs4 import BeautifulSoup
from lxml import etree
import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 

# Preprocessing Text Data #
###########################

"""
Preprocessing script
"""
def main(languages):
	print("This is the preprocess_data script.")

	target_languages = languages

	# Boolean variables for managing languages to be preprocessed
	zho_bool = False
	eng_bool = False
	fra_bool = False
	ger_bool = False
	kob_bool = False
	kur_bool = False
	mor_bool = False
	rus_bool = False
	ukr_bool = False
	vie_bool = False

	# Include languages based on provided "target_languages"
	if "zho" in target_languages:
		zho_bool = True
	if "eng" in target_languages:
		eng_bool = True
	if "fra" in target_languages:
		fra_bool = True
	if "ger" in target_languages:
		ger_bool = True
	if "kob" in target_languages:
		kob_bool = True
	if "kur" in target_languages:
		kur_bool = True
	if "mor" in target_languages:
		mor_bool = True
	if "rus" in target_languages:
		rus_bool = True
	if "ukr" in target_languages:
		ukr_bool = True
	if "vie" in target_languages:
		vie_bool = True

	# TODO: Causes an UnboundLocalError: local variable 'ukr_bool' referenced before assignment...
	#   But I do not understand why the above "ukr_bool" should not be readable (and assigned) in the code below....
	#   Temporary fix: Move this logic outside of its own function (less modular though :/ )
	# Modular execution based on language selection
	def language_selection():
		print("Selecting target languages.") # Debugging

		print("Debugging Booleans: "+str(ukr_bool)) # Debugging
		
		# Include languages based on provided "target_languages"
		if "zho" in target_languages:
			zho_bool = True
		if "eng" in target_languages:
			eng_bool = True
		if "fra" in target_languages:
			fra_bool = True
		if "ger" in target_languages:
			ger_bool = True
		if "kob" in target_languages:
			kob_bool = True
		if "kur" in target_languages:
			kur_bool = True
		if "mor" in target_languages:
			mor_bool = True
		if "rus" in target_languages:
			rus_bool = True
		if "ukr" in target_languages:
			ukr_bool = True
		if "vie" in target_languages:
			vie_bool = True

		print("Debugging Booleans: "+str(ukr_bool)) # Debugging
	

	# Preprocessing of collected text data
	def data_preprocessing():
		print("Start preprocessing for languages: "+str(languages)) # Debugging
		
		# Path to directory containing collected datasets and output directory
		datasets_path = "./../data/data_datasets/"
		preprocessed_path = './../data/data_preprocessed/'

		# If the directory does not already exist
		if not os.path.exists(preprocessed_path):
			# Create the directory
			os.makedirs(preprocessed_path)


		# Monolingual Datasets - Chinese #
		##################################
		if zho_bool:
			pass


		# Monolingual Datasets - English #
		##################################
		if eng_bool:
			pass


		# Monolingual Datasets - French #
		#################################
		if fra_bool:
			pass


		# Monolingual Datasets - German #
		#################################
		if ger_bool:
			pass


		# Monolingual Datasets - Kobani #
		#################################
		if kob_bool:
			pass


		# Monolingual Datasets - Kurmanji #
		###################################
		if kur_bool:

			# 2023AhmadiSouthernCorpus
			# We ignore the arabic script for now, since it is barely used for Kurmanji and usually Sorani (Central Kurdish)
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2023AhmadiSouthernCorpus/KurdishLID/datasets/NorthernKurdish-latn_train.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2023AhmadiSouthernCorpus-kur.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			# 2020AhmadiKurdishTokenization
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2020AhmadiKurdishTokenization/KurdishTokenization/data/kmr_sentences.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2020AhmadiKurdishTokenization-kur.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			# 2013EsmailiPewan
			read_files = glob.glob(datasets_path+'2013EsmailiPewan/pewan/Pewan/Corpora/Kurmanji/docs2/'+"*.txt")

			# Write the text into a new file
			with open(preprocessed_path+'2013EsmailiPewan-kur.txt', 'w') as outfile:
				for file in read_files:
					with open(file, "r") as infile:
						outfile.write(infile.read())
						outfile.write('\n')

			# 2020FatihkurtKurdishTwitter
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2020FatihkurtKurdishTwitter/kurdish-twitter-data/Kurmanji/twitter-data.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2020FatihkurtKurdishTwitter-kur.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			# 2001HaigKurdishNewspaper
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2001HaigKurdishNewspaper/ccknt.txt', encoding="latin-1") as file:
				input_lines = file.readlines()#.decode("latin-1")

			# Write the text into a new file
			with open(preprocessed_path+'2001HaigKurdishNewspaper-kur.txt', 'w', encoding="UTF-8") as file:
				for line in input_lines:
					file.write(line)#.encode("UTF-8")


		# Monolingual Datasets - Morisien #
		###################################
		if mor_bool:

			# 2022DabreMorisienMT 
			# Read data from json file (jsonl is just a "long json")
			# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
			input_lines = [json.loads(line)
					for line in open(datasets_path+'2022DabreMorisienMT/data/cr/cr_train.jsonl', 'r', encoding='utf-8')]

			# The input is on the format:   {"input": "morisien_text_here", "target": ""}
			# Extracting the Morisien texts and store them in data
			data = [input_lines[index]['input']
					for index in range(len(input_lines))]

			# Removing the first (empty) element from the list of text lines
			data.pop(0)

			#print(data[3]) # Debugging to check content

			# Write the Morisien text into a new file
			with open(preprocessed_path+'2022DabreMorisienMT-mor.txt', 'w') as file:
				for line in data:
					file.write(line)
					file.write('\n')


		# Monolingual Datasets - Russian #
		##################################
		if rus_bool:
			pass


		# Monolingual Datasets - Ukrainian #
		####################################
		if ukr_bool:
			pass
		

		# Monolingual Datasets - Vietnamese #
		#####################################
		if vie_bool:
			pass
		

		# Multilingual Datasets (Targets) #
		###################################

		# Kurmanji - English
		if kur_bool or eng_bool:

			# 2022AhmadiInterdialect 
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.KMR_no_tag.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022AhmadiInterdialect-kur_eng.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.ENG_no_tag.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022AhmadiInterdialect-eng_kur.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			# 2020LeichtfußFreeDict
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2020LeichtfußFreeDict/fd-dictionaries/kur-eng/kur-eng.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2020LeichtfußFreeDict-kur_eng.txt', 'w') as file:
				for line in input_lines:
					file.write(line)




		# Kurmanji - German
		if kur_bool or ger_bool:

			# 2020LeichtfußFreeDict
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2020LeichtfußFreeDict/fd-dictionaries/deu-kur/Deutsch-Kurdî.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2020LeichtfußFreeDict-ger_kur.txt', 'w') as file:
				for line in input_lines:
					file.write(line)
		
			input_lines = []
			# Read the .txt file line-by-line
			with open(datasets_path+'2020LeichtfußFreeDict/fd-dictionaries/kur-deu/kur-deu.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2020LeichtfußFreeDict-kur_ger.txt', 'w') as file:
				for line in input_lines:
					file.write(line)


		# Morisien - English
		if mor_bool or eng_bool:

			# 2022DabreMorisienMT 
			# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
			#input_lines_dev = [json.loads(line)
			#		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
			#input_lines_test = [json.loads(line)
			#		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
			input_lines_train = [json.loads(line)
					for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
			#input_lines = input_lines_dev + input_lines_test + input_lines_train
			input_lines = input_lines_train

			# The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
			# Extracting the English and Morisien texts and store them in data
			data_eng_mor = [input_lines[index]['input']
					for index in range(len(input_lines))]
			data_mor_eng = [input_lines[index]['target']
					for index in range(len(input_lines))]

			# Write the English and Morisien text into a new file
			with open(preprocessed_path+'2022DabreMorisienMT-eng_mor.txt', 'w') as file:
				for line in data_eng_mor:
					file.write(line)
					file.write('\n')
			with open(preprocessed_path+'2022DabreMorisienMT-mor_eng.txt', 'w') as file:
				for line in data_mor_eng:
					file.write(line)
					file.write('\n')


		# Morisien - French
		if mor_bool or fra_bool:

			# 2022DabreMorisienMT 
			# Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
			#input_lines_dev = [json.loads(line)
			#		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
			#input_lines_test = [json.loads(line)
			#		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
			input_lines_train = [json.loads(line)
					for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
			#input_lines = input_lines_dev + input_lines_test + input_lines_train
			input_lines = input_lines_train

			# The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
			# Extracting the English and Morisien texts and store them in data
			data_fra_mor = [input_lines[index]['input']
					for index in range(len(input_lines))]
			data_mor_fra = [input_lines[index]['target']
					for index in range(len(input_lines))]

			# Write the English and Morisien text into a new file
			with open(preprocessed_path+'2022DabreMorisienMT-fra_mor.txt', 'w') as file:
				for line in data_fra_mor:
					file.write(line)
					file.write('\n')
			with open(preprocessed_path+'2022DabreMorisienMT-mor_fra.txt', 'w') as file:
				for line in data_mor_fra:
					file.write(line)
					file.write('\n')


		# German - French - English
		if ger_bool or fra_bool or eng_bool:
			# 2016ElliottMulti30k
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2016ElliottMulti30k/wmt17-mmt/data/train.de') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2016ElliottMulti30k-ger.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2016ElliottMulti30k/wmt17-mmt/data/train.en') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2016ElliottMulti30k-eng.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2016ElliottMulti30k/wmt17-mmt/data/train.fr') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2016ElliottMulti30k-fra.txt', 'w') as file:
				for line in input_lines:
					file.write(line)



		# Ukrainian - English
		if ukr_bool or eng_bool:

			input_ukr = []
			input_eng = []

			# 2023SaichyshynaMulti30K
			# Read json file containing multiple languages
			# (Same issue as in 2022DabreMorisienMT) Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
			input_lines = [json.loads(line)
					for line in open(datasets_path+'2023SaichyshynaMulti30K/Multi30k-uk/train.json', 'r', encoding='utf-8')]

			# The input is on the format:   {"input": "ukrainian_text_here", "target": ""}
			data_ukr = [input_lines[index]['uk']
					for index in range(len(input_lines))]
			data_eng = [input_lines[index]['en']
					for index in range(len(input_lines))]

			# Write the text into a new file
			with open(preprocessed_path+'2023SaichyshynaMulti30K-ukr_eng.txt', 'w') as file:
				for line in data_ukr:
					file.write(line)
					file.write('\n')
			with open(preprocessed_path+'2023SaichyshynaMulti30K-eng_ukr.txt', 'w') as file:
				for line in data_eng:
					file.write(line)
					file.write('\n')



		# Vietnamese - Chinese
		if vie_bool or zho_bool:

			# 2022NgoSynthetic
			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/cn-vi/train.tok.cn') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-zho_vie.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/cn-vi/train.tok.true.vi') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-vie_zho.txt', 'w') as file:
				for line in input_lines:
					file.write(line)


		# Vietnamese - English
		if vie_bool or eng_bool:

			# 2022NgoSynthetic
			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/en-vi/train.tok.en') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-eng_vie.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/cn-vi/train.tok.true.vi') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-vie_eng.txt', 'w') as file:
				for line in input_lines:
					file.write(line)


			# 2021DoanPhoMT
			# There is also an already tokenized version in the collected data
			input_lines = []

			# Read the .txt file line-by-line
			with open(datasets_path+'2021DoanPhoMT/PhoMT/detokenization/train/train.en') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2021DoanPhoMT-eng_vie.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			# Read the .txt file line-by-line
			with open(datasets_path+'2021DoanPhoMT/PhoMT/detokenization/train/train.vi') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2021DoanPhoMT-vie_eng.txt', 'w') as file:
				for line in input_lines:
					file.write(line)





		# Vietnamese - French
		if vie_bool or fra_bool:

			# 2022NgoSynthetic
			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/fr-vi/train.fr') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-fra_vie.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/fr-vi/train.vi') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-vie_fra.txt', 'w') as file:
				for line in input_lines:
					file.write(line)






		# Multilingual Datasets (Others) #
		##################################
		
		# Kurmanji and Turkish
		if kur_bool: 

			# 2020LeichtfußFreeDict
			input_lines = []

			with open(datasets_path+'2020LeichtfußFreeDict/fd-dictionaries/kur-tur/kur-tur.txt') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2020LeichtfußFreeDict-kur_tur.txt', 'w') as file:
				for line in input_lines:
					file.write(line)


		# Vietnamese - Japanese
		if vie_bool:

			# 2022NgoSynthetic
			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/ja-vi/train.ja-vi.ky.ja') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-jap_vie.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

			input_lines = []
			
			# Read the .txt file line-by-line
			with open(datasets_path+'2022NgoSynthetic/Low-resource-Machine-Translation/Datasets/ja-vi/train.ja-vi.tok.true.vi') as file:
				input_lines = file.readlines()

			# Write the text into a new file
			with open(preprocessed_path+'2022NgoSynthetic-vie_jap.txt', 'w') as file:
				for line in input_lines:
					file.write(line)

		

	# Connected to the TODO related to the UnboundLocalError above
	# language_selection()

	data_preprocessing()


if __name__ == "__main__":
	main()
