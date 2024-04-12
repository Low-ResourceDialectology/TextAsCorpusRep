# Work in progress

import argparse
from datetime import datetime
import glob
import json
import os
import statistics
import sys
#import nltk
#from nltk.tokenize import sent_tokenize

# Download necessary NLTK data for sentence tokenization
#nltk.download('punkt')

def ensure_directory_exists(directory):
    """Ensure that the directory exists, create it if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)


# ##########################
# Counting the flickr30k data
def count_elements(dictionary):
    count = 0
    for value in dictionary.values():
        if isinstance(value, dict):
            count += count_elements(value)  # Recursively count elements in nested dictionary
        else:
            count += 1  # Increment count for non-dictionary elements
    return count

flickr_dict = {}
with open('./../data/flickr30k-aligned.json', 'r') as json_file:
    flickr_dict = json.load(json_file)

# Count elements in the example dictionary
total_elements = count_elements(flickr_dict)
print("Total annotations in the collected flickr30k data:", total_elements)




def count_sub_items(dictionary):
    sub_item_counts = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            sub_item_counts[key] = 1  # Initialize count for current level
            sub_item_counts[key] += count_sub_items(value)  # Recursively count sub-items in nested dictionary
        else:
            sub_item_counts[key] = 1  # Leaf node, count as one sub-item
    return sum(sub_item_counts.values())

# Count sub-items for each entry in the example dictionary
sub_item_counts = {}
for key, value in flickr_dict.items():
    sub_item_counts[key] = count_sub_items(value)

all_sub_counts = []
# Print sub-item counts for each entry
for key, count in sub_item_counts.items():
    #print(f"Entry {key}: {count} sub-items")
    all_sub_counts.append(count)
average_sub_counts = sum(all_sub_counts) / len(all_sub_counts)
print("Average number of annotations for flickr30k images collected:", average_sub_counts)


# Function to count sub-items for each entry in the dictionary
def count_sub_items(dictionary):
    sub_item_counts = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            sub_item_counts[key] = 1  # Initialize count for current level
            sub_item_counts[key] += count_sub_items(value)  # Recursively count sub-items in nested dictionary
        else:
            sub_item_counts[key] = 1  # Leaf node, count as one sub-item
    return sum(sub_item_counts.values())

# Count sub-items for each entry in the dictionary
sub_item_counts = {}
for key, value in flickr_dict.items():
    sub_item_counts[key] = count_sub_items(value)

# Sort dictionary items based on sub-item counts (descending order)
sorted_items = sorted(flickr_dict.items(), key=lambda x: sub_item_counts[x[0]], reverse=True)

# Create a new dictionary with sorted items
sorted_dict = dict(sorted_items)

# Print the sorted dictionary
#print("Sorted Dictionary:")
#print(sorted_dict)
json_object = json.dumps(sorted_dict, indent=4, ensure_ascii=False)
with open('./../data/flickr30k-aligned-sorted.json', "w") as outfile:
    outfile.write(json_object)


sys.exit()


#def tokenize_into_sentences(text, language='english'):
#    return sent_tokenize(text, language=language)

# For languages not covered by the nltk package
def tokenize_into_sentences(text_lines):
    sentences = []
    current_sentence = ""
    sentence_delimiters = [".", "!", "?"]  # You may need to adjust this based on the specific punctuation used in Central Kurdish

    for line in text_lines:
        for char in line:
            current_sentence += char
            if char in sentence_delimiters:
                sentences.append(current_sentence.strip())
                current_sentence = ""

    # Append the last sentence if it's not empty
    if current_sentence.strip():
        sentences.append(current_sentence.strip())

    return sentences

def read_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        text_lines = file.readlines()
        return text_lines

def count_lines(text_lines):
    return sum(1 for line in text_lines)

def count_words(text_lines):
    word_count = 0
    for line in text_lines:
        word_count += len(line.split())
    return word_count

def count_words_unique(text_lines):
    words_unique = set()
    for line in text_lines:
        words_unique.update(line.split())
    return len(words_unique)

def calculate_line_statistics(text_lines):
    line_lengths = [len(line.strip()) for line in text_lines]

    line_min = min(line_lengths)
    line_max = max(line_lengths)
    line_mean = sum(line_lengths) / len(line_lengths)
    line_mode = statistics.mode(line_lengths)
    line_median = statistics.median(line_lengths)

    # TODO: Count number of words per line/sentence too

    return line_min, line_max, line_mean, line_mode, line_median

def calculate_word_statistics(text_lines):
    words = [word for line in text_lines for word in line.split()]
    word_lengths = [len(word) for word in words]

    word_min = min(word_lengths)
    word_max = max(word_lengths)
    word_mean = sum(word_lengths) / len(word_lengths)
    word_mode = statistics.mode(word_lengths)
    word_median = statistics.median(word_lengths)

    return word_min, word_max, word_mean, word_mode, word_median


def process_text_file(input_file, info_dir):
    # Metadata
    cur_language = os.path.dirname(os.path.dirname(input_file))
    cur_variety = os.path.dirname(input_file)
    cur_date = datetime.now().strftime("%Y-%m-%d")

    # Handle very large files (>2.000 MB)
    file_stats = os.stat(input_file)
    #print(f'File Size in Bytes is {file_stats.st_size}')
    #print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')
    cur_file_size_mb = file_stats.st_size / (1024 * 1024)
    if cur_file_size_mb > 2000:
        stats = {
        "File":input_file,
        "Date":cur_date,
        "Language":cur_language,
        "Variety":cur_variety,
        "Unique word count":0,
        "Word count":0,
        "Word stats":0,
        "Sentence count":0,
        "Sentence stats":0,
        "Line count":0,
        "Line stats":0,
        "Note":"TEXT FILE TOO LARGE"
        }
        
        input_file_filename = os.path.basename(input_file).split('.')[0]
        output_file = f'{info_dir}{input_file_filename}.json'
        save_output_json(output_file, stats)
    
    else:
        # Read data and preprocess text
        text_lines = read_file(input_file)
        text_sents = tokenize_into_sentences(text_lines)

        # Perform text processing tasks
        unique_word_count = count_words_unique(text_lines)
        
        word_count = count_words(text_lines)
        word_min, word_max, word_mean, word_mode, word_median = calculate_word_statistics(text_lines)
        word_stats = {
            "Length min":word_min, 
            "Length max":word_max, 
            "Length mean":word_mean, 
            "Length mode":word_mode, 
            "Length median":word_median
        }

        sent_count = count_lines(text_sents)
        sent_min, sent_max, sent_mean, sent_mode, sent_median = calculate_line_statistics(text_sents)
        sent_stats = {
            "Length (chars) min":sent_min,
            "Length (chars) max":sent_max, 
            "Length (chars) mean":sent_mean, 
            "Length (chars) mode":sent_mode, 
            "Length (chars) median":sent_median
        }

        line_count = count_lines(text_lines)
        line_min, line_max, line_mean, line_mode, line_median = calculate_line_statistics(text_lines)
        line_stats = {
            "Length (chars) min":line_min,
            "Length (chars) max":line_max, 
            "Length (chars) mean":line_mean, 
            "Length (chars) mode":line_mode, 
            "Length (chars) median":line_median
        }

        # Aggregate statistics
        stats = {
            "File":input_file,
            "Date":cur_date,
            "Language":cur_language,
            "Variety":cur_variety,
            "Unique word count":unique_word_count,
            "Word count":word_count,
            "Word stats":word_stats,
            "Sentence count":sent_count,
            "Sentence stats":sent_stats,
            "Line count":line_count,
            "Line stats":line_stats
            }
        
        input_file_filename = os.path.basename(input_file).split('.')[0]
        output_file = f'{info_dir}{input_file_filename}.json'
        save_output_json(output_file, stats)

def process_var_dir(var_dir):
    text_dir = f'{var_dir}text/'
    ensure_directory_exists(text_dir)
    info_dir = f'{var_dir}info/'
    ensure_directory_exists(info_dir)
    aligned_dir = f'{var_dir}aligned/'
    ensure_directory_exists(aligned_dir)
    embeddings_dir = f'{var_dir}embeddings/'
    ensure_directory_exists(embeddings_dir)
    dict_dir = f'{var_dir}dict/'
    ensure_directory_exists(dict_dir)

    text_files = glob.glob(f'{text_dir}*')
    for text_file in text_files:
        process_text_file(text_file, info_dir)

def process_language_dir(lang_dir):
    variety_dirs = glob.glob(f'{lang_dir}*/')
    for var_dir in variety_dirs:
        print(f'Processing var_dir: {var_dir}')
        process_var_dir(var_dir)

def get_text_statistics(args):
    # Based on config-file for files 
    if args.files is not None and os.path.exists(args.files):
        with open(args.files, 'r') as config_file:
            config = json.load(config_file)

    # Based on config-file for language directories
    elif args.languages is not None and os.path.exists(args.languages):
        pass

    # Based on all language data that exists in ./data
    else:
        language_dirs = glob.glob('./data/*/')
        for lang_dir in language_dirs:
            print(f'Processing lang_dir: {lang_dir}')
            process_language_dir(lang_dir)

def save_output_json(output_file, stats, indent=4, ensure_ascii=False):
    # Save results to output json file
    stats_json = json.dumps(stats, indent=indent, ensure_ascii=ensure_ascii)
    with open(output_file, 'w') as outfile:
        outfile.write(stats_json)


def main():
    parser = argparse.ArgumentParser(description='Text Processing Script')
    parser.add_argument('--files', type=str, help='Path to the configuration file for processing files')
    # TODO: Turn into list of strings (languages) to be processed
    parser.add_argument('--languages', type=str, help='Path to the configuration file for processing languages')
    # python3 processing/master_texter.py --languages ./data
    parser.add_argument('--all', type=str, help='Path to the data for processing all languages')
    # python3 processing/master_texter.py --stats --all ./data
    parser.add_argument('--language', type=str, default='english', help='Language of the text (default: English)')
    parser.add_argument('-s', '--stats', action='store_true', help='Get statistics for text data')
    parser.add_argument('-m', '--monoses', action='store_true', help='Bilingual Lexicon Induction via Monoses')
    args = parser.parse_args()

    if args.stats:
        get_text_statistics(args)
    
    if args.monoses:
        get_text_statistics(args)

    

    sys.exit()    

    for file_info in config['files']:
        input_file = file_info['input']
        output_file = file_info['output']
        language = file_info.get('language', 'english')  # Default language is English
        
        # Debugging of input arguments
        #current_working_directory = os.getcwd()
        #print(f'current_working_directory: {current_working_directory}')
        #print(f'input_file: {input_file}')
        #print(f'output_file: {output_file}')

        # Metadata
        cur_date = datetime.now().strftime("%Y-%m-%d")

        # Ensure output directory exists
        output_directory = os.path.dirname(output_file)
        ensure_directory_exists(output_directory)

        # Read data and preprocess text
        text_lines = read_file(input_file)
        #text_sents = tokenize_into_sentences(text_lines, language)
        text_sents = tokenize_into_sentences(text_lines)

        # Perform text processing tasks
        unique_word_count = count_words_unique(text_lines)
        
        word_count = count_words(text_lines)
        word_min, word_max, word_mean, word_mode, word_median = calculate_word_statistics(text_lines)
        word_stats = {
            "Length min":word_min, 
            "Length max":word_max, 
            "Length mean":word_mean, 
            "Length mode":word_mode, 
            "Length median":word_median
        }

        sent_count = count_lines(text_sents)
        sent_min, sent_max, sent_mean, sent_mode, sent_median = calculate_line_statistics(text_sents)
        sent_stats = {
            "Length min":sent_min,
            "Length max":sent_max, 
            "Length mean":sent_mean, 
            "Length mode":sent_mode, 
            "Length median":sent_median
        }

        line_count = count_lines(text_lines)
        line_min, line_max, line_mean, line_mode, line_median = calculate_line_statistics(text_lines)
        line_stats = {
            "Length min":line_min,
            "Length max":line_max, 
            "Length mean":line_mean, 
            "Length mode":line_mode, 
            "Length median":line_median
        }

        # Aggregate statistics
        stats = {
            "File":input_file,
            "Date":cur_date,
            "Unique word count":unique_word_count,
            "Word count":word_count,
            "Word stats":word_stats,
            "Sentence count":sent_count,
            "Sentence stats":sent_stats,
            "Line count":line_count,
            "Line stats":line_stats
            }
        
        save_output_json(output_file, stats)
        
        # Save results to output file
        # with open(output_file, 'w') as out_file:
        #     out_file.write(f"File: {input_file}\n")
        #     #out_file.write(f"Language: {language}\n")
        #     out_file.write(f"Line count: {line_count}\n")
        #     out_file.write(f"Word count: {word_count}\n")
        #     out_file.write(f"Unique word count: {unique_word_count}\n")
        #     out_file.write(f"Line statistics: {line_stats}\n")
        #     out_file.write(f"Word statistics: {word_stats}\n")
        #     # Write other statistics to the output file

if __name__ == "__main__":
    main()