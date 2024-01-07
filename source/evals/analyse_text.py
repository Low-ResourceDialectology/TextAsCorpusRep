# -*- coding: utf-8 -*-
# Python Script for analysing text data of various stages of the processing pipeline
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import json
import logging
import os
import re
import shutil
import sys

# Enable importing the other scripts by adding their location to the python-path
sys.path.append(r"./../../")

import utils.utilities_general as util_ge

"""
From cleaned and "plain" text data to 
    - documents holding "sentences" and "words" 
    - tables holding corresponding numbers
    - plots showing the data distributions
"""

# TODO: From analyse_text_content.py
# ===========================================
# By Language - COUNT SENTENCES & COUNT WORDS
# ===========================================
def count_text_data(input_path, filenames, intermediate_seednllb, output_path, dataset_language, dataset_name):

    # Create directory if not existing
    util.create_directory(output_path)
    current_filename = util.get_basename(input_path+dataset_name)

    text_content = []
    # Collect all text from all files into "text_content"
    for filename in filenames:
        current_file_in = input_path+filename
        text_lines = util.read_text_file(current_file_in)
        for line in text_lines:
            text_content.append(line)
    # → text_content = [ from_file_one, from_file_two, ... ]

    #
    # Still containing duplicates in the data
    #
    # Count text lines
    number_textlines = len(text_content)

    """
    # TODO: Handling multiple input files AND single input files
    if not dataset_name == "NLLB Seed":
        # Turn text into sentences
        all_text_one_string = ""
        for line in text_content:
            for string in line:
                all_text_one_string + string

        sentences_all = util.split_text_into_sentences(all_text_one_string)
    else:
        sentences_all = text_content
    """
    sentences_all = text_content

    # Count sentences
    number_sentences = len(sentences_all)
    
    """
    # Count words (first attempt)
    # This does not make sense... But why?
    number_words_all = 0
    words_all_unique = []
    for sent in sentences_all:
        for word in sent:
            number_words_all += 1
            if not word in words_all_unique:
                words_all_unique.append(word)
    # → 876015 words and only 208 unique words?!?!
    """
    # Build frequency dictionary (just for counting words . . .)
    word_frequency_dictionary = {}
    for sent in sentences_all:
        for word in sent.split():
            if word not in word_frequency_dictionary:
                word_frequency_dictionary[word] = 1
            elif word in word_frequency_dictionary:
                word_frequency_dictionary[word] += 1

    # Count words
    number_words_all = 0
    for word in word_frequency_dictionary:
        number_words_all += word_frequency_dictionary[word]

    # Count unique words
    number_words_all_unique = len(word_frequency_dictionary)

    #
    # Now without any duplicated data
    #
    # Count unique text lines in unique data
    unique_textlines = []
    for text_line in text_content:
        if not text_line in unique_textlines:
            unique_textlines.append(text_line)

    number_textlines_unique = len(unique_textlines)

    # Count unique sentences in unique data
    unique_sentences = []
    for sentence in sentences_all:
        if not sentence in unique_sentences:
            unique_sentences.append(sentence)
    
    number_sentences_unique = len(unique_sentences)

    # Build frequency dictionary 
    word_frequency_dictionary_unique = {}
    for sent in unique_sentences:
        for word in sent.split():
            if word not in word_frequency_dictionary_unique:
                word_frequency_dictionary_unique[word] = 1
            elif word in word_frequency_dictionary_unique:
                word_frequency_dictionary_unique[word] += 1

    # Sort frequency dictionary 
    sorted_word_frequency_dictionary_unique = sorted(word_frequency_dictionary_unique.items(), key=lambda x:x[1], reverse = True)
    sorted_word_frequency_dictionary_unique = dict(sorted_word_frequency_dictionary_unique)

    # Count words in unique data
    unique_number_words = 0
    for word in sorted_word_frequency_dictionary_unique:
        unique_number_words += sorted_word_frequency_dictionary_unique[word]

    # Count unique words in unique data
    unique_number_words_unique = len(sorted_word_frequency_dictionary_unique) # Number of items in this dict is number of unique words
    
    # Serializing json
    json_object = json.dumps(sorted_word_frequency_dictionary_unique, indent=4)
    
    # Writing to sample.json
    with open(f'{intermediate_seednllb}{current_filename}-word_frequency_dictionary.json', "w") as outfile:
        outfile.write(json_object)
    
    

    metadata = {
        "Dataset Name":dataset_name,
        "Dataset Language":dataset_language,
        "Number of Lines":number_textlines,
        "Number of Sentences":number_sentences,
        "Number of Words (with duplicate sentences)":number_words_all,
        "Number of unique Words (with duplicate sentences)":number_words_all_unique,
        "Number of unique Lines":number_textlines_unique,
        "Number of unique Sentences":number_sentences_unique,
        "Number of Words":unique_number_words,
        "Number of unique Words":unique_number_words_unique,
    }

    # Serializing json
    metadata_json_object = json.dumps(metadata, indent=4)

    # Save all metadata/information to file
    with open(f'{intermediate_seednllb}{current_filename}-metadata.json', "w") as outfile:
        outfile.write(metadata_json_object)



