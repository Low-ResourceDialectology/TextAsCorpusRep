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
import gzip # Reading compressed files .gz
import logging
import os
import re
from statistics import mean
import string
import zipfile # Extracting compressed files .zip

from PyPDF2 import PdfReader 

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
        pass
        #logging.debug(f'Directory already exists: {directory_path}')


# ===========================================
# Files - Paths, Names, Basenames, Fileextensions
# https://note.nkmk.me/en/python-os-basename-dirname-split-splitext/
# ===========================================
"""
Get the basename (filename with extension) from an entire path
INPUT: "InterdialectCorpus/master/KMR-ENG/KMR-ENG.KMR_no_tag.txt"
OUTPUT: "KMR-ENG.KMR_no_tag.txt"
"""
def get_filename_with_extension(directory_path):
    filename_with_extension = os.path.basename(directory_path)
    
    return filename_with_extension

"""
Get the filename (without extension) from an entire path
INPUT: "InterdialectCorpus/master/KMR-ENG/KMR-ENG.KMR_no_tag.txt"
OUTPUT: "KMR-ENG.KMR_no_tag"
"""
def get_filename_without_extension(directory_path):
    filename_without_extension = os.path.splitext(os.path.basename(directory_path))[0]
    return filename_without_extension
    """
    NOTE: os.path.splitext() split at the last (right) dot . 
        "KMR-ENG.KMR_no_tag.txt" → "KMR-ENG.KMR_no_tag"
    NOTE: os.path.split() to split by the first (left) dot .
        "KMR-ENG.KMR_no_tag.txt" → "KMR-ENG"
    """

"""
Get file extension of a file/path
INPUT: "InterdialectCorpus/master/KMR-ENG/KMR-ENG.KMR_no_tag.txt"
OUTPUT: "txt"
"""
def get_fileextension(directory_path):
    fileextension = directory_path.split('.')[-1]
    return fileextension

"""
Get the basename (filename with extension) of a file/path
INPUT: "InterdialectCorpus/master/KMR-ENG/KMR-ENG.KMR_no_tag.txt"
OUTPUT: "KMR-ENG.KMR_no_tag.txt"
"""
def get_basename(directory_path):
    basename = os.path.basename(directory_path)
    return basename


# ===========================================
# Files - Size, Metadata, Others
# 
# ===========================================
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
# Files - Extract and Transform
# ===========================================
def extract_zipped_file(zip_file_path, output_path):
    print(f'Extracting {zip_file_path} to {output_path}')
    with zipfile.ZipFile(f'{zip_file_path}', 'r') as zip_ref:
        zip_ref.extractall(f'{output_path}')

def read_compressed_file_gz_text(gz_file_path):
    with gzip.open(gz_file_path, 'rt') as f:
        file_content = f.read()
        return file_content
    
def read_compressed_file_gz_binary(gz_file_path):
    with gzip.open(gz_file_path, 'rb') as f:
        file_content = f.read()
        return file_content

# ++++++++++++++++++++++++++++++++++++++ .pdf
"""
Extract text from PDF file
USES: PdfReader from PyPDF2
"""
def pdf_to_txt_file(input_pdf_file, output_txt_file):

    # Creating a pdf reader object 
    reader = PdfReader(f'{input_pdf_file}') 
    
    # Printing number of pages in pdf file 
    print(f'Transforming PDF file with {len(reader.pages)} pages.') 

    text_content = []

    for page in reader.pages:
        current_text = page.extract_text() 
        text_content.append(current_text)

    write_text_file_lines(output_txt_file, text_content)
    #with open(f'{output_txt_file}', 'w') as out_file:
    #    for line in text_content:
    #        out_file.write(line)

    # Getting a specific page from the pdf file 
    #page = reader.pages[0] 
    # Extracting text from page 
    #text = page.extract_text() 


# ===========================================
# Files - Text
# ===========================================
# ++++++++++++++++++++++++++++++++++++++ .txt 
"""
Read text from file
"""
def read_text_file(input_file, file_encoding="UTF-8"): # "latin-1"
    text_lines = []
    with open(input_file, 'r', encoding=file_encoding) as f:
        text_lines = f.readlines()
        return text_lines

"""
Read text from file that is binary encoded
"""
def read_text_file_binary(input_file, file_encoding="UTF-8"):
    text_lines = []
    with open(input_file, 'rb') as f:
        text_input = f.readlines()
        text_lines = text_input.encode(file_encoding)
        return text_lines

"""
Write text to file
"""
def write_text_file(output_file, text_data, file_encoding="UTF-8"):
    with open(output_file, 'w', encoding=file_encoding) as f:
        for line in text_data:
            f.write(line)

"""
Write text to file- line by line
"""
def write_text_file_lines(output_file, text_data, file_encoding="UTF-8"):
    #print(f'INSANITY: {output_file}')
    with open(output_file, 'w', encoding=file_encoding) as f:     
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
def check_for_non_empty_string(input_data):
    if input_data == "":
        return False
    else:
        return True 
    
def text_lines_remove_empty_lines(input_data):
    output_lines = []
    for line in input_data:
        if not line == '\n' or line == ' \n':
            # Also remove leading and trailing whitespace
            output_lines.append(line.strip())
    return output_lines

"""
First, add a full stop to each line (turning them into sentences)
Second, read all lines into a single string
Third, split by full stops and save as separate lines again
"""
def text_lines_long_to_sentences(input_data):
    new_text_lines = []
    for line in input_data:
        # Remove line-breaks
        new_line = line.replace('\n','')

        if not new_line.endswith('.'):
            new_line = f'{new_line}.'
        new_text_lines.append(new_line)

    one_line = ""
    for line in new_text_lines:
        one_line = one_line + line
    
    text_line_sentences = []
    one_line_split = one_line.split('.')
    for sentence in one_line_split:
        # Remove whitespaces with .strip()
        text_line_sentences.append(sentence.strip()+'.')
        
    return text_line_sentences

"""
First, read all lines into a single string
Second, split by full stops and save as separate lines again
"""
def text_lines_short_to_sentences(input_data):
    new_text_lines = []
    for line in input_data:
        # Remove line-breaks
        new_line = line.replace('\n','')

        new_text_lines.append(new_line)

    one_line = ""
    for line in new_text_lines:
        one_line = one_line + line
    
    text_line_sentences = []
    one_line_split = one_line.split('.')
    for sentence in one_line_split:
        # Remove whitespaces with .strip()
        text_line_sentences.append(sentence.strip()+'.')
        
    return text_line_sentences


# TODO
def text_lines_to_sentences_sophisticated(text_lines):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'

    def split_into_sentences(text: str) -> list[str]:
        """
        Split the text into sentences.

        If the text contains substrings "<prd>" or "<stop>", they would lead 
        to incorrect splitting because they are used as markers for splitting.

        :param text: text to be split into sentences
        :type text: str

        :return: list of sentences
        :rtype: list[str]
        """
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
        text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences]
        if sentences and not sentences[-1]: sentences = sentences[:-1]
        return sentences


def remove_punctuation_end(input_data):
    current_string = input_data
    #print(f'{current_string} last char: {current_string[-1]}')
    #print(f'current_string = {current_string}')

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

def text_lines_remove_special_characters(input_data):
    clean_text_lines = []
    for line in input_data:
        clean_line = re.sub("[^A-ZîÎêÊûÛşŞçÇ#,.!?:;() ]","",line,0,re.IGNORECASE)
        clean_text_lines.append(clean_line.replace('  ',' ').replace('URL','').strip())

    return clean_text_lines