# -*- coding: utf-8 -*-
# Python Script for transforming, sorting and cleaning collected text data (webdata)
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################
"""
Prior Step: Get and Transform Webdata
This Step: Cleaning of Text Data
Next Step: Language Identification
"""

""" Development-Note:
Moved from the clean.py script for datasets to prepare future work to be better structured.
"""

import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 
import json
import logging
import os
import re
import sys

# Enable importing the other scripts by adding their location to the python-path
sys.path.append(r"./../../")

import utils.utilities_general as util_ge


"""
Transforming the collected Data into a normalized structure for easy processing.
"""
def transform_data(current_dataset_key, current_dataset_info, inputPath, outputPath):

    logging.debug(f'====== Transforming dataset')
    logging.debug(f'++++++ inputPath: {inputPath}')
    logging.debug(f'++++++ outputPath: {outputPath}')

    # #########################################################################
    # TODO - Data in PDF format
    # INPUT: "2012MorisienGramer/GRAMER_KREOL_MORISIEN_Volim_1_Dokiman_Re-2.pdf"
    # OUTPUT: "mor.mor"
    if current_dataset_key == '2012MorisienGramer':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'mor.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{output_file}')


    # #########################################################################
    # TODO - Data in PDF format
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2021MorisienDictionaryEnglish':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'eng.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{output_file}')

    # #########################################################################
    # TODO - Data in PDF format
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2021MorisienEducationalBooksPupil':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'mor.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{filename}-{output_file}')

    # #########################################################################
    # TODO - Data in PDF format
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2021MorisienEducationalBooksTeacher':
        logging.debug(f'TODO: Download these files first!')

    # #########################################################################
    # TODO - Data in form of many different (pdf) files
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2023DevVirahsawmyBoukieBananePDF':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'mor.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{filename}-{output_file}')

    # #########################################################################
    # TODO - Simple txt format mainly in need of sorting
    # INPUT: "2023DevVirahsawmyBoukieBananeWeb/mor-boukiebanane_com.txt"
    # OUTPUT: "mor-boukiebanane_com.mor"
    if current_dataset_key == '2023DevVirahsawmyBoukieBananeWeb':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_input_filename = "boukiebanane_com-mor.txt"
        current_output_filename = "boukiebanane_com-mor.mor"

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Read the .txt file line-by-line
        input_lines = util_ge.read_text_file(f'{download_path}{current_input_filename}')
        output_lines = []

        for line in input_lines:
            if not line == '':
                output_lines.append(line)

        # Write the text into a new file
        util_ge.write_text_file(f'{transform_path}{current_output_filename}', output_lines)



