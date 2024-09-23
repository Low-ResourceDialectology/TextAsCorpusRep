# -*- coding: utf-8 -*-
# Python Script for working with text data from available datasets
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

# Path to project repository: /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep

""" Use
# Navigate to directory for analyze experiment
cd ~/Lappotron4000/CrazyProjects/TextAsCorpusRep/experiments/nllb_seed_pivot/scr

# Activate virtual environment
source ./../../../venvTextAsCorpusRep/bin/activate


# =====================================================================
# Munich-Quick-Fix for processing pdfs and text from website
Sources:
SeedNLLB: https://github.com/openlanguagedata/seed

TODO: Automate directory creation and seed download
Create directories:
    nllb_seed_pivot/data/input/
    nllb_seed_pivot/data/automatic/
    nllb_seed_pivot/data/evaluated/
    nllb_seed_pivot/data/output/
and move the nllb-seed file (eng_Latn) into the input directory.


# =====================================================================
# Automatic translation of nllb-seed data
python nllb_seed_main.py --inputPath ./../data/input/ --outputPath ./../data/automatic/ --translation --scriptMode translateSeed --language deu vie zho -v

# =====================================================================
# Evaluation of translated nllb-seed data
python nllb_seed_main.py --inputPath ./../data/automatic/ --outputPath ./../data/evaluated/ --scriptMode evaluateTranslations --language deu vie -v


"""


import argparse
import json
import logging
import os
import sys
import textwrap

import translate_text_lines as tran_tl
""" 
Temporary solution to process pdf files and crawled text from website.
"""

""" Check for input path to be valid directory """
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

""" Create output path if not existing """
def dir_path_out(string):
    # Directory does not exist yet
    try:
        os.makedirs(string)
    # Directory already exists
    except FileExistsError:
        pass 

""" Check for file to exist """
def dir_file(string):
    if os.path.isfile(string):
        return string
    else:
        raise NotADirectoryError(string)


""" main():
Parsing input parameters for this script, given in terminal.
Such as: python main.py -e
"""
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logger = logging.getLogger('progress')

    # List of languages to be processed
    #language_list = [] # Debugging
    #language_list = args.languages
    #logger.debug(f'language_list: {language_list}')

    """
    Script execution based on input arguments
    """
    def mode_script():
        #
        # TRANSLATE TEXT
        # 
        if args.translation:
            logging.info("Start Translation.")

            tran_tl.main(args.inputPath, args.outputPath, args.scriptMode, args.languages)
            
        #else:
        #    logging.info("No suitable mode provided.")

    mode_script()
    logging.info("Reached end of Script.")


# Standard boilerplate to call the main() function to begin the program.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #prog='PROG',
        #description=__doc__,
        description=textwrap.dedent('''\
            Description of Script/Module
            ---------------------------------------------
            For more information check out the github repository:
            https://github.com/Low-ResourceDialectology/TextAsCorpusRep
            '''),
        epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars = '@' )
        # Specify your real parameters here:
    parser.add_argument("-v", "--verbose",action="store_true", help="increase output verbosity.")
    parser.add_argument('-ip', '--inputPath', type=dir_path, help='path to input files')
    #parser.add_argument('-if', '--inputFile', type=argparse.FileType('r'), help='path to input file')
    parser.add_argument('-if', '--inputFile', type=str, help='path to input file')
    #parser.add_argument('-op', '--outputPath', type=dir_path_out,help='path to output files.')
    parser.add_argument('-op', '--outputPath', type=str ,help='path to output files.')
    parser.add_argument('--infoPath', type=str ,help='path to language and dataset information files.')
    parser.add_argument('-l', '--languages', type=str, nargs='+', help='list of language ids.')
    parser.add_argument('--scriptMode', type=str, nargs='+', help='mode of script execution.')
    parser.add_argument('--translation', action="store_true", help='')
    
    args = parser.parse_args()
    
    print("Debug: Argument parsing done")

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    main(args, loglevel)