# -*- coding: utf-8 -*-
# Python Script for working with text data from available datasets
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Use

"""


import argparse
import json
import logging
import os
import sys
import textwrap

import datasets_01_prepare as ds_prep
""" 
Declare languages to include and other project/user parameters.
Build clean directory structure before any data is involved.
"""

import datasets_02_download as ds_down
""" 

"""

import datasets_03_transform as ds_tran
""" 

"""

import datasets_04_analyze as ds_anal
""" 

"""

import datasets_05_sort as ds_sort
""" 

"""

import datasets_06_clean as ds_clea
""" 

"""

import datasets_07_aggregate as ds_aggr
""" 

"""

import datasets_08_process as ds_proc
""" 

"""

import datasets_09_evaluate as ds_eval
""" 

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

    def mode_script():
        if args.prepare:
            logging.info("Start preperation.")
            ds_prep.main(args.languages)
        elif args.download:
            logging.info("Start download.")
            ds_down.main(args.languages)
        elif args.transform:
            logging.info("Start transformation.")
            ds_tran.main(args.languages)
        elif args.analyze:
            logging.info("Start analysis.")
            ds_anal.main(args.languages)
        elif args.sort:
            logging.info("Start sort process.")
            ds_sort.main(args.languages)
        elif args.clean:
            logging.info("Start clean process.")
            ds_clea.main(args.languages)
        elif args.aggregate:
            logging.info("Start aggregation.")
            ds_aggr.main(args.languages)
        elif args.process:
            logging.info("Start processing.")
            ds_proc.main(args.languages)
        elif args.evaluate:
            logging.info("Start evaluation.")
            ds_eval.main(args.languages)
        else:
            logging.info("No suitable mode provided.")

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
    parser.add_argument("-v", "--verbose",action="store_true",help="increase output verbosity.")
    parser.add_argument('-ip', '--inputPath', type=dir_path,help='path to input files')
    parser.add_argument('-if', '--inputFile', type=argparse.FileType('r'),help='path to input file')
    parser.add_argument('-op', '--outputPath', type=dir_path_out,help='path to output files.')
    parser.add_argument('--languages', type=str, nargs='+', help='list of language ids.')
    parser.add_argument('--prepare', action="store_true", help='')
    parser.add_argument('--download', action="store_true", help='')
    parser.add_argument('--transform', action="store_true", help='')
    parser.add_argument('--analyze', action="store_true", help='')
    parser.add_argument('--sort', action="store_true", help='')
    parser.add_argument('--clean', action="store_true", help='')
    parser.add_argument('--aggregate', action="store_true", help='')
    parser.add_argument('--process', action="store_true", help='')
    parser.add_argument('--evaluate', action="store_true", help='')
    
    args = parser.parse_args()
    
    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    
    main(args, loglevel)