"""
Sorting the (collected and) transformed Data into a normalized structure for easy processing.
INPUT: Various combinations of files, monolingual, bilingual, multilingual text data.
OUTPUT: Single file for "words" and for "sentences" per language of dataset.

Some datasets can already be considered to be "sorted" at this point and will just be copied to the new location.
"""
def sort_data(current_dataset_key, current_dataset_info, input_path, output_path):

    logging.debug(f'====== Sorting dataset')
    logging.debug(f'++++++ inputPath: {input_path}')
    logging.debug(f'++++++ outputPath: {output_path}')

    # TODO: Something weird going on here that messed up some of the lines
    # such as: "K o u m a  f i n n  d e z a  s o u l igne dan rapor lortograf, Akademi Kreol Morisien"
    if current_dataset_key == '2012MorisienGramer':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}mor.mor'
        output_file = f'{sort_path}mor.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = []
        #text_lines_sorted = util_ge.text_lines_to_sentences(text_lines_no_empty)
        for line in text_lines_no_empty:
            fixed_line = ""

            # WHAT AM I EVEN DOING HERE?! COUNTING EMPTY SPACES IN TEXT LINES?!?!
            # Just do it for every line and be done with it!
            # Oh... Right... That's why! → Back to the idiotic way (at least it works!)
            """
            for index in range(len(line)):
                if not line[index] == ' ':
                    fixed_line = fixed_line + line[index]
                elif line[index] == ' ' and line[index+1] == ' ':
                    fixed_line = fixed_line + line[index]
            text_lines_sorted.append(fixed_line)
            """
            
            if len(line) > 7 and len(line) < 25:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 24 and len(line) < 35:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 34 and len(line) < 45:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 44 and len(line) < 55:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[35] == ' ' and line[37] == ' ' and line[39] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[36] == ' ' and line[38] == ' ' and line[40] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 54 and len(line) < 65:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[35] == ' ' and line[37] == ' ' and line[39] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[36] == ' ' and line[38] == ' ' and line[40] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 64:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[35] == ' ' and line[37] == ' ' and line[39] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[36] == ' ' and line[38] == ' ' and line[40] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[43] == ' ' and line[45] == ' ' and line[47] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[44] == ' ' and line[46] == ' ' and line[48] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[47] == ' ' and line[49] == ' ' and line[51] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[57] == ' ' and line[59] == ' ' and line[61] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[58] == ' ' and line[60] == ' ' and line[62] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[59] == ' ' and line[61] == ' ' and line[63] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[60] == ' ' and line[62] == ' ' and line[64] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)
            else:
                text_lines_sorted.append(line)
            
        # Dirty Quick-Fix for handling full stops such as "Dr." or "..."
        text_lines_replaced = []
        for line in text_lines_sorted:
            text_lines_replaced.append(line.replace('Dr.', 'Doctor').replace('M.A.', 'MA').replace('Mm.','Mademoiselle').replace('Mm ','Mademoiselle ').replace('M. ','Monsieur '))

        text_lines_dirty_fix = util_ge.text_lines_short_to_sentences(text_lines_replaced)

        text_lines_output = []
        # Remove lines only containing a full stop
        for line in text_lines_dirty_fix:
            if not line == '.':
                text_lines_output.append(line)

        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_output)


    """
    Each page of this dictionary is of the form

        DIKS YON ER KREOL MORISYEN  
 
        3 
        A 
        abandone  (abandon) [from Fre 
        abandonner] : to abandon. Akoz samem, 
        ler mo ti ena sizan mo ti abandon 
        posibilite vinn enn gran pent = Because 
        (of) that, when I was six years old I 
        missed the  chance to become a great 
        painter.  Mo finn abandon li tusel lakaz = I 
        left him alone at home.  
        abba  : in vain. Mo'nn seye me abba = I've 
        tried but in vain.  
        abi [from Fre abus] : abuse  
        abitan  [from Fre habitant] : inhabitant.  So 
        abitan zot katorz = Its inhab itants number 
        fourteen.  
        abite  [from Fre habiter] : to inhabit. 
        Dezyem  planet la ti abite par enn vantar = 

    Idea: 
    1. Remove the headline
    2. Remove the page number
    3. Remove the letter-indicator
    4. Put everything into a single string/text line
    5. Split at the ":"
        → abandone  (abandon) [from Fre abandonner] 
        → : to abandon. Akoz samem, ler mo ti ena sizan mo ti abandon posibilite vinn enn gran pent = Because (of) that, when I was six years old I missed the  chance to become a great painter.  Mo finn abandon li tusel lakaz = I left him alone at home.  abba  
        → : in vain. Mo'nn seye me abba = I've tried but in vain.  abi [from Fre abus] 
    6. Now split at the last full stop
        → abandone  (abandon) [from Fre abandonner] 
        → : to abandon. Akoz samem, ler mo ti ena sizan mo ti abandon posibilite vinn enn gran pent = Because (of) that, when I was six years old I missed the  chance to become a great painter.  Mo finn abandon li tusel lakaz = I left him alone at home
            .  
            abba  
        → : in vain. Mo'nn seye me abba = I've tried but in vain
            .  
            abi [from Fre abus] 
    7. Recombine 
        For the very first item:
            Element in front of : with element behind the : but without the part after the .
        For each following item:
            Element after the . but in front of : with element behind the : but without the part after the .
    """
    if current_dataset_key == '2021MorisienDictionaryEnglish':
        # TODO: The above steps
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}eng.mor'
        output_file = f'{sort_path}eng.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_input = []

        # Iterate over files in that directory
        # Read text file to text lines
        text_lines_current_file = util_ge.read_text_file(input_file)
        text_lines_useful = text_lines_current_file[40:9010]

        for line in text_lines_useful:
            if not line == "    DIKS YON ER KREOL MORISYEN  ":
                text_lines_input.append(line)

        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_short_to_sentences(text_lines_no_empty)
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)

    """
    Combine the text of all files into one.
    """
    if current_dataset_key == '2021MorisienEducationalBooksPupil':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        output_file = f'{sort_path}mor.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_input = []

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                for line in text_lines_current_file:
                    text_lines_input.append(line)

        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_short_to_sentences(text_lines_no_empty)
        # Remove some of the silly transformations such as "." as a single line
        text_lines_output = []
        for line in text_lines_sorted:
            if len(line) > 4:
                text_lines_output.append(line)

        # Save text file        
        util_ge.write_text_file_lines(output_file, text_lines_output)

    if current_dataset_key == '2021MorisienEducationalBooksTeacher':
        pass

    if current_dataset_key == '2022AhmadiInterdialect':
        # TODO: Add full stop (.) at end of each sentence.
        # Remove special characters spanning text-lines "line_1, line_2, line_3"
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Save text file
                util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)


    """
    Combine the text of many txt files into one txt file.
    """
    if current_dataset_key == '2023DevVirahsawmyBoukieBananePDF':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        output_file = f'{sort_path}mor.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_input = []

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                for line in text_lines_current_file:
                    text_lines_input.append(line)

        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_short_to_sentences(text_lines_no_empty)
        # Remove some of the silly transformations such as "." as a single line
        text_lines_output = []
        for line in text_lines_sorted:
            if len(line) > 4:
                text_lines_output.append(line)
        
        # Save text file
        util_ge.write_text_file_lines(f'{output_file}', text_lines_output)


    if current_dataset_key == '2023DevVirahsawmyBoukieBananeWeb':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}boukiebanane_com-mor.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)
    
        # Read text file to text lines
        text_lines_current_file = util_ge.read_text_file(input_file)
        current_filename = util_ge.get_filename_with_extension(input_file)
        current_file_out = f'{sort_path}{current_filename}'
        
        # ================================
        # Sentences
        current_content = []

        # Combine all lines into one
        one_line = ""

        for line in text_lines_current_file:
            # Also remove all line breaks
            one_line = one_line + line.replace('\n', '')

        # Replace all special characters with a space
        one_line_no_special = re.sub('[^A-Za-z0-9.,!?:;()]+', ' ', one_line)

        # Replace all single characters with a space
        one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
        
        # Replace all double spaces with one space
        one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
        
        # Remove leading and trailing spaces
        one_line_stripped = one_line_no_doublespace.strip()
        

        one_line_split = one_line_stripped.split('.')
        #logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

        for sentence in one_line_split:
            current_content.append(sentence+'.')

        util_ge.write_text_file_lines(current_file_out, current_content)
        #with open(current_file_out, 'w') as file:
            #for line in one_line_split:
                #if util.check_for_non_empty_string(line):
                #    file.write(line.strip().replace('  ',' '))
                #    file.write('\n')

        """
        # ================================
        # Words
        # Combine all lines into one
        one_line = ""

        for line in text_lines_current_file:
            # Also remove all line breaks
            one_line = one_line + line

        #logging.debug(f'one_line[0:100] = {one_line[0:100]}')

        #one_line_split = one_line.split('.')
        #logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

        # Replace all line breaks with a space
        one_line_no_breaks = re.sub('\n', ' ', one_line)
        
        # Replace all special characters with a space
        one_line_no_special = re.sub('[^A-Za-z0-9]+', ' ', one_line_no_breaks)

        # Replace all single characters with a space
        one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
        
        # Replace all double spaces with one space
        one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
        
        # Remove leading and trailing spaces
        one_line_stripped = one_line_no_doublespace.strip()

        # Make all text lower case
        one_line_no_uppercase = one_line_stripped.lower()

        words = one_line_no_uppercase.split(" ")

        word_count = {}

        for word in words:
            if word not in word_count:
                word_count[word] = 1
            elif word in word_count:
                word_count[word] += 1
            
        #current_content.append(sentence)

        # Sort dictionary 
        sorted_word_count = sorted(word_count.items(), key=lambda x:x[1], reverse = True)
        sorted_word_count_dict = dict(sorted_word_count)

        # Serializing json
        json_object = json.dumps(sorted_word_count_dict, indent=4)
        
        # Writing to sample.json
        with open(analyze_path_pdf+filename+'.json', "w") as outfile:
            outfile.write(json_object)
        """
        # Save text file
        #util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)



