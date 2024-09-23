# -*- coding: utf-8 -*-
# Python Script for text parsing via NLTK
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Sources:
POS-Tagging with NLTK Tutorial: https://www.guru99.com/pos-tagging-chunking-nltk.html
"""

""" Use:
 (Install)
python -m spacy download en_core_web_sm
	# Required for pos_parsing # screw tutorial-maker that leave these "minor side-information" out for some reason!
	#nltk.download('punkt') 
	#nltk.download('averaged_perceptron_tagger')

 1. Navigate to project directory
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/scr

 2. Activate virtual environment via
source ./../../venvTextAsCorpusRep/bin/activate

 3. Use of this script:
python preprocess_parsing.py -i PATH_TO_INPUT -o PATH_OT_OUTPUT

 4. Experiment 12 Sentences
 4.1 Create directory: /TextAsCorpusRep/experiments/parsing_NLTK/12sentences-input
                     & /TextAsCorpusRep/experiments/parsing_NLTK/12sentences-output
 4.2 Move text file with 12 sentences into input directory: 12sentences.txt
 4.3 Paths for the input files and output, starting from the script, are as following:
     ./../experiments/parsing_NLTK/12sentences-input/12sentences.txt
	 ./../experiments/parsing_NLTK/12sentences-output
 4.4 Run experiment via
     python preprocess_parsing.py -p \
		-i ./../experiments/parsing_NLTK/12sentences-input/12sentences.txt \
		-o ./../experiments/parsing_NLTK/12sentences-output/
