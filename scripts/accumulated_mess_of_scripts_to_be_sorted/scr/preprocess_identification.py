# -*- coding: utf-8 -*-
# Python Script for language identification using GlotLID
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

"""
GlotLID: https://github.com/cisnlp/GlotLID
"""

"""
For a sentence:
For a file:
For a directory:
"""

import os.path as path
import argparse
import textwrap
from collections import defaultdict # Counting predictions
import fasttext
from huggingface_hub import hf_hub_download

def main():
	parser = argparse.ArgumentParser(
	prog='PROG',
	formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''\
	A script for language identification.
	---------------------------------------
	    For more information check out GlotLID:
	    https://github.com/cisnlp/GlotLID
	'''))
	parser.add_argument('-s', '--sentence', action="store_true",
		                  help='identify language of a sentence.')
	parser.add_argument('-f', '--file', action="store_true",
		                  help='identify language of a file.')
	parser.add_argument('-d', '--directory', action="store_true",
		                  help='identify language of files in a directory.')
	parser.add_argument("-p", "--path", dest="path", 
	                    help="specified path to file or directory.")
	parser.add_argument("-t", "--text", dest="text", 
	                    help="text input by user.")
	args = parser.parse_args()
	
	#parser.print_help()
	
	# Take the input arguments to then decide which mode to run
	sentence = args.sentence
	document = args.file
	directory = args.directory
	path = args.path
	text = args.text

	# Debugging:
	print("sentence: "+str(sentence) 
	+ "    file: "+str(document) 
	+ "    directory: "+str(directory)
	+ "    path: "+str(path))

	"""
	Download the model from huggingface prior to first execution.
	"""
	def download_model():
		# TODO: Include a check if downloading is neccessary. (Shouldn't HugginFace do this on its own?)
		# Download model
		## cache_dir: path to the folder where the downloaded model will be stored/cached.
		model_path = hf_hub_download(repo_id="cis-lmu/glotlid", filename="model.bin", cache_dir="./cached_models")
		return model_path
		
	"""
	Prepare (cached) model for language identification.
	"""
	def load_model(model_path):
		# Load the model
		model = fasttext.load_model(model_path)
		
		# Predict language label (call this function as many times as needed)
		#model.predict("Hello, world!")
		
		return model


	def script_modes(model):
		if sentence:
			identify_sentence(model, text)
		else:
			pass

		if document:
			identify_file(model, path)
		else:
			pass

		if directory:
			identify_directory(model, path)
		else:
			pass
	
	"""
	Sentence: 
	"""
	def identify_sentence(model, text):
		print("Identifying sentence")
		#subprocess.call("./setup.bh")
		return
			
	"""
	File:
	"""
	def identify_file(model, path):
		print("Identifying file")

		# Read the input-file
		text_input = []

		print("Reading file from path: "+str(path))
		with open(path) as f:
			text_input = f.readlines()
		
		print("Writing to file: "+str(path)+'-id.txt')
		with open(path+'-id.txt', 'w') as f:     
			for line in text_input:
				# Remove newline characters from string
				prediction = model.predict(line.replace("\n",""))
				f.write(str(prediction)+"\n")
		return
	
	"""
	Directory:
	"""
	def identify_directory(model, path):
		print("Identifying directory")
		#studytoolkitGUI.main()
		return

	"""
	Count:
	"""
	def count_languages(path):
		print("Count predicted languages")
		labels_count = defaultdict(int)
		
		# Read the file line by line
		with open(path+'-id.txt', 'r') as file:
			for line in file:
			# Extract the label (assuming it's the first element after splitting by '__label__' and '_' characters)
				label = line.split('__label__')[1].split('_')[0]
				labels_count[label] += 1  # Increment the count for this label

		# Sort the counts in decreasing order
		sorted_labels = sorted(labels_count.items(), key=lambda x: x[1], reverse=True)

		# Print the counts
		with open(path+'-id-counts.txt', 'w') as f:     
			for label, count in sorted_labels:
				print(f"{label}: {count}")
				f.write(str(f"{label}: {count}")+"\n")
		return

	# Run steps prior to use
	model_path = download_model()
	model = load_model(model_path)
	
	
	# Run methods based on input-arguments
	script_modes(model)
	count_languages(path)
	print("Debugging: End of script.")
	

if __name__ == "__main__":
	main()