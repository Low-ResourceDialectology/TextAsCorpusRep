# -*- coding: utf-8 -*-
# Python Script to sort data by "Word vs. Sentence" and "Mono- vs.  Bi- vs. Multi-lingual"
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################


import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 
import json
import logging
import os
import shutil
import sys

import utilities as util


def main(languages, inputPath, outputPath, dataset_list):

    #logging.info(f'  Sorting datasets')
    #logging.debug(f'languages: {languages}')
    #logging.debug(f'inputPath: {inputPath}')
    #logging.debug(f'outputPath: {outputPath}')
    #logging.debug(f'dataset_list: {dataset_list}')

    
    # ===========================================
    # MONOLINGUAL
    # ===========================================
    def sort_dataset(transform_path, sort_path):

        # Create directory if not existing
        util.create_directory(sort_path)

        # For each file in the directory
        for filename in os.listdir(transform_path):
            # Combine the directory path with the filename
            text_file = os.path.join(transform_path, filename)
            
            # Checking if it is a file
            if os.path.isfile(text_file):
                        
                logging.debug(f'  Sorting: {text_file}')

                # Get file information
                f_basename = util.get_basename(text_file)
                #logging.debug(f'    f_basename: {f_basename}')
                f_ending = util.get_fileending(text_file)
                #logging.debug(f'    f_ending: {f_ending}')
                #f_size = util.get_filesize_b(text_file)
                #logging.debug(f'    f_size: {f_size}')

                #
                # Monolingual vs. Bilingual → Monolingual
                #
                if f_basename == f_ending:
                    
                    sort_path_mono = sort_path + 'Monolingual/'
                    util.create_directory(sort_path_mono)

                    text_words = []
                    text_sents = []

                    text_data = util.read_text_file(text_file)

                    for line in text_data:

                        # Check if only a single word
                        if len(line.split(' ')) is 1:
                            text_words.append(line)
                        
                        # Otherwise multiple words
                        else:
                            text_sents.append(line)
                    
                    # Once all lines have been checked, write text (words & sents) to file

                    # In case the data contained single words
                    if len(text_words) > 0:
    
                        output_file_words = sort_path_mono + 'Words/'
                        util.create_directory(output_file_words)
                        util.write_text_file(output_file_words+f'{f_basename}.{f_ending}', text_words)

                    # In case the data contained sentences
                    if len(text_sents) > 0:

                        output_file_sents = sort_path_mono + 'Sentences/'
                        util.create_directory(output_file_sents)
                        util.write_text_file(output_file_sents+f'{f_basename}.{f_ending}', text_sents)
                    # utils.write_text_file(output_file, text_words)
                    # or
                    # write_text_file_lines(output_file, text_words)
                
                #
                # Monolingual vs. Bilingual → Bilingual
                #
                else:

                    sort_path_bili = sort_path + 'Bilingual/'
                    util.create_directory(sort_path_bili)

                    text_words = []
                    text_sents = []

                    text_data = util.read_text_file(text_file)

                    for line in text_data:

                        # Check if only a single word
                        if len(line.split(' ')) is 1:
                            text_words.append(line)
                        
                        # Otherwise multiple words
                        else:
                            text_sents.append(line)
                    
                    # Once all lines have been checked, write text (words & sents) to file

                    # In case the data contained single words
                    if len(text_words) > 0:
    
                        output_file_words = sort_path_bili + 'Words/'
                        util.create_directory(output_file_words)
                        util.write_text_file(output_file_words+f'{f_basename}.{f_ending}', text_words)

                    # In case the data contained sentences
                    if len(text_sents) > 0:

                        output_file_sents = sort_path_bili + 'Sentences/'
                        util.create_directory(output_file_sents)
                        util.write_text_file(output_file_sents+f'{f_basename}.{f_ending}', text_sents)
                    # utils.write_text_file(output_file, text_words)
                    # or
                    # write_text_file_lines(output_file, text_words)
       

    # ===========================================
    # Morisien 
    # ===========================================
    if '2022DabreMorisienMT' in dataset_list:

        transform_path = inputPath + '2022DabreMorisienMT/'
        sort_path = outputPath + '2022DabreMorisienMT/'
        logging.debug(f'  transform_path: {transform_path}')
        logging.debug(f'  sort_path: {sort_path}')
        sort_dataset(transform_path, sort_path)
        

    # ===========================================
    # Kurmanji 
    # ===========================================
    if '2022AhmadiInterdialect' in dataset_list:

        transform_path = inputPath + '2022AhmadiInterdialect/'
        sort_path = outputPath + '2022AhmadiInterdialect/'
        logging.debug(f'  transform_path: {transform_path}')
        logging.debug(f'  sort_path: {sort_path}')
        sort_dataset(transform_path, sort_path)
        

    # ===========================================
    # Vietnamese 
    # ===========================================
    if '2017LuongNMT' in dataset_list:

        transform_path = inputPath + '2017LuongNMT/'
        sort_path = outputPath + '2017LuongNMT/'
        logging.debug(f'  transform_path: {transform_path}')
        logging.debug(f'  sort_path: {sort_path}')
        sort_dataset(transform_path, sort_path)
        
        

                