"""

import os
import argparse
import textwrap
import nltk
import spacy
from pathlib import Path # For saving spacy plot to file
#from spacy import displacy

# pip install torch
# pip install transformers
# pip install underthesea
import underthesea # import pos_tag # https://github.com/undertheseanlp/underthesea/tree/main/docs

"""
Input parameters for this script
"""
def main():
	parser = argparse.ArgumentParser(
	prog='PROG',
	formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''\
	A corpus of text data for selected languages.
	---------------------------------------------
	    For more information check out the github repository:
	    https://github.com/Low-ResourceDialectology/TextAsCorpusRep
	'''))
	parser.add_argument('-e', '--example', action="store_true",
		                help='example run for testing.')
	parser.add_argument('-s', '--sentence', nargs="+", type=str,
					 	default=["Christian is well known for being a pizza-eating dwarf fortress fanatic, who might or might not be the inventor of the color green."],
		                help='path to input file.')
	parser.add_argument('-p', '--parser', action="store_true",
		                help='parsing the input text.')
	parser.add_argument('-i', '--inputPath', nargs="+", type=str,
					 	default=["./input.txt"],
		                help='path to input file.')
	parser.add_argument('-o', '--outputPath', nargs="+", type=str,
					 	default=["./output.txt"],
		                help='path to output file.')
	args = parser.parse_args()
	
	#parser.print_help()
	
	# Take the input arguments to then decide which mode to run
	example = args.example
	sentence = args.sentence
	parsing = args.parser
	inputPath = args.inputPath
	outputPath = args.outputPath

	# Debugging:
	print("example: "+str(example)+"    parsing: "+str(parsing))
	#print("input1: "+str(input1)+"\ninput2: "+str(input2))
	print("inputPath[0]: "+str(inputPath[0])+"\noutputPath[0]: "+str(outputPath[0]))

	"""
	Example Run:
	"""
	def example_run(sent, example=False):
		if example:
			print("Run example for testing.")

			text =sent.split()
			print("After Split:",text)

			tokens_tag = nltk.pos_tag(text)
			print("After Token:",tokens_tag)

			patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
			chunker = nltk.RegexpParser(patterns)
			print("After Regex:",chunker)

			output = chunker.parse(tokens_tag)
			print("After Chunking",output)

		else:
			print("Info: example variable is: "+str(example))

	"""
	Parse Text:
	"""
	def parse_text(input_path, output_path, parsing=False):
		# Part-of-Speech Tagging
		if parsing:
			print("Parsing text file")

			# Read input files into two lists of text lines
			input_lines = []
			with open(input_path) as f:
				input_lines = f.readlines()

			# Write scores to file
			with open(output_path+'pos_tags.txt', 'w') as f:     
				for line in input_lines:
					
					sentence = nltk.sent_tokenize(line)
					for sent in sentence:
						#print(nltk.pos_tag(nltk.word_tokenize(sent)))
						tags = nltk.pos_tag(nltk.word_tokenize(sent))
						f.write(str(tags))
					# Linebreak for next line of text
					f.write('\n')	

			# Visualize Part-of-Speech Tagging
			nlp = spacy.load("en_core_web_sm")

			line_counter = 1
			for line in input_lines:
				doc = nlp(line)
			
				# Options for "dep" to render a background color
				options = {"bg":"rgb(220,255,220)", "distance":75}
				#svg = spacy.displacy.render(doc, style = "dep") # render is for use in jupyterNotebooks
				#svg = spacy.displacy.serve(doc, style = "dep", options=options) # serve for use on server and in HTML
				svg = spacy.displacy.render(doc, style = "dep", options=options, jupyter=False)

				file_name = '-'.join([w.text for w in doc if not w.is_punct]) # → OSError: [Errno 36] File name too long: 
				#output_path = Path("/images/" + file_name)
				file_name = file_name[:100]

				output_path_svg = Path(output_path+'dependency_plot_'+str(line_counter)+file_name+'.svg')
				output_path_svg.open("w", encoding="utf-8").write(svg)
				line_counter = line_counter + 1 
		else:
			print("Info: parsing variable is: "+str(parsing))

	"""
	Parse Vietnamese Text:
	"""
	def parse_vietnamese(input_path, output_path):
		# Part-of-Speech Tagging
		
		print("Parsing Vietnamese text file")
		# Read input files into two lists of text lines
		input_lines = []
		with open(input_path) as f:
			input_lines = f.readlines()

		# Write tag to file
		with open(output_path+'pos_tags_vietnamese.txt', 'w') as f:     
			for line in input_lines:
				
				tags = underthesea.pos_tag(line)
				f.write(str(tags))
				f.write('\n')
		
		# TODO: Fix error: KeyError: '__getitems__'
		# Write dependencies to file
		#with open(output_path+'dependency_vietnamese.txt', 'w') as f:     
		#	for line in input_lines:
		#		
		#		tags = underthesea.dependency_parse(line)
		#		f.write(str(tags))
		#		f.write('\n')	

	"""
	Parse Kurmaanji Text:
	"""
	def parse_kurmanji(input_path, output_path):
		# Part-of-Speech Tagging
		
		print("Parsing Kurmanji text file")
		# Read input files into two lists of text lines
		input_lines = []
		with open(input_path) as f:
			input_lines = f.readlines()

		# Write scores to file
		with open(output_path+'pos_tags_kurmanji.txt', 'w') as f:     
			for line in input_lines:
				
				tags = underthesea.pos_tag(line)
				f.write(str(tags))
				# Linebreak for next line of text
				f.write('\n')

	"""
	Parse Morisien Text:
	"""
	def parse_morisien(input_path, output_path):
		# Part-of-Speech Tagging
		
		print("Parsing Morisien text file")
		# Read input files into two lists of text lines
		input_lines = []
		with open(input_path) as f:
			input_lines = f.readlines()

		# Write scores to file
		with open(output_path+'pos_tags_morisien.txt', 'w') as f:     
			for line in input_lines:
				
				tags = underthesea.pos_tag(line)
				f.write(str(tags))
				# Linebreak for next line of text
				f.write('\n')
	
	"""
	Parse German Text:
	"""
	def parse_german(input_path, output_path):
		# Part-of-Speech Tagging
		
		print("Parsing German text file")
		# Read input files into two lists of text lines
		input_lines = []
		with open(input_path) as f:
			input_lines = f.readlines()

		# Write scores to file
		with open(output_path+'pos_tags_german.txt', 'w') as f:     
			for line in input_lines:
				
				sentence = nltk.sent_tokenize(line, language='german')
				for sent in sentence:
					#print(nltk.pos_tag(nltk.word_tokenize(sent)))
					tags = nltk.pos_tag(nltk.word_tokenize(sent, language='german'))
					f.write(str(tags))
				# Linebreak for next line of text
				f.write('\n')	

	
	def mode_corpus():
		if example is True:
			example_run(sentence, example)
		elif parsing:
			parse_text(inputPath[0], outputPath[0], parsing)
			#parse_vietnamese(inputPath[0], outputPath[0])
			# TODO: Solve hardcoded quick-fix
			parse_vietnamese(inputPath[0][:-4]+'_vietnamese.txt', outputPath[0])
			#parse_kurmanji(inputPath[0][:-4]+'_kurmanji.txt', outputPath[0])
			#parse_morisien(inputPath[0][:-4]+'_morisien.txt', outputPath[0])
			parse_german(inputPath[0][:-4]+'_german.txt', outputPath[0])
		else:
			print("Info: No suitable parameter for mode given.")
	

	mode_corpus()
	print("Debugging: End of script.")

if __name__ == "__main__":
    main()
