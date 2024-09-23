# -*- coding: utf-8 -*-
# Python Script for sentence and paragraph embeddings via SentenceBERT
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Use:
 (Install)
python -m venv /media/QereqolaXebate/Applications/SentenceBERT/venvSentenceBERT
source /media/QereqolaXebate/Applications/SentenceBERT/venvSentenceBERT
pip install -U sentence-transformers

 1. Navigate to project directory
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/scr

 2. Activate virtual environment of SentenceBERT
source /media/QereqolaXebate/Applications/SentenceBERT/venvSentenceBERT/bin/activate

 3. Use of this script:
python preprocess_sentenceBERT.py -e

python preprocess_sentenceBERT.py -s2 -i1 The wild vegetation is cut and burned, and ashes are used as fertilizers. -i2 Die wilde Vegetation wird gerohdet und verbrannt, und die Asche wird als Dünger benutzt.
python preprocess_sentenceBERT.py -s2 -i "Die wilde Vegetation wird abgeholzt und verbrannt, die Asche wird als Dünger verwendet." "Die wilde Vegetation wird gerohdet und verbrannt, und die Asche wird als Dünger benutzt."
python preprocess_sentenceBERT.py -s2 -i "Die wilden Pflanzen werden geschnitten und verbrannt, und die Asche wird als Dünger verwendet." "Die wilde Vegetation wird gerohdet und verbrannt, und die Asche wird als Dünger benutzt."

 4. Experiment Morisien & Kurmanji in 2023 December
 4.1 Create directory: /TextAsCorpusRep/experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-input
                     & /TextAsCorpusRep/experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-output
 4.2 Move normalized files into input directory: 2022AhmadiInterdialect-eng_kur.txt & 2022DabreMorisienMT-eng_mor.txt
 4.3 Paths for the input files and output, starting from the script, are as following:
     ./../experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-input/2022AhmadiInterdialect-eng_kur.txt
	 ./../experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-input/2022DabreMorisienMT-eng_mor.txt
	 ./../experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-output/
 4.4 Run experiment via
     python preprocess_sentenceBERT.py -sf \
		-if1 ./../experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-input/2022AhmadiInterdialect-eng_kur.txt \
		-if2 ./../experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-input/2022DabreMorisienMT-eng_mor.txt \
		-o ./../experiments/embeddings_sentenceBERT/morisien_kurmanji-2023_december-output/
