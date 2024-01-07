# -*- coding: utf-8 -*-
# Python Script for extracting texts from cleaned data into a (corpus-like) format
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import glob
import json
import logging
import os
import re
import shutil
import sys

# Enable importing the other scripts by adding their location to the python-path
sys.path.append(r"./../../")

import utils.utilities_general as util_ge


def extract_from_datasets(
        data_clean_datasets_path, 
        data_monolingual_plain_path, 
        data_multingual_plain_path):
    
    logging.debug(f'====== Extracting data from datasets')
    logging.debug(f'++++++ inputPath: {data_clean_datasets_path}')
    logging.debug(f'++++++ outputPath (mono): {data_monolingual_plain_path}')
    logging.debug(f'++++++ outputPath (multi): {data_multingual_plain_path}')

    # Create directories if not existing
    util_ge.create_directory(data_monolingual_plain_path)
    util_ge.create_directory(data_multingual_plain_path)

    # Get the paths to all clean datasets
    clean_datasets = glob.glob(f'{data_clean_datasets_path}/*')

    # For each clean data directory (dataset)
    for clean_dataset in clean_datasets:

        # Dataset name/key and "Info"
        clean_dataset_name = util_ge.get_filename_without_extension(clean_dataset)
        logging.debug(f'Current clean dataset name:   {clean_dataset_name}')

        # Get all files from current dataset
        clean_dataset_files = glob.glob(f'{clean_dataset}/*')
    
        # For each file in current dataset
        for clean_file in clean_dataset_files:

            # Get dataset "Info" such as "Origin or data" and "References" 
            clean_file_filename = util_ge.get_filename_without_extension(clean_file)
            clean_file_extension = util_ge.get_fileextension(clean_file)
            #logging.debug(f'Current clean file name:      {clean_file_filename}')
            #logging.debug(f'Current clean file extension: {clean_file_extension}')
            
            # Get additional "Info", specific to this file such as "Purpose" or "Alignments"
            # Check for alignments and other information from file-name

            # Filenames with a '-' have specific information prior to it
            # TODO: Handling File-Info: Either work via this name, or start collecting "Info" and "Metadata" in earlier steps?
            if '-' in clean_file_filename:
                filename_info = clean_file_filename.rsplit('-',0)
                clean_file_filename = clean_file_filename.rsplit('-',1)

            # Collect all alignments of current file to later create output files accordingly
            filename_alignments_list = []

            # Filenames with a '_' have multiple aligned languages
            if ('_') in clean_file_filename:
                filename_alignments_string = clean_file_filename
                
                for alignment in filename_alignments_string.split('_'):
                    filename_alignments_list.append(alignment)
                    # e.g. → ["deu", "eng"] with the extension "fra" in dataset "2016ElliottMulti30k"

            # Filenames without a '_' have just a single aligned language
            else:
                filename_alignments_list.append(clean_file_filename[-3:])

            # Filenames with the same lang_id as their extension are monolingual and will have the same
            #   string for "aligned language" as for "content language"
            if clean_file_extension in filename_alignments_list:
                monolingual_data = True
            else:
                monolingual_data = False

            output_file_names = []
            output_info_file_names = []
            if monolingual_data == True:
                output_file_path = f'{data_monolingual_plain_path}{clean_file_extension}/'
                
                for aligned_language in filename_alignments_list:
                    new_output_file_name = f'{aligned_language}.{clean_file_extension}'
                    output_file_names.append(new_output_file_name)
                    
                    new_output_info_file_name = f'{aligned_language}-{clean_file_extension}.info'
                    output_info_file_names.append(new_output_info_file_name)
            else: # "Multilingual == True"
                output_file_path = f'{data_multingual_plain_path}{clean_file_extension}/'

                for aligned_language in filename_alignments_list:
                    new_output_file_name = f'{aligned_language}.{clean_file_extension}'
                    output_file_names.append(new_output_file_name)

                    new_output_info_file_name = f'{aligned_language}-{clean_file_extension}.info'
                    output_info_file_names.append(new_output_info_file_name)

            # Combine "file names" and "info file names" to always be linked together
            #output_file_names_and_info_file_names = zip(output_file_names, output_info_file_names)

            # Create directory if not existing
            util_ge.create_directory(output_file_path)
            
            # Read current file content
            clean_file_content = util_ge.read_text_file(clean_file)
            #clean_file_example = clean_file_content[0]
            #logging.debug(f'Current clean data example:   {clean_file_example}')
            #logging.debug(f'Current clean file length:    {len(clean_file_content)}')

            # For each line in current file
            for clean_text_line in clean_file_content:

                # Check (somehow?) if word, sentence, or paragraph
                # TODO: Find better way than splitting on whitespace
                # If current content is word, change output location accordingly
                #if len(clean_text_line.split(' ')) == 1:
                #    content_type = 'word'
                # If current content is sentence, change output location accordingly
                #else:
                #    content_type = 'sent'
                # If current content is paragraph, change output location accordingly
                # TODO: Not possible with current cleaning-process-setup

                content_type = 'data'

                # Get "Meta Data" (such as length of content, contained characters, encoding, ...)
                # TODO: Move all the "Meta Data" stuff to a later part of processing pipeline to not overload this section here.
                #clean_text_line_length = len(clean_text_line)

                # Append the current "Content" AND the current "Info" AND "Meta Data"
                # → So that the content and corresponding informations files stay aligned
                #for output_file_name, output_info_file_name in output_file_names_and_info_file_names:
                for output_file_name in output_file_names:
                    # Writing clean test data to output file
                    util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)
                    #logging.debug(f'File to append to+: {output_file_path}{content_type}-{output_file_name}')
                    #util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_info_file_name}',f'{filename_info}\t{clean_text_line_length}')
                    
                    # Quick-Fix for weird filenaming (Pair-Programming with Myy)
                    #name_part_01 = output_file_name.rsplit(".",1)
                    #logging.debug(f'name_part_01: {name_part_01}')
                    #output_info_file_name = f'{name_part_01[0]}-{name_part_01[1]}.info'
                    
                    #util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_info_file_name}',f'{clean_text_line_length}')
                    #logging.debug(f'File for info to append to+: {output_file_path}{content_type}-{output_info_file_name}')


            #sys.exit()

