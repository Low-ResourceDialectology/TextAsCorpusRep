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
cd ~/Lappotron4000/CrazyProjects/TextAsCorpusRep/experiments/analyze_text_data/scripts

# Activate virtual environment
source ./../../../venvTextAsCorpusRep/bin/activate


# =====================================================================
# Munich-Quick-Fix for processing pdfs and text from website
Sources:
SeedNLLB: https://github.com/openlanguagedata/seed
DabreMT: https://arxiv.org/abs/2206.02421
BoukieBanane: https://boukiebanane.com/

Create directories:
    analyze_text_data/data/BoukieBanane/
    analyze_text_data/data/DabreMT/
    analyze_text_data/data/SeedNLLB/
and move the corresponding files into them.

BoukieBanane (From prior processing until sort): 23 txt files with content
DabreMT (From prior processing until sort): 6 txt files with words and sentences
SeedNLLB (from Github): eng_Latn

# =====================================================================
python analyze_main.py --inputPath ./../data/ --anal01 -v


"""


import argparse
import json
import logging
import os
import sys
import textwrap


import analyze_01 as anal_01
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

    #
    # Dictionaries to hold information that might be used "globally" in multiple scripts.
    # 
    language_info = {}
    """ Format:
    language_info = 
    """

    dataset_info = {}
    """ Format:
    dataset_info = 
    """
    
    dataset_list = []
    """ Format:
    dataset_list = ['2022DabreMorisienMT', '2022AhmadiInterdialect', '2017LuongNMT']
    """


    """
    Script execution based on input arguments
    """
    def mode_script():
        #
        # ANALYZE 01
        # 
        if args.anal01:
            logging.info("Start Analysis.")

            anal_01.main(args.inputPath)

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
    parser.add_argument('--prepare', action="store_true", help='')
    parser.add_argument('--anal01', action="store_true", help='')
    
    args = parser.parse_args()
    
    print("Debug: Argument parsing done")

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    main(args, loglevel)