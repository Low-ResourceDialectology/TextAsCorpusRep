# -*- coding: utf-8 -*-
# Python Script for all types of reoccuring functionalities
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

"""

"""

import logging
import os
from statistics import mean
import string

# ===========================================
# Directories
# ===========================================
"""
Create a new directory if it does not already exist
"""
def create_directory(directory_path):

    #logging.info(f'  Creating new directory')
    #logging.debug(f'Creating directory: {directory_path}')
    
    # Attempt to create directory
    try:
        os.makedirs(directory_path)
    
    # Directory already exists
    except FileExistsError:
        logging.debug(f'Directory already exists: {directory_path}')


# ===========================================
# Files - General
# ===========================================
"""
Get the filename from an entire path
"""
def get_filename(directory_path):
    filename = os.path.basename(directory_path)
    
    return filename

"""
Get the basename of a file/path
"""
def get_basename(directory_path):
    basename = os.path.basename(directory_path).split(".")[0]
    
    return basename

"""
Get file ending of a file/path
"""
def get_fileending(directory_path):
    fileending = directory_path.split('.')[-1]
    
    return fileending

"""
Get file size in MB
"""
def get_filesize_mb(input_file):
    try:
        #file_size = os.path.getsize(input_file)
        #print(f"File Size in Bytes is {file_size}")
        file_stats = os.stat(input_file)
        file_size = round((file_stats.st_size/(1024*1024)),3)
        #print(f"File Size in Bytes is {file_size}")
        #print(f"File Size in MegaBytes is {file_size / (1024*1024)}")
        return file_size
    except FileNotFoundError:
        print("File not found.")
    except OSError:
        print("OS error occurred.")
        
"""
Get file size in Byte
"""
def get_filesize_b(input_file):
    try:
        file_stats = os.stat(input_file)
        file_size = round((file_stats.st_size),3)
        return file_size
    
    except FileNotFoundError:
        print("File not found.")
        
    except OSError:
        print("OS error occurred.")


# ===========================================
# Files - Text
# ===========================================
# ++++++++++++++++++++++++++++++++++++++ .txt 
"""
Read text from file
"""
def read_text_file(input_file):
    text_lines = []
    with open(input_file, 'r') as f:
        text_lines = f.readlines()
        return text_lines

"""
Write text to file
"""
def write_text_file(output_file, text_data):
    with open(output_file, 'w') as f:
        for line in text_data:
            f.write(line)

"""
Write text to file- line by line
"""
def write_text_file_lines(output_file, text_data):
    with open(output_file, 'w') as f:     
        for line in text_data:
            f.write(line+'\n')

# ++++++++++++++++++++++++++++++++++++++ .json
"""
Read text from file
"""
def read_json_file(input_file):
    pass

def write_json_file(output_file, dictionary):
    pass

# ++++++++++++++++++++++++++++++++++++++ .csv
def read_csv_file(input_file):
    pass

# ++++++++++++++++++++++++++++++++++++++ .pdf
def read_pdf_file(input_file):
    pass


# ===========================================
# Text - Lines
# ===========================================
def get_lines_number_total(input_data):
    number_lines = sum(1 for line in input_data)
    return number_lines

def get_number_lines_file(input_file):
    with open(input_file, 'r') as fp:
        number_lines = sum(1 for line in fp)
        #print('Total line count: ', number_lines)
        return number_lines

def get_lines_number_unique(input_data):
    unique_words = set(input_data)
    number_words_unique = len(unique_words)
    return number_words_unique

def get_lines_min_and_length(input_data):
    lines_min = min(input_data, key=len)
    lines_min_length = len(lines_min)
    return lines_min, lines_min_length

def get_lines_max_and_length(input_data):
    lines_max = max(input_data, key=len)
    lines_max_length = len(lines_max)
    return lines_max, lines_max_length

#def get_lines_max(input_data):
#    max_lines = max(len(line) for line in input_data)
#    return max_lines

def get_lines_mean(input_data):
    mean_lines = mean([len(line) for line in input_data])
    return mean_lines


# ===========================================
# Text - Sentences
# ===========================================
def get_number_sentences(input_file):
    pass

def get_number_sentences_unique(input_file):
    pass


# ===========================================
# Text - Words
# ===========================================
def get_words_number_total(input_data):
    number_words = 0
    for line in input_data:
        words = line.split()
        number_words += len(words)
    return number_words

def get_number_words_file(input_file):
    with open(input_file,'r') as file:
        text_data = file.read()
    number_words = get_words_number_total(text_data)
    return number_words
    """
    number_words = 0
    with open(input_file,'r') as file:
        data = file.read()
        lines = data.split()
        number_words += len(lines)
    #print('Total word count: ', number_words)
    return number_words
    """

def get_words_number_unique(input_data):
    words = set()
    for line in input_data:
        word_list = line.split()
        for word in word_list:
            words.add(word)
    number_words_unique = len(words)
    return number_words_unique

def get_words_min_and_length(input_data):
    words = []
    for line in input_data:
        word_list = line.split()
        for word in word_list:
            words.append(word)
    min_word = min(words, key=len)
    min_word_length = len(min_word)
    return min_word, min_word_length

def get_words_max_and_length(input_data):
    words = []
    for line in input_data:
        word_list = line.split()
        for word in word_list:
            words.append(word)
    max_word = max(words, key=len)
    max_word_length = len(max_word)
    return max_word, max_word_length

def get_words_mean_length(input_data):
    words = []
    for line in input_data:
        word_list = line.split()
        for word in word_list:
            words.append(word)
    mean_words = mean([len(word) for word in words])
    return mean_words


# ===========================================
# Text - Characters
# ===========================================
def get_number_characters(input_data):
    pass

def get_number_characters_unique(input_file):
    pass


# ===========================================
# Text - Processing
# ===========================================
def remove_punctuation_end(input_data):
    current_string = input_data
    #print(f'{current_string} last char: {current_string[-1]}')
    
    # ” is not considered to be part of string.punctuation?
    if current_string.startswith('“'):
        current_string = current_string[1:]
    
    if current_string.endswith('”'):
        current_string = current_string[:-1]
    
    if current_string[0] in string.punctuation:
        current_string = current_string[1:]

    #if current_string[-1] in ['.', ',', '!', '?']:  
    if current_string[-1] in string.punctuation:
        current_string = current_string[:-1]

    #elif current_string[-1] in ['.', ',', '!', '?']:
    #elif current_string[-1] in string.punctuation:
    #    clean_string = current_string[:-1]
    
    clean_string = current_string
    
    return clean_string


