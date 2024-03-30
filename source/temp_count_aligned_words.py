# -*- coding: utf-8 -*-
# Python Script for finding and counting aligned words between languages
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

"""Usage
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/source

source ./../environments/ventMTACR/bin/activate

python temp_count_aligned_words.py
"""

import argparse
import configparser
import glob
import json
import logging
import os
import sys
import textwrap

import utils.utilities_general as util_ge


def main():

    """
    Going through all English words that are aligned with at least one other language
    and then find all languages aligned with this word.
    OUTPUT: 
        "you": ["ukr", "zho", "mfe", "fra", "vie", "kmr", "deu"],
        "Object": ["mfe", "vie"],
    For "you" we have the translation in each of our current languages,
    for "Object" only Morisien and Vietnamese.
    """
    def collect_aligned_languages_per_english_word():

        # Read the eng-aligned words
        logs_path = './../logs/'
        logs_file_path = './../logs/aligned_words_eng.json'

        with open(logs_file_path, 'r') as json_file:
            data = json.load(json_file)
        
        sorted_aligned_words = {}
        # = { "1": { "key1": [languages], "key2": [languages], ...} }

        for key in data.keys():
            number_of_aligned_languages = str(len(data[key]))
            
            if number_of_aligned_languages in sorted_aligned_words.keys():
                sorted_aligned_words[number_of_aligned_languages][key] = data[key]
            else:
                sorted_aligned_words[number_of_aligned_languages] = {}
                sorted_aligned_words[number_of_aligned_languages][key] = data[key]


        # Save a new file for each number of occurences
        for out_key in sorted_aligned_words.keys():

            aligned_words_dict = sorted_aligned_words[out_key]
            # Serializing json
            json_object = json.dumps(aligned_words_dict, indent=4, ensure_ascii=False)
            output_file = f'{logs_path}aligned_words_eng-{out_key}.json'
            print(f'Writing to file: {output_file}')

            # Writing to json file
            with open(output_file, "w") as outfile:
                outfile.write(json_object)

    #collect_aligned_languages_per_english_word()
    #print('Done did it!')
    
    
    """
    From the previously collected languages (per English word) for which a translation exists, 
    count these "links" between languages for each lanuages pair.
    """
    def count_alinged_words_per_language_pair():

        # Path to log files
        logs_path = './../logs/'

        # Currently included language codes
        language_codes = ["mfe", "kmr", "vie", "zho", "ukr", "deu", "fra"]

        # All files created by the function (26.01.2024)
        # collect_aligned_languages_per_english_word()
        collected_aligned_word_files = [
            "aligned_words_eng-2.json", "aligned_words_eng-3.json",
            "aligned_words_eng-4.json", "aligned_words_eng-5.json",
            "aligned_words_eng-6.json", "aligned_words_eng-7.json"
        ]
        #aligned_words_eng-1.json → Only aligned with one language- no new "Link"
    
        # For each of the included languages
        for language in language_codes:

            current_language_dict = {}

            # Look into each of the Aligned_Words_English-Files
            for collected_aligned_word_file in collected_aligned_word_files:
                current_file_path = f'{logs_path}{collected_aligned_word_file}'

                # Read the collected alignments from this file- such as:
                # "respected": ["mfe", "fra", "vie", "kmr", "deu"]
                with open(f'{current_file_path}','r') as input_json:
                    current_collected_aligned_words_json = json.load(input_json)

                # For each English word in current json-data
                for key in current_collected_aligned_words_json.keys():

                    # Read the aligned languages:
                    aligned_languages = current_collected_aligned_words_json[key]

                    # Check if the current language has a translation for this word
                    if language in aligned_languages:

                        # If this is the only language, there is only English as aligned language in the data
                        if len(aligned_languages) == 1:
                            if "eng" in current_language_dict:
                                current_language_dict["eng"].append(key)
                            # And create this new language pair (new key in dict) if not exist yet
                            else:
                                current_language_dict["eng"] = [key]

                        # Otherwise there will be more items and we check them out
                        else:

                            # For each of these aligned languages
                            for lang_item in aligned_languages:

                                # If we found the current language as "aligned language", we simply add English
                                if lang_item == language:
                                    if "eng" in current_language_dict:
                                        current_language_dict["eng"].append(key)
                                    # And create this new language pair (new key in dict) if not exist yet
                                    else:
                                        current_language_dict["eng"] = [key]

                                # Otherwise we found another language being aligneable via this word and add it
                                else:
                                    # Place the aligned word (key) into the current_language_dict placed under the aligned language
                                    if lang_item in current_language_dict:
                                        current_language_dict[lang_item].append(key)
                                    # And create this new language pair (new key in dict) if not exist yet
                                    else:
                                        current_language_dict[lang_item] = [key]
                    # All languages for this word checked and added
                # All words from current alignment_file processed
            # All alignment_files processed
            
            # Write the output into a new file
            output_filename = f'{language}-aligned_via-eng.json'
            output_filepath = f'{logs_path}{output_filename}'

            # Serializing json and write to file
            json_object = json.dumps(current_language_dict, indent=4)
            with open(output_filepath, "w") as outfile:
                outfile.write(json_object)

            # Count the findings and also write those out
            current_lang_dict_numbers = {}
            for aligned_language in current_language_dict.keys():
                number_of_words = len(current_language_dict[aligned_language])
                current_lang_dict_numbers[aligned_language] = number_of_words
                
            output_filename = f'{language}-aligned_via-eng-numbers.json'
            output_filepath = f'{logs_path}{output_filename}'

            # Serializing json and write to file
            json_object = json.dumps(current_lang_dict_numbers, indent=4)
            with open(output_filepath, "w") as outfile:
                outfile.write(json_object)
                        
        # All currently contained languages checked
    count_alinged_words_per_language_pair()
                
    
    sys.exit()

    # Find all the "via-eng" aligned words
    data_multingual_plain_path = './../data/multilingual/plain/'
    logs_path = './../logs/'

    language = 'eng'

    input_path = f'{data_multingual_plain_path}{language}/'

    # Get all files for current language
    lang_files = glob.glob(f'{input_path}/wordlist-*')

    aligned_words_dict = {}

    # For each file in current dataset
    for lang_file in lang_files:

        lang_file_filename = util_ge.get_filename_without_extension(lang_file)
        
        # Filenames with a '-' have specific information prior to it
        # In this case if file contains "word", "sent", or "para" text data
        lang_file_info = lang_file_filename.split('-')[0]           # "wordlist"
        lang_file_aligned = lang_file_filename.split('-')[1]        # "kmr" | "vie" | "mfe"
        lang_file_content = util_ge.get_fileextension(lang_file)    # "kmr" | "vie" | "mfe"

        current_text = util_ge.read_text_file(lang_file)
        for line in current_text:
            clean_word = line.replace('\n','')

            # For already encountered words
            if clean_word in aligned_words_dict.keys():
                aligned_words_dict[clean_word].append(lang_file_aligned)
            else:
                aligned_words_dict[clean_word] = [lang_file_aligned]

    # Serializing json
    json_object = json.dumps(aligned_words_dict, indent=4, ensure_ascii=False)
    
    output_json = f'{logs_path}aligned_words_eng.json'

    # Writing to json file
    with open(output_json, "w") as outfile:
        outfile.write(json_object)



if __name__ == "__main__":
    main()