"""

"""
def data_to_sentences():
    pass


"""

"""
def data_to_words():
    pass


"""

"""
def data_to_sents_and_words(languages_selected, data_path):

    # Iterate over language-directories in that directory
    for language_directory in os.listdir(data_path):
        # Checking if it is a directory and not maybe a file
        if os.path.isdir(language_directory):
            # Check if current language directory should be transformed
            current_language = util_ge.get_dir_basename(language_directory)
            if current_language in languages_selected:
                logging.debug(f'Transforming plain data for: {current_language}')

                # Iterate over files in that directory
                for filename in os.listdir(language_directory):
                    f = os.path.join(language_directory, filename)
                    # Checking if it is a file
                    if os.path.isfile(f):
                        # In case it is a "data" file
                        if filename.startswith('data'):
                            # Read text file to text lines 
                            text_lines_input = util_ge.read_text_file(f)
                            output_filename = filename.replace('.','-')
                            # e.g. "kmr.kmr" → "kmr-kmr"

                            # ========================
                            # TODO: SENTENCES

                            # Extract "complete" sentences from data into "output_filename.sent"
                            # TODO: Add parameter to define "complete" such as "min|max for number of words|characters"
                            data_to_sentences()
                            
                            
                            # ========================
                            # TODO: WORDS

                            # Extract all words from data into "output_filename.words"
                            # TODO: Then sort alphabetically
                            data_to_words()



"""

"""
def sentences_to_information():
    pass


"""

"""
def words_to_information():
    pass

"""

"""
def words_to_frequency_dictionary():
    pass


"""

"""
def analyse_monolingual(languages_selected, data_path, logs_path):

    # Not analysed languages
    languages_not_analysed = []

    # Iterate over language-directories in that directory
    for language_directory in os.listdir(data_path):
        # Checking if it is a directory and not maybe a file
        if os.path.isfile(language_directory):
            # Check if current language directory should be analysed
            current_language = util_ge.get_dir_basename(language_directory)
            if current_language in languages_selected:
                logging.debug(f'Analysing: {current_language}')

                # Iterate over files in that directory
                for filename in os.listdir(language_directory):
                    f = os.path.join(language_directory, filename)
                    # Checking if it is a file
                    if os.path.isfile(f):
                        # In case it is a "data" file
                        if filename.startswith('data'):
                            # Read text file to text lines 
                            text_lines_input = util_ge.read_text_file(f)
                            output_filename = filename.replace('.','-')
                            # e.g. "kmr.kmr" → "kmr-kmr"

                            # ========================
                            # TODO: SENTENCES

                            # TODO: (To logs) Get information about sentences such as "min|max|mean|median length"
                            sentences_to_information()

                            # ========================
                            # TODO: WORDS

                            # TODO: Create frequency dictionary from word file into "output_filename.freqdict"
                            words_to_frequency_dictionary()

                            # TODO: (To logs) Get information about words such as "min|max|mean|median length"
                            words_to_information()





            # If current language_directory shall not be analysed
            else:
                # Add language name to the list of not analysed ones
                if not current_language in languages_not_analysed:
                    languages_not_analysed.append(current_language)
            
    logging.debug(f'List of languages for which data exists, but not analysed: {languages_not_analysed}')



"""

"""
def visualize_analysis_logs(languages_selected, logs_path):

    # Iterate over language-directories in that directory
    for language_directory in os.listdir(data_path):
        # Checking if it is a directory and not maybe a file
        if os.path.isfile(language_directory):
            # Check if current language directory should be analysed
            current_language = util_ge.get_dir_basename(language_directory)
            if current_language in languages_selected:
                logging.debug(f'Visualising: {current_language}')

                # Iterate over files in that directory
                for filename in os.listdir(language_directory):
                    f = os.path.join(language_directory, filename)
                    # Checking if it is a file
                    if os.path.isfile(f):
                        # In case it is a "data" file
                        if filename.startswith('data'):
                            # Read text file to text lines 
                            text_lines_input = util_ge.read_text_file(f)
                            output_filename = filename.replace('.','-')
                            # e.g. "kmr.kmr" → "kmr-kmr"




