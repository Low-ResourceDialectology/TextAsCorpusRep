# -*- coding: utf-8 -*-
# Python Script for transforming NLLB Seed data to json format
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################
""" Use:
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato

python transform_seed_data.py
"""
import os

"""
Each sentence of the NLLB Seed data needs to start with something like:
{"id": "item_1", "text": "
and end with:
"} 
"""
def main():

	#input_text_file = './MTACR-december/data/nllb.txt'
	#output_json_file = './MTACR-december/data/nllb.json'
	input_text_file = './MTACR-december/data/seed.txt'
	output_json_file = './MTACR-december/data/seed.json'

	nllb_seed = []

	# Read text data from .txt file
	with open(input_text_file) as f:
		nllb_seed = f.readlines()

	# Transform into .json format required by potato
	counter = 0
	nllb_transformed = []
	for line in nllb_seed:
		counter = counter + 1
		prefix = '{"id": "item_'+str(counter)+'", "text": "'
		line_new = line[:-2].replace('"','\\"') # [:2] excludes the last 2 characters (\n) to add it again in the postfix
		postfix = '"}\n'
		
		nllb_transformed.append(prefix+line_new+postfix) 

	# Write transformed data to file
	with open(output_json_file, 'w') as f: 
		for line in nllb_transformed:    
			f.write(line)

	print("Debugging: End of script.")

if __name__ == "__main__":
    main()
