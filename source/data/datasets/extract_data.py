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


""" INPUT parameter: 
    info_datasets_ready,          # Dictionary of only select datasets marked "ready"
    data_clean_datasets_path,     # Location of cleaned data (datasets)
    data_clean_webdata_path,      # Location of cleaned data (webdata)
    data_monolingual_plain_path,  # Location for (mono) clean language data
    data_multingual_plain_path,   # Location for (multi) clean language data
    languages_selected,
    executionMode                 # such as 'None' or 'count'
"""
def main(info_datasets_ready, 
         data_clean_datasets_path, 
         data_clean_webdata_path, 
         data_monolingual_plain_path, 
         data_multingual_plain_path,
         languages_selected,
         executionMode):
    
    #logging.debug(f'info_datasets_ready: {info_datasets_ready}')

    """
    From clean data to plain-mono and plain-multi
    """
    def extract_from_datasets(
            info_datasets_ready,
            data_clean_datasets_path, 
            data_clean_webdata_path,
            data_monolingual_plain_path, 
            data_multingual_plain_path):
        
        logging.debug(f'====== Extracting data from datasets')
        logging.debug(f'++++++ inputPath: {data_clean_datasets_path}')
        logging.debug(f'++++++ outputPath (mono): {data_monolingual_plain_path}')
        logging.debug(f'++++++ outputPath (multi): {data_multingual_plain_path}')

        selected_dataset_keys = info_datasets_ready.keys()
        logging.debug(f'++++++ Dataset Keys: {selected_dataset_keys}')

        # Create directories if not existing
        util_ge.create_directory(data_monolingual_plain_path)
        util_ge.create_directory(data_multingual_plain_path)

        # NOTE: This would quickly grow out of hand for many datasets and languages
        # Get the paths to all clean datasets
        #clean_datasets = glob.glob(f'{data_clean_datasets_path}/*')
        #for clean_dataset in clean_datasets:

        # For each clean data directory (dataset)
        for clean_dataset_name in selected_dataset_keys:

            logging.debug(f'Current clean dataset name:   {clean_dataset_name}')
            clean_dataset = f'{data_clean_datasets_path}{clean_dataset_name}/'

            # Get dataset "Info" such as "Origin or data" and "References" 
            info_key = clean_dataset_name
            info_name = info_datasets_ready[clean_dataset_name]["Name"]
            info_year = info_datasets_ready[clean_dataset_name]["Year"]
            info_url = info_datasets_ready[clean_dataset_name]["URL"]

            dataset_info = {
                "Key":info_key,
                "Name":info_name,
                "Date":info_year,
                "URL":info_url
            } #TODO: Save to file → Maybe as tuples (text , info) ?

            # Get all files from current dataset
            clean_dataset_files = glob.glob(f'{clean_dataset}/*')
        
            # For each file in current dataset
            for clean_file in clean_dataset_files:

                clean_file_filename = util_ge.get_filename_without_extension(clean_file)
                clean_file_extension = util_ge.get_fileextension(clean_file)
                #logging.debug(f'Current clean file name:      {clean_file_filename}')
                #logging.debug(f'Current clean file extension: {clean_file_extension}')
                
                # Get additional "Info", specific to this file such as "Purpose" or "Alignments"
                # Check for alignments and other information from file-name

                # Filenames with a '-' have specific information prior to it
                # TODO: Handling File-Info: Either work via this name, or start collecting "Info" and "Metadata" in earlier steps?
                if '-' in clean_file_filename:
                    filename_info = clean_file_filename.split('-')[0]
                    clean_file_filename = clean_file_filename.split('-')[1]

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

                
                output_file_names = []
                output_info_file_names = []

                # Filenames with the same lang_id as their extension are monolingual and will have the same
                #   string for "aligned language" as for "content language"
                if clean_file_extension in filename_alignments_list:
                    #monolingual_data = True
                    output_file_path = f'{data_monolingual_plain_path}{clean_file_extension}/'
                    
                    for aligned_language in filename_alignments_list:
                        new_output_file_name = f'{aligned_language}.{clean_file_extension}'
                        output_file_names.append(new_output_file_name)
                        
                        new_output_info_file_name = f'{aligned_language}-{clean_file_extension}.info'
                        output_info_file_names.append(new_output_info_file_name)
                else:
                    #monolingual_data = False
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
                    text_line_length = len(clean_text_line.split())
                    # → "Find a better way" → 4

                    # =========================================================
                    # Current Content is "Word"
                    if text_line_length <= 1: 
                        content_type = 'word'

                        # Handle special cases such as: Lekonomi/lanplwa.
                        if '/' in clean_text_line:
                            words_from_line = clean_text_line.split('/')

                            # Clean each word from line
                            for word in words_from_line:
                                clean_text_line = util_ge.text_line_remove_special_characters_punctuation(word)

                                # Save each word from line
                                for output_file_name in output_file_names:
                                    # Writing clean test data to output file # TODO: Repeated executions will introduce duplicates!
                                    util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)

                        # Handle special cases such as: Lekonomi\lanplwa.
                        elif '\\' in clean_text_line:
                            words_from_line = clean_text_line.split('\\')

                            # Clean each word from line
                            for word in words_from_line:
                                clean_text_line = util_ge.text_line_remove_special_characters_punctuation(word)

                                # Save each word from line
                                for output_file_name in output_file_names:
                                    # Writing clean test data to output file # TODO: Repeated executions will introduce duplicates!
                                    util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)

                        # Normal case
                        else:
                            clean_text_line = util_ge.text_line_remove_special_characters_punctuation(clean_text_line)

                            for output_file_name in output_file_names:
                                # Writing clean test data to output file # TODO: Repeated executions will introduce duplicates!
                                util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)

                    # =========================================================
                    # Current Content is "Sentence"
                    elif 1 < text_line_length <= 80:
                        content_type = 'sent'

                        for output_file_name in output_file_names:
                            # Writing clean test data to output file # TODO: Repeated executions will introduce duplicates!
                            util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)

                    # =========================================================
                    # Current Content is "Paragraph"
                    #elif 30 < text_line_length:
                    else:
                        content_type = 'para'

                        for output_file_name in output_file_names:
                            # Writing clean test data to output file # TODO: Repeated executions will introduce duplicates!
                            util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)

                    # If current content is word, change output location accordingly
                    #if len(clean_text_line.split(' ')) == 1:
                    #    content_type = 'word'
                    # If current content is sentence, change output location accordingly
                    #else:
                    #    content_type = 'sent'
                    # If current content is paragraph, change output location accordingly
                    # TODO: Not possible with current cleaning-process-setup

                    

                    # Get "Meta Data" (such as length of content, contained characters, encoding, ...)
                    # TODO: Move all the "Meta Data" stuff to a later part of processing pipeline to not overload this section here.
                    #clean_text_line_length = len(clean_text_line)

                    # Append the current "Content" AND the current "Info" AND "Meta Data"
                    # → So that the content and corresponding informations files stay aligned
                    #for output_file_name, output_info_file_name in output_file_names_and_info_file_names:
                #    for output_file_name in output_file_names:
                        # Writing clean test data to output file # TODO: Repeated executions will introduce duplicates!
                #        util_ge.write_text_file_append_plus_line(f'{output_file_path}{content_type}-{output_file_name}', clean_text_line)
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




    """
    From extracted data to wordlist and frequency dictionaries
    """
    def collect_and_count_words(
            languages_selected,
            data_monolingual_plain_path, 
            data_multingual_plain_path):
        
        logging.debug(f'====== Collecting and counting')
        logging.debug(f'++++++ inputPath (mono): {data_monolingual_plain_path}')
        logging.debug(f'++++++ inputPath (multi): {data_multingual_plain_path}')
        logging.debug(f'++++++ Languages: {languages_selected}')

        for language in languages_selected:

            logging.debug(f'Current language:   {language}')

            # =================================================================
            # Monolingual Data
            lang_data_path = f'{data_monolingual_plain_path}{language}/'
            logging.debug(f'Checking for dir: {lang_data_path}')

            # Check if monolingual data exists for this language
            if os.path.isdir(lang_data_path):
                #logging.debug(f'Target is a proper directory.')
                # All monolingual words for this language
                lang_words_count = {}                

                # Get all files for current language
                lang_files = glob.glob(f'{lang_data_path}/*')
            
                # For each file in current dataset
                for lang_file in lang_files:

                    lang_file_filename = util_ge.get_filename_without_extension(lang_file)
                    
                    # Filenames with a '-' have specific information prior to it
                    # In this case if file contains "word", "sent", or "para" text data
                    lang_file_info = lang_file_filename.split('-')[0]           # "word" | "sent" | "para"
                    lang_file_aligned = lang_file_filename.split('-')[1]        # "kmr" | "vie" | "mfe"
                    lang_file_content = util_ge.get_fileextension(lang_file)    # "kmr" | "vie" | "mfe"

                    # For words
                    if lang_file_info == 'word':
                        
                        current_text = util_ge.read_text_file(lang_file)
                        for line in current_text:
                            clean_word = util_ge.text_line_remove_special_characters_punctuation(line)

                            # For already encountered words
                            if clean_word in lang_words_count:
                                lang_words_count[clean_word] += 1
                            else:
                                lang_words_count[clean_word] = 1
                        
                    # For sentences
                    elif lang_file_info == 'sent' or lang_file_info == 'para':

                        current_text = util_ge.read_text_file(lang_file)
                        for line in current_text:

                            # Turn sentence into list of words
                            words_from_line = line.split()
                            
                            for word in words_from_line:
                                
                                clean_word = util_ge.text_line_remove_special_characters_punctuation(word)

                                # For already encountered words
                                if clean_word in lang_words_count:
                                    lang_words_count[clean_word] += 1
                                else:
                                    lang_words_count[clean_word] = 1

                    else:
                        print(f'Unknown data content identifier encountered: {lang_file_info}')
                    # For paragraphs
                    #elif lang_file_info == 'para':
                    #    pass

                # Once words from all files have been collected (and counted)
                # =============================================================
                # Sort them by their frequency 
                output_json_file_frequency = f'{lang_data_path}freqdict-{lang_file_aligned}.{lang_file_content}'

                lang_words_count_descending = sorted(lang_words_count.items(), key=lambda x:x[1], reverse=True)
                converted_lang_words_count_descending = dict(lang_words_count_descending)
                    
                # Serializing json
                json_object = json.dumps(converted_lang_words_count_descending, indent=4, ensure_ascii=False)
                
                # Writing to json file
                with open(output_json_file_frequency, "w") as outfile:
                    outfile.write(json_object)

                # =============================================================
                # Sort them alphabetically
                output_json_file_alphabetic = f'{lang_data_path}wordlist-{lang_file_aligned}.{lang_file_content}'

                lang_words_alphabetic = sorted(list(lang_words_count.keys()))
                util_ge.write_text_file_lines(output_json_file_alphabetic, lang_words_alphabetic)

                #converted_lang_words_alphabetic = dict(lang_words_alphabetic)
                    
                # Serializing json
                #json_object = json.dumps(converted_lang_words_alphabetic, indent=4, ensure_ascii=False)
                
                # Writing to json file
                #with open(output_json_file_alphabetic, "w") as outfile:
                #    outfile.write(json_object)


            # =================================================================
            # Multilingual Data
            lang_data_path = f'{data_multingual_plain_path}{language}/'
            logging.debug(f'Checking for dir: {lang_data_path}')

            # Check if multilingua data exists for this language
            if os.path.isdir(lang_data_path):
                
                # A dictionary for each aligned language inside this dictionarie
                lang_dictionaries = {}

                # Get all files for current language
                lang_files = glob.glob(f'{lang_data_path}/*')
            
                # For each file in current dataset
                for lang_file in lang_files:

                    lang_file_filename = util_ge.get_filename_without_extension(lang_file)
                    
                    # Filenames with a '-' have specific information prior to it
                    # In this case if file contains "word", "sent", or "para" text data
                    lang_file_info = lang_file_filename.split('-')[0]           # "word" | "sent" | "para"
                    lang_file_aligned = lang_file_filename.split('-')[1]         # "kmr" | "vie" | "mfe"
                    lang_file_content = util_ge.get_fileextension(lang_file)    # "kmr" | "vie" | "mfe"

                    # In case another file belonging to this aligned language was already processed
                    if lang_file_aligned in lang_dictionaries.keys():
                        # All monolingual words for this language
                        #NOTE-Already exists: lang_dictionaries[lang_file_aligned] = {}
                        #     lang_dictionaries { "lang_file_aligned": {"word1": 1, "word2": 1, ...}

                        # TODO-Refactor: The following block might as well be its own function 
                        # For words
                        if lang_file_info == 'word':
                            
                            current_text = util_ge.read_text_file(lang_file)
                            for line in current_text:
                                clean_word = util_ge.text_line_remove_special_characters_punctuation(line)

                                # For already encountered words
                                if clean_word in lang_dictionaries[lang_file_aligned]:
                                    lang_dictionaries[lang_file_aligned][clean_word] += 1
                                else:
                                    lang_dictionaries[lang_file_aligned][clean_word] = 1
                            
                        # For sentences
                        elif lang_file_info == 'sent' or lang_file_info == 'para':

                            current_text = util_ge.read_text_file(lang_file)
                            for line in current_text:

                                # Turn sentence into list of words
                                words_from_line = line.split()
                                
                                for word in words_from_line:
                                    
                                    clean_word = util_ge.text_line_remove_special_characters_punctuation(word)

                                    # For already encountered words
                                    if clean_word in lang_dictionaries[lang_file_aligned]:
                                        lang_dictionaries[lang_file_aligned][clean_word] += 1
                                    else:
                                        lang_dictionaries[lang_file_aligned][clean_word] = 1

                        else:
                            print(f'Unknown data content identifier encountered: {lang_file_info}')
                        # For paragraphs
                        #elif lang_file_info == 'para':
                        #    pass


                    # In case of this being the first file of this aligned language
                    else:
                        # All monolingual words for this language
                        lang_dictionaries[lang_file_aligned] = {}

                        # For words
                        if lang_file_info == 'word':
                            
                            current_text = util_ge.read_text_file(lang_file)
                            for line in current_text:
                                clean_word = util_ge.text_line_remove_special_characters_punctuation(line)

                                # For already encountered words
                                if clean_word in lang_dictionaries[lang_file_aligned]:
                                    lang_dictionaries[lang_file_aligned][clean_word] += 1
                                else:
                                    lang_dictionaries[lang_file_aligned][clean_word] = 1
                            
                        # For sentences
                        elif lang_file_info == 'sent' or lang_file_info == 'para':

                            current_text = util_ge.read_text_file(lang_file)
                            for line in current_text:

                                # Turn sentence into list of words
                                words_from_line = line.split()
                                
                                for word in words_from_line:
                                    
                                    clean_word = util_ge.text_line_remove_special_characters_punctuation(word)

                                    # For already encountered words
                                    if clean_word in lang_dictionaries[lang_file_aligned]:
                                        lang_dictionaries[lang_file_aligned][clean_word] += 1
                                    else:
                                        lang_dictionaries[lang_file_aligned][clean_word] = 1

                        else:
                            print(f'Unknown data content identifier encountered: {lang_file_info}')
                        # For paragraphs
                        #elif lang_file_info == 'para':
                        #    pass

                # Once words from all files have been collected (and counted)
                # The following takes care of each dictionary (aligned language) collected
                for lang_key in lang_dictionaries.keys():
                    # While processing the "mfe" data-directory, "language" == "mfe"
                    #   while processing the aligned data for "fra", lang_key == "fra"
                    lang_file_aligned = lang_key
                    lang_file_content = language
                    lang_words_count = lang_dictionaries[lang_key]

                    # =============================================================
                    # Sort them by their frequency 
                    output_json_file_frequency = f'{lang_data_path}freqdict-{lang_file_aligned}.{lang_file_content}'

                    lang_words_count_descending = sorted(lang_words_count.items(), key=lambda x:x[1], reverse=True)
                    converted_lang_words_count_descending = dict(lang_words_count_descending)
                        
                    # Serializing json
                    json_object = json.dumps(converted_lang_words_count_descending, indent=4, ensure_ascii=False)
                    
                    # Writing to json file
                    with open(output_json_file_frequency, "w") as outfile:
                        outfile.write(json_object)

                    # =============================================================
                    # Sort them alphabetically
                    output_json_file_alphabetic = f'{lang_data_path}wordlist-{lang_file_aligned}.{lang_file_content}'

                    lang_words_alphabetic = sorted(list(lang_words_count.keys()))
                    util_ge.write_text_file_lines(output_json_file_alphabetic, lang_words_alphabetic)
                    
                    #converted_lang_words_alphabetic = dict(lang_words_alphabetic)
                        
                    # Serializing json
                    #json_object = json.dumps(converted_lang_words_alphabetic, indent=4, ensure_ascii=False)
                    
                    # Writing to json file
                    #with open(output_json_file_alphabetic, "w") as outfile:
                    #    outfile.write(json_object)


    # =========================================================================
    # Execution
    # 
    if executionMode == 'None':
        # Start extraction from clean data based on datasets
        extract_from_datasets(
            info_datasets_ready,
            data_clean_datasets_path, 
            data_clean_webdata_path,
            data_monolingual_plain_path, 
            data_multingual_plain_path
            )
    elif executionMode == 'count':
        collect_and_count_words(
            languages_selected,
            data_monolingual_plain_path, 
            data_multingual_plain_path
            )

    # Start extraction from clean data based on webdata
    # TODO: Implement
    #extract_from_datasets(data_clean_webdata_path,data_monolingual_plain_path,data_multingual_plain_path)



if __name__ == "__main__":
    main()