"""
Cleaning the (collected and transformed and) sorted Data into a normalized structure for easy processing.
INPUT: Single file for "words" and for "sentences" per language of dataset.
OUTPUT: The same files, but now containing cleaned text (normalized encoding, no special characters, removal of weird formatting).

Some datasets can already be considered to be "cleaned" at this point and will just be copied to the new location.
"""
def clean_data(current_dataset_key, current_dataset_info, input_path, output_path):

    logging.debug(f'====== Cleaning dataset')
    logging.debug(f'++++++ inputPath: {input_path}')
    logging.debug(f'++++++ outputPath: {output_path}')
    logging.debug(f'====== TODO: Implement - For now: Copy from Sort-Step')

    if current_dataset_key == '2012MorisienGramer':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2021MorisienDictionaryEnglish':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2021MorisienEducationalBooksPupil':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2021MorisienEducationalBooksTeacher':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    """
    Some ad-hoc text cleaning from previous experiments - Pre December 2023.
    """
    if current_dataset_key == '2023DevVirahsawmyBoukieBananePDF':
        sort_path = f'{input_path}{current_dataset_key}/'
        clean_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(clean_path)
        
        # Note: Should actually be only a single file at this point.
        # Iterate over files in that directory
        for filename in os.listdir(sort_path):
            f = os.path.join(sort_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # ================================
                # Sentences
                current_content = []

                # Combine all lines into one
                one_line = ""

                for line in text_lines_current_file:
                    # Also remove all line breaks
                    one_line = one_line + line.replace('\n', '')

                # Replace all special characters with a space
                one_line_no_special = re.sub('[^A-Za-z0-9.,!?:;()]+', ' ', one_line)

                # Replace all single characters with a space
                one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
                
                # Replace all double spaces with one space
                one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
                
                # Remove leading and trailing spaces
                one_line_stripped = one_line_no_doublespace.strip()
                

                one_line_split = one_line_stripped.split('.')
                #logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

                for sentence in one_line_split:
                    current_content.append(sentence+'.')

                # Save text file
                util_ge.write_text_file_lines(f'{clean_path}{current_filename}', current_content)

        # Old code for simple copying of the files:
        #move_files_from_directory(input_path, output_path, current_dataset_key)
        util_ge.rename_files_in_directory(f'{output_path}{current_dataset_key}/', "right", 3)

    if current_dataset_key == '2023DevVirahsawmyBoukieBananeWeb':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)
        util_ge.rename_files_in_directory(f'{output_path}{current_dataset_key}/', "right", 3)


""" INPUT parameter: 
    info_datasets_ready,          # Only select datasets marked "ready"
    data_raw_dataset_path,        # Location of raw data to clean
    data_transform_datasets_path, # (Temp) Location for transformed data
    data_sort_datasets_path,      # (Temp) Location for sorted data
    data_clean_datasets_path,     # Location for cleaned data
    execute_transforming,         # Flag if transforming step should be done (default=True)
    execute_sorting,              # Flag if sorting step should be done (default=True)
    execute_cleaning              # Flag if cleaning step should be done (default=True) 
