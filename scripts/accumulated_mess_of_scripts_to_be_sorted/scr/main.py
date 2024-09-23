# -*- coding: utf-8 -*-
# Python Script for working with this corpus
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

"""
User-Guide:
 1. Prior to first start create a virtual environment named venvTextAsCorpusRep via
python -m venv venvTextAsCorpusRep

 2. Then activate this environment via
source venvTextAsCorpusRep/bin/activate

 3. Install the required python packages via
python -m pip install -r requirements.txt 

4. Use of this script:
python main.py -c -l ger kur mor ukr vie
"""

import os
import argparse
import textwrap
import collect_data
import preprocess_data
import explore_data

"""
Input parameters for this script and selection of different target languages:
'-c', '--collect'
'-p', '--preprocess'
'-e', '--explore' (default?)
'-l', '--languages'

Included target languages;
	Chinese: "zho", 	English "eng", 
	French "fra", 		German "ger", 
	Kobani "kob", 		Kurmanji "kur", 
	Morisien "mor",		Russian "rus",
	Ukrainian "ukr", 	Vietnamese "vie"
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
	parser.add_argument('-c', '--collect', action="store_true",
		                  help='setting up the directory structure and collect data.')
	parser.add_argument('-p', '--preprocess', action="store_true",
		                  help='preprocess the collected text data.')
	parser.add_argument('-e', '--explore', action="store_true",
		                  help='explore the data.')
	parser.add_argument('-l', '--languages', nargs="+", type=str,
		                  help='which languages to include.')
	args = parser.parse_args()
	
	#parser.print_help()
	
	# Take the input arguments to then decide which mode to run
	collect = args.collect
	preprocess = args.preprocess
	explore = args.explore
	languages = args.languages

	# Debugging:
	print("collect: "+str(collect) + "    preprocess: "+str(preprocess) + "     run: "+str(explore) + "    languages: "+str(languages))

	def mode_corpus():
		if collect:
			data_collecting(languages, collect)
		if preprocess:
			data_preprocessing(languages, preprocess)
		if explore:
			data_exploring(languages, explore)
	
	"""
	Collecting Data: Call "collecting_data.py" to build directory structure and download text data.
	"""
	def data_collecting(languages, collect=False):
		if collect:
			print("Calling collecting_data.py script.")
			collect_data.main(languages)
			return
			
	"""
	Preprocess Data: Call "preprocess_data.py" to preprocess the collected data.
	"""
	def data_preprocessing(languages, preprocess=False):
		if preprocess:
			print("Calling preprocess_data.py script.")
			preprocess_data.main(languages)
			return
	
	"""
	Explore Data: Call "explore_data.py" to explore and visualize the corpus data.
	"""
	def data_exploring(languages, explore=False):
		if explore:
			print("Calling explore_data.py script.")
			explore_data.main()
			return

	mode_corpus()
	print("Debugging: End of script.")

if __name__ == "__main__":
    main()
