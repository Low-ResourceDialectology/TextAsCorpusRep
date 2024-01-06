# -*- coding: utf-8 -*-
# Python Script for analyzing text data of various stages of the processing pipeline
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

def main():
    pass


# TODO: From analyze_text_content.py
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
    



