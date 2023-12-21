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
# Navigate to directory for dataset processing
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/scr/datasets

# Activate virtual environment
source ./../../../venvTextAsCorpusRep/bin/activate

# Install requirements
pip install -r ./../../requirements.txt

# ============================================
# Step 00 - Run script for dataset preperation
python datasets_main.py --prepare -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor

# Step 01 - Run script for dataset download
python datasets_main.py --prepare --download -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor 

# Step 02 - Run script for dataset transform
python datasets_main.py --prepare --transform -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor 

# Step 03 - Run script for dataset analysis
python datasets_main.py --analyze -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor 

# Step 04 - Run script for dataset sorting
python datasets_main.py --prepare --sort -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor

# Step 05 - Run script for dataset cleaning
python datasets_main.py --prepare --clean -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor

# Step 06 - Run script for dataset aggregation
python datasets_main.py --prepare --aggregate -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor kmr vie 

# Step 07 - Run script for dataset processing

# Step 08 - Run script for dataset evaluation

# =====================================================================
# Munich-Quick-Fix for processing pdfs and text from website
Create directories:
    /01_download/2023BoukieBanane_txt/
    /01_download/2023BoukieBanane_pdf/
and move the corresponding files into them.

python datasets_main.py --temporary -v \
    --infoPath ./../../data/datasets/ --inputPath ./../../data/datasets/ --outputPath ./../../data/datasets/ \
    --languages mor 



python ./scr/datasets/datasets_main.py -ip PATH -op PATH -l LANGUAGES --prepare --download --transform --analyze --analyze --sort -- clean --aggregate
"""


import argparse
import json
import logging
import os
import sys
import textwrap


import datasets_00_prepare as ds_prep
""" 
Declare languages to include and other project/user parameters.
Build clean directory structure before any data is involved.
"""

import datasets_01_download as ds_down
""" 

"""

import datasets_02_transform as ds_tran
""" 

"""

import datasets_03_analyze as ds_anal
""" 

"""

import datasets_04_sort as ds_sort
""" 

"""

import datasets_05_clean as ds_clea
""" 

"""

import datasets_06_aggregate as ds_aggr
""" 

"""

import datasets_07_process as ds_proc
""" 

"""

import datasets_08_evaluate as ds_eval
""" 

"""

import datasets_09_temporary as ds_temp
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
    language_list = args.languages
    logger.debug(f'language_list: {language_list}')

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
        # PREPARE
        # 
        if args.prepare:
            logging.info("Start preperation.")

            info_path = args.infoPath+'00_prepare/'

            ds_prep.create_dirs_for_lang(args.outputPath)

            language_info = ds_prep.read_language_information(info_path)
            dataset_info = ds_prep.read_dataset_information(info_path)

            #for language in language_info.keys():
            #    if language in args.languages:
            #        logger.debug(f'Languages Information: {language_info[language]}')


            for dataset in dataset_info.keys():
                if dataset_info[dataset]["language"] in args.languages:
                    #logger.debug(f'Dataset Information: {dataset_info[dataset]}')
                    dataset_list.append(dataset)

        #
        # DOWNLOAD
        # 
        if args.download:
            logging.info("Start download.")

            """ Format:
            dataset_info =  { 
					"2022DabreMorisienMT":
					{
						"language":"mor", 
					 	"id":"prajdabre/KreolMorisienMT",
						"source":"huggingface" | "github" | "website"
					}
				}, ...
            """

            download_path = args.outputPath+'01_download/'
            ds_down.main(args.languages, download_path, dataset_info)

        #
        # TRANSFORM
        # 
        if args.transform:
            logging.info("Start transformation.")

            download_path = args.inputPath+'01_download/'
            transform_path = args.outputPath+'02_transform/'

            ds_tran.main(args.languages, download_path, transform_path, dataset_list)

        #
        # ANALYZE
        # 
        if args.analyze:
            logging.info("Start analysis.")

            ds_anal.main(args.languages, args.inputPath, args.outputPath, dataset_list)

        #
        # SORT
        # 
        if args.sort:
            logging.info("Start sort process.")

            transform_path = args.inputPath+'02_transform/'
            sort_path = args.outputPath+'04_sort/'

            ds_sort.main(args.languages, transform_path, sort_path, dataset_list)

        #
        # CLEAN
        # 
        if args.clean:
            logging.info("Start clean process.")

            sort_path = args.inputPath+'04_sort/'
            clean_path = args.outputPath+'05_clean/'

            ds_clea.main(args.languages, sort_path, clean_path, dataset_list)

        #
        # AGGREGATE
        # 
        if args.aggregate:
            logging.info("Start aggregation.")

            clean_path = args.inputPath+'05_clean/'
            aggregate_path = args.outputPath+'06_aggregate/'

            ds_aggr.main(args.languages, clean_path, aggregate_path, dataset_list)

        #
        # PROCESS
        # 
        if args.process:
            logging.info("Start processing.")

            ds_proc.main(args.languages)

        #
        # EVALUATE
        # 
        if args.evaluate:
            logging.info("Start evaluation.")

            ds_eval.main(args.languages)

        #
        # TEMPORARY
        # 
        if args.temporary:
            logging.info("Start temporary solution for PDFs and text from website.")

            ds_temp.main(args.languages, args.inputPath, args.outputPath, dataset_list)

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
    parser.add_argument('--download', action="store_true", help='')
    parser.add_argument('--transform', action="store_true", help='')
    parser.add_argument('--analyze', action="store_true", help='')
    parser.add_argument('--sort', action="store_true", help='')
    parser.add_argument('--clean', action="store_true", help='')
    parser.add_argument('--aggregate', action="store_true", help='')
    parser.add_argument('--process', action="store_true", help='')
    parser.add_argument('--evaluate', action="store_true", help='')
    parser.add_argument('--temporary', action="store_true", help='')
    
    args = parser.parse_args()
    
    print("Debug: Argument parsing done")

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    main(args, loglevel)