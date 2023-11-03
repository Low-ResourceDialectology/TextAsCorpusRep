# -*- coding: utf-8 -*-
# Python Script for setting up directories and collecting online data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

import os
import shutil
from git import Repo

"""
Data collection script.
1. Check existence of directories for selected languages
2. Create missing ones
3. Collect online available text data for selected languages
"""
def main(languages):
	print("Starting collect_data script.") # Debugging

	# Create directories #
	######################
	# Some datasets are monolingual, but many contain multiple languages and to prevent duplicates,
	# storing will be centralized for the original data.
	collected_data_path = './../data/data_datasets/'

	# Lists of directories based on available data from online sources by language
	## These are currently managed manually.

	## Chinese
	zho_paths = ['']

	## English
	eng_paths = ['']

	## French
	fra_paths = ['']

	## German
	ger_paths = ['2016ElliottMulti30k']

	## Kobani
	kob_paths = ['']

	## Kurmanji
	kur_paths = ['2023AhmadiSouthernCorpus',
				'2022AhmadiInterdialect',
				'2020AhmadiKurdishTokenization',
				'2013EsmailiPewan',
				'2020FatihkurtKurdishTwitter',
				'2020LeichtfußFreeDict',
				'2001HaigKurdishNewspaper']

	## Morisien (Mauritian Creole)
	mor_paths = ['2022DabreMorisienMT']

	## Russian
	rus_paths = ['']

	## Ukrainian
	ukr_paths = ['2023SaichyshynaMulti30K']

	## Vietnamese
	vie_paths = ['2022NgoSynthetic',
				'2021DoanPhoMT']



	# Helper-Function for language selection
	def language_selection(target_languages):
		print("Selecting target languages.") # Debugging

		# Start with empty list of directories:
		list_of_datasets = []

		#print("Line 147"+str(target_languages)) # Debugging

		# Include languages based on provided "target_languages"
		if "zho" in target_languages:
			list_of_datasets = list_of_datasets + zho_paths
		if "eng" in target_languages:
			list_of_datasets = list_of_datasets + eng_paths
		if "fra" in target_languages:
			list_of_datasets = list_of_datasets + fra_paths
		if "ger" in target_languages:
			list_of_datasets = list_of_datasets + ger_paths
		if "kob" in target_languages:
			list_of_datasets = list_of_datasets + kob_paths
		if "kur" in target_languages:
			list_of_datasets = list_of_datasets + kur_paths
		if "mor" in target_languages:
			list_of_datasets = list_of_datasets + mor_paths
		if "rus" in target_languages:
			list_of_datasets = list_of_datasets + rus_paths
		if "ukr" in target_languages:
			list_of_datasets = list_of_datasets + ukr_paths
		if "vie" in target_languages:
			list_of_datasets = list_of_datasets + vie_paths

		# Return the directory list for all selected target languages:
		return list_of_datasets

		

	# Creating the directories
	def setup_directories(target_languages):
		print("Creating the missing target languages directories.") # Debugging

		# Call Helper-Function to get list of directories:
		language_dir_list = language_selection(target_languages)

		# Create the directories based on the list:
		for dir_to_create in language_dir_list:

			# If the directory does not already exist
			if not os.path.exists(collected_data_path+dir_to_create):
				# Create the directory
				os.makedirs(collected_data_path+dir_to_create)

			# If the directory already exists
			else:
				# Remove the directory-path from the list to exclude from further steps
				language_dir_list.remove(dir_to_create)

		# Once all missing directories have been created 
		# and the ones, that already existed have been excluded from the list,
		# Collect online available text data (sets)




	# Collecting the data from online sources
	def collect_online_data(target_languages):
		print("Start collecting online data.") # Debugging

		# Read info from source.json file


		# Clone github repository
		#Repo.clone_from(git_url, repo_dir)



	#print("Line 147"+str(languages)) # Debugging

	# Start with creating missing directories for target languages and check which ones already exist
	setup_directories(languages)

	# Collect text data from online sources
	collect_online_data(languages)



if __name__ == "__main__":
    main()