def extract_from_webdata(
        data_clean_webdata_path, 
        data_monolingual_plain_path, 
        data_multingual_plain_path):
    pass
    # For each clean data directory (webdata)

        # Get dataset "Info" such as "Origin or data" and "References" 


        # For each file in current dataset

            # Get additional "Info", specific to this file such as "Purpose" or "Alignments"
    

            # For each line in current file
    
                # Check (somehow?) if word, sentence, or paragraph
    

                # If current content is word, change output location accordingly
    
    
                # If current content is sentence, change output location accordingly
    

                # If current content is paragraph, change output location accordingly
    

                # Get "Meta Data" (such as length of content, contained characters, encoding, ...)


                # Append the current "Content" AND the current "Info" AND "Meta Data"
                # → So thatthe content and corresponding informations files stay aligned


""" INPUT parameter: 
    info_datasets_ready,          # Only select datasets marked "ready"
    data_clean_datasets_path,     # Location of cleaned data (datasets)
    data_clean_webdata_path,      # Location of cleaned data (webdata)
    data_monolingual_plain_path,  # Location for (mono) clean language data
    data_multingual_plain_path)  # Location for (multi) clean language data
"""
def main(info_datasets_ready, 
         data_clean_datasets_path, 
         data_clean_webdata_path, 
         data_monolingual_plain_path, 
         data_multingual_plain_path):
    
    # Start extraction from clean data based on datasets
    extract_from_datasets(data_clean_datasets_path,data_monolingual_plain_path,data_multingual_plain_path)

    # Start extraction from clean data based on webdata
    # TODO: Implement
    #extract_from_datasets(data_clean_webdata_path,data_monolingual_plain_path,data_multingual_plain_path)


if __name__ == "__main__":
    main()