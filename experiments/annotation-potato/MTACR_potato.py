# -*- coding: utf-8 -*-
# Python Script for annotations via potato
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Sources:
Potato: the POrtable Text Annotation TOol: https://github.com/davidjurgens/potato#potato-the-portable-text-annotation-tool
NLLB-Seed Machine Translation Data version 2: https://github.com/openlanguagedata/seed/blob/main/seed/eng_Latn
"""

""" User-Guide:
 0. Open a terminal and navigate to your desired directory:
cd PATH_TO_DIRECTORY/TextAsCorpusRep/experiments/annotation-potato
( cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato )

 1. Clone the github repository to your computer:
git clone git@github.com:davidjurgens/potato.git
( alternatively: git clone https://github.com/davidjurgens/potato.git )

 2. Prior to first start create a virtual environment named venvPotato via
python -m venv venvPotato
(you might have to use python3 instead of python)

 3. Then activate this environment via
source venvPotato/bin/activate

 4. Install the required python packages via
pip install -r ./potato/requirements.txt
(you might have to use pip3 instead of pip)

 5. To check installation, run a simple check-box style annotation on text data via
python potato/flask_server.py start project-hub/simple_examples/configs/simple-check-box.yaml -p 8000

This will launch the webserver on port 8000 which can be accessed via a webbrowser at 
http://localhost:8000

 6. Start our annotation experiment via
python potato/potato/flask_server.py start MTACR-december/MTACR-textbox.yaml -p 8000

TODO 7. Use of this script via
python MTACR_potato.py



"""

import os
import argparse
import textwrap
import collect_data
import preprocess_data
import explore_data

"""

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