"""

import os
import argparse
import textwrap
from sentence_transformers import SentenceTransformer, util

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
	parser.add_argument('-l', '--languages', nargs="+", type=str,
		                help='which languages to include.')
	parser.add_argument('-s2', '--similarity_two', action="store_true",
					 	help='calculate cosine similarity of two sentences.')
	parser.add_argument('-i1', '--input1', nargs="*", type=str,
					 	default=["He","likes","to","eat","pizza"],
		                help='input sentences 1 to compare.')
	parser.add_argument('-i2', '--input2', nargs="*", type=str,
					 	default=["He","loves","to","drink","energydrink"],
		                help='input sentences 2 to compare.')
	parser.add_argument('-sf', '--similarity_files', action="store_true",
					 	help='calculate cosine similarity of two files.')
	parser.add_argument('-if1', '--inputPath1', nargs="+", type=str,
					 	default=["./input1.txt"],
		                help='path to input file.')
	parser.add_argument('-if2', '--inputPath2', nargs="+", type=str,
					 	default=["./input2.txt"],
		                help='path to other input file.')
	parser.add_argument('-o', '--outputPath', nargs="+", type=str,
					 	default=["./output.txt"],
		                help='path to output file.')
	args = parser.parse_args()
	
	#parser.print_help()
	
	# Take the input arguments to then decide which mode to run
	example = args.example
	languages = args.languages
	similarity_two = args.similarity_two
	input1 = args.input1
	input2 = args.input2
	similarity_files = args.similarity_files
	inputPath1 = args.inputPath1
	inputPath2 = args.inputPath2
	outputPath = args.outputPath

	# Debugging:
	#print("example: "+str(example)+"    languages: "+str(languages)+"    similarity_two: "+str(similarity_two))
	#print("input1: "+str(input1)+"\ninput2: "+str(input2))
	print("inputPath1[0]: "+str(inputPath1[0])+"\ninputPath2[0]: "+str(inputPath2[0])+"\noutputPath[0]: "+str(outputPath[0]))


	"""
	Example Run:
	"""
	def example_run(example=False):
		if example:
			print("Run example for testing.")

			model = SentenceTransformer('all-MiniLM-L6-v2')

			# Our sentences we like to encode
			sentences = ['This framework generates embeddings for each input sentence',
				'Sentences are passed as a list of string.',
				'The quick brown fox jumps over the lazy dog.']

			# Sentences are encoded by calling model.encode()
			embeddings = model.encode(sentences)

			# Print the embeddings
			for sentence, embedding in zip(sentences, embeddings):
				print("Sentence:", sentence)
				print("Embedding:", embedding)
				print("")
		else:
			print("Info: example variable is: "+str(example))

	"""
	The sentences (texts) are mapped such that sentences with similar meanings are close in vector space. 
	One common method to measure the similarity in vector space is to use cosine similarity.
	Following: https://www.sbert.net/docs/quickstart.html#comparing-sentence-similarities
	"""
	def sentence_similarities_two(sent1, sent2):
		# Load the model
		model = SentenceTransformer('all-MiniLM-L6-v2')

		# Sentences are encoded by calling model.encode()
		emb1 = model.encode(sent1)
		emb2 = model.encode(sent2)

		# Calculate cosine similarity
		cos_sim = util.cos_sim(emb1, emb2)
		print("Cosine-Similarity:", cos_sim, "\n For sentence: ", sent1, "\n and sentence: ", sent2)


	"""
	The sentences (texts) are mapped such that sentences with similar meanings are close in vector space. 
	One common method to measure the similarity in vector space is to use cosine similarity.
	Following: https://www.sbert.net/docs/quickstart.html#comparing-sentence-similarities
	"""
	def sentence_similarities_files(input_path_1, input_path_2, outputPath):
		# Load the model
		model = SentenceTransformer('all-MiniLM-L6-v2')

		# Read input files into two lists of text lines
		input_lines_1 = []
		with open(input_path_1) as f:
			input_lines_1 = f.readlines()

		input_lines_2 = []
		with open(input_path_2) as f:
			input_lines_2 = f.readlines()
		
		# Sentences are encoded by calling model.encode()
		embeddings_1 = model.encode(input_lines_1)
		embeddings_2 = model.encode(input_lines_2)

		# Compute cosine similarity between all pairs
		cos_sim = util.cos_sim(embeddings_1, embeddings_2)

		# Add all pairs to a list with their cosine similarity score
		all_sentence_combinations = []
		for i in range(len(cos_sim)-1):
			for j in range(i+1, len(cos_sim)):
				all_sentence_combinations.append([cos_sim[i][j], i, j])

		# Sort list by the highest cosine similarity score
		all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)

		print("Top-5 most similar pairs:")
		for score, i, j in all_sentence_combinations[0:5]:
			print("{} \t {} \t {:.4f}".format(input_lines_1[i], input_lines_2[j], cos_sim[i][j]))

		# Write scores to file
		with open(outputPath+'score_cosine_similarity.txt', 'w') as f:     
			for line in cos_sim:
				f.write(str(line))

		# Write sorted list of all sentence combinations to file
		with open(outputPath+'score_cosine_similarity_sorted.txt', 'w') as f:     
			for line in all_sentence_combinations:
				f.write(str(line))

	
	def mode_corpus():
		if example:
			example_run(example)
		elif similarity_two:
			sentence_similarities_two(input1, input2)
		elif similarity_files:
			sentence_similarities_files(inputPath1[0], inputPath2[0], outputPath[0])
		else:
			print("Info: No suitable parameter for mode given.")
	

	mode_corpus()
	print("Debugging: End of script.")

if __name__ == "__main__":
    main()