"""
def main(info_datasets_ready, 
         data_raw_dataset_path, 
         data_transform_datasets_path, 
         data_sort_datasets_path, 
         data_clean_datasets_path,
         execute_transforming,
         execute_sorting,
         execute_cleaning):

    logging.debug(f'TODO: Build upon the download.py script for webdata, once the Raman-Selenium integration has been done.')
    logging.debug(f'TODO: OR: At least the file formats are known and certain not to change later on.')

    # Process all datasets for which info was provided:
    for key in info_datasets_ready.keys():
        current_dataset_key = key

        # Processing capabilities guaranteed for following datasets
        available_webdata_keys = [
            '2012MorisienGramer',
            '2021MorisienDictionaryEnglish',
            '2021MorisienEducationalBooksPupil',
            #'2021MorisienEducationalBooksTeacher',
            '2023DevVirahsawmyBoukieBananePDF',
            '2023DevVirahsawmyBoukieBananeWeb']
        
        if current_dataset_key in available_webdata_keys:
            logging.debug(f'====   Dataset: {current_dataset_key}')
            
            # Take the entire dataset (info) and continue
            current_dataset_info = info_datasets_ready[key]

            if execute_transforming == True:
                transform_data(current_dataset_key,
                               current_dataset_info,
                               data_raw_dataset_path,
                               data_transform_datasets_path)

            if execute_sorting == True:
                sort_data(current_dataset_key,
                          current_dataset_info,
                          data_transform_datasets_path,
                          data_sort_datasets_path)

            if execute_cleaning == True:
                clean_data(current_dataset_key,
                           current_dataset_info,
                           data_sort_datasets_path,
                           data_clean_datasets_path)


if __name__ == "__main__":
    main()

