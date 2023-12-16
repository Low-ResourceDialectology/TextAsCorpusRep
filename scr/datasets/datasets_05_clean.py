# -*- coding: utf-8 -*-
# Python Script to clean data that has been sorted
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

    #logging.info(f'  Cleaning datasets')
    #logging.debug(f'languages: {languages}')
    #logging.debug(f'inputPath: {inputPath}')
    #logging.debug(f'outputPath: {outputPath}')
    #logging.debug(f'dataset_list: {dataset_list}')

    # ===========================================
    # MONOLINGUAL
    # ===========================================
    def clean_monolingual(sort_path, clean_path):
        
        # Create directory if not existing
        util.create_directory(clean_path)

        #
        # Check for monolingual data directories
        #
        if os.path.isdir(sort_path+'Monolingual'):
            
            #
            # Check for words data directories
            #
            if os.path.isdir(sort_path+'Monolingual/Words'):
                
                sort_path_mono_words = sort_path+'Monolingual/Words/'

                # For each file in the directory
                for filename in os.listdir(sort_path_mono_words):
                    # Combine the directory path with the filename
                    text_file = os.path.join(sort_path_mono_words, filename)
                    
                    # Checking if it is a file
                    if os.path.isfile(text_file):
                                
                        logging.debug(f'    Sorting: {text_file}')

                        f_basename = util.get_basename(text_file)
                        f_ending = util.get_fileending(text_file)

                        clean_path_mono_words = clean_path + 'Monolingual/Words/'
                        util.create_directory(clean_path_mono_words)

                        text_words = []

                        text_data = util.read_text_file(text_file)

                        for line in text_data:

                            # Remove punctuation at end of word
                            word = util.remove_punctuation_end(line.replace("\n", ""))
                            text_words.append(word)
                        
                        util.write_text_file_lines(clean_path_mono_words+f'{f_basename}.{f_ending}', text_words)

            #
            # Check for sentences data directories
            #
            if os.path.isdir(sort_path+'Monolingual/Sentences'):
                
                sort_path_mono_sents = sort_path+'Monolingual/Sentences/'

                # For each file in the directory
                for filename in os.listdir(sort_path_mono_sents):
                    # Combine the directory path with the filename
                    text_file = os.path.join(sort_path_mono_sents, filename)
                    
                    # Checking if it is a file
                    if os.path.isfile(text_file):
                                
                        logging.debug(f'    Sorting: {text_file}')

                        f_basename = util.get_basename(text_file)
                        f_ending = util.get_fileending(text_file)

                        clean_path_mono_sents = clean_path + 'Monolingual/Sentences/'
                        util.create_directory(clean_path_mono_sents)

                        text_sents = []

                        text_data = util.read_text_file(text_file)

                        for line in text_data:

                            # TODO: clean sentences
                            #sent = util.remove_punctuation_end(line)
                            #text_sents.append(sent)
                            text_sents.append(line.replace("\n", ""))
                        
                        util.write_text_file_lines(clean_path_mono_sents+f'{f_basename}.{f_ending}', text_sents)


    # ===========================================
    # BILINGUAL
    # ===========================================
    def clean_bilingual(sort_path, clean_path):
        #
        # Check for bilingual data directories
        #
        if os.path.isdir(sort_path+'Bilingual'):
                
            #
            # Check for words data directories
            #
            if os.path.isdir(sort_path+'Bilingual/Words'):
                
                sort_path_mono_words = sort_path+'Bilingual/Words/'

                # For each file in the directory
                for filename in os.listdir(sort_path_mono_words):
                    # Combine the directory path with the filename
                    text_file = os.path.join(sort_path_mono_words, filename)
                    
                    # Checking if it is a file
                    if os.path.isfile(text_file):
                                
                        logging.debug(f'    Sorting: {text_file}')

                        f_basename = util.get_basename(text_file)
                        f_ending = util.get_fileending(text_file)

                        clean_path_mono_words = clean_path + 'Bilingual/Words/'
                        util.create_directory(clean_path_mono_words)

                        text_words = []

                        text_data = util.read_text_file(text_file)

                        for line in text_data:

                            # Remove punctuation at end of word
                            #print(type(line)) → <class 'str'>
                            word = util.remove_punctuation_end(line.replace("\n", ""))
                            text_words.append(word)
                        
                        util.write_text_file_lines(clean_path_mono_words+f'{f_basename}.{f_ending}', text_words)

            #
            # Check for sentences data directories
            #
            if os.path.isdir(sort_path+'Bilingual/Sentences'):
                
                sort_path_mono_sents = sort_path+'Bilingual/Sentences/'

                # For each file in the directory
                for filename in os.listdir(sort_path_mono_sents):
                    # Combine the directory path with the filename
                    text_file = os.path.join(sort_path_mono_sents, filename)
                    
                    # Checking if it is a file
                    if os.path.isfile(text_file):
                                
                        logging.debug(f'    Sorting: {text_file}')

                        f_basename = util.get_basename(text_file)
                        f_ending = util.get_fileending(text_file)

                        clean_path_mono_sents = clean_path + 'Bilingual/Sentences/'
                        util.create_directory(clean_path_mono_sents)

                        text_sents = []

                        text_data = util.read_text_file(text_file)

                        for line in text_data:

                            # TODO: clean sentences
                            #sent = util.remove_punctuation_end(line)
                            #text_sents.append(sent)
                            text_sents.append(line.replace("\n", ""))
                        
                        util.write_text_file_lines(sort_path_mono_sents+f'{f_basename}.{f_ending}', text_sents)


    # ===========================================
    # Morisien 
    # ===========================================
    if '2022DabreMorisienMT' in dataset_list:

        sort_path = inputPath + '2022DabreMorisienMT/'
        clean_path = outputPath + '2022DabreMorisienMT/'
        logging.debug(f'  sort_path: {sort_path}')
        logging.debug(f'  clean_path: {clean_path}')
        clean_monolingual(sort_path, clean_path)
        clean_bilingual(sort_path, clean_path)
    

    # ===========================================
    # Kurmanji 
    # ===========================================
    if '2022AhmadiInterdialect' in dataset_list:

        sort_path = inputPath + '2022AhmadiInterdialect/'
        clean_path = outputPath + '2022AhmadiInterdialect/'
        logging.debug(f'  sort_path: {sort_path}')
        logging.debug(f'  clean_path: {clean_path}')
        clean_monolingual(sort_path, clean_path)
        clean_bilingual(sort_path, clean_path)
    
    # ===========================================
    # Vietnamese 
    # ===========================================
    if '2017LuongNMT' in dataset_list:

        sort_path = inputPath + '2017LuongNMT/'
        clean_path = outputPath + '2017LuongNMT/'
        logging.debug(f'  sort_path: {sort_path}')
        logging.debug(f'  clean_path: {clean_path}')
        clean_monolingual(sort_path, clean_path)
        clean_bilingual(sort_path, clean_path)
    

        
        

        
        