""" INPUT parameter: 
    languages_selected
    #info_datasets_ready ?
    list_of_data_paths_to_analyse = A list containing any of the following variables:
        data_raw_dataset_path,
        data_transform_datasets_path,
        data_sort_datasets_path,
        data_clean_datasets_path,
        data_raw_webdata_path,
        data_transform_webdata_path,
        data_sort_webdata_path,
        data_clean_webdata_path,
        data_monolingual_clean_path,
        data_monolingual_bronze_path,
        data_monolingual_silver_path,
        data_monolingual_gold_path,
        data_monolingual_platinum_path,
        data_multingual_bronze_path,
        data_multingual_silver_path,
        data_multingual_gold_path,
        data_multingual_platinum_path
"""
def main(
        languages_selected,
        #info_datasets_ready,
        list_of_data_paths_to_analyse,
        logs_path
        ):
    
    # TODO: Experiment with data formats to identify which sets can be processed by the same function to reduce redundancy
    # Parse each path from list of paths in order to customize analysis
    for data_path in list_of_data_paths_to_analyse:
        # Detect "stage" of the data
        base_path_data = data_path.split('/data/')[1]
        if '/raw/' in base_path_data:
            # Raw Text Data
            if '/datasets/' in base_path_data:
                # Raw Datasets
                logging.debug(f'Analysing raw datasets from: {data_path}')

            elif '/webdata/' in base_path_data:
                # Raw Webdata
                logging.debug(f'Analysing raw webdata from: {data_path}')

        if '/transform/' in base_path_data:
            # Transformed Text Data
            if '/datasets/' in base_path_data:
                # Transformed Datasets
                logging.debug(f'Analysing transformed datasets from: {data_path}')

            elif '/webdata/' in base_path_data:
                # Transformed Webdata
                logging.debug(f'Analysing transformed webdata from: {data_path}')

        if '/sort/' in base_path_data:
            # Sorted Text Data
            if '/datasets/' in base_path_data:
                # Sorted Datasets
                logging.debug(f'Analysing sorted datasets from: {data_path}')

            elif '/webdata/' in base_path_data:
                # Sorted Webdata
                logging.debug(f'Analysing sorted webdata from: {data_path}')

        if '/clean/' in base_path_data:
            # Cleaned Text Data
            if '/datasets/' in base_path_data:
                # Cleaned Datasets
                logging.debug(f'Analysing cleaned datasets from: {data_path}')

            elif '/webdata/' in base_path_data:
                # Cleaned Webdata
                logging.debug(f'Analysing cleaned webdata from: {data_path}')

        if '/monolingual/' in base_path_data:
            # Monolingual Text Data
            if '/plain/' in base_path_data:
                # Plain Monolingual Data
                logging.debug(f'Analysing plain monolingual data from: {data_path}')
                data_to_sents_and_words(languages_selected, data_path)
                analyse_monolingual(languages_selected, data_path, logs_path)
                logs_to_analyse_path = f'{logs_path}text_analysis/monolingual-plain/'
                visualize_analysis_logs(languages_selected, data_path, logs_to_analyse_path)

            elif '/bronze/' in base_path_data:
                # Bronze Monolingual Data
                logging.debug(f'Analysing bronze monolingual data from: {data_path}')

            elif '/silver/' in base_path_data:
                # Silver Monolingual Data
                logging.debug(f'Analysing silver monolingual data from: {data_path}')

            elif '/gold/' in base_path_data:
                # Gold Monolingual Data
                logging.debug(f'Analysing gold monolingual data from: {data_path}')

            elif '/platinum/' in base_path_data:
                # Platinum Monolingual Data
                logging.debug(f'Analysing platinum monolingual data from: {data_path}')

        if '/multilingual/' in base_path_data:
            # Multilingual Text Data
            if '/plain/' in base_path_data:
                # Plain Multilingual Data
                logging.debug(f'Analysing plain multilingual data from: {data_path}')

            elif '/bronze/' in base_path_data:
                # Bronze Multilingual Data
                logging.debug(f'Analysing bronze multilingual data from: {data_path}')

            elif '/silver/' in base_path_data:
                # Silver Multilingual Data
                logging.debug(f'Analysing silver multilingual data from: {data_path}')

            elif '/gold/' in base_path_data:
                # Gold Multilingual Data
                logging.debug(f'Analysing gold multilingual data from: {data_path}')

            elif '/platinum/' in base_path_data:
                # Platinum Multilingual Data
                logging.debug(f'Analysing platinum multilingual data from: {data_path}')


if __name__ == "__main__":
    main()

