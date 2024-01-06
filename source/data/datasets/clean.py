# -*- coding: utf-8 -*-
# Python Script for transforming, sorting and cleaning collected text data (datasets)
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################
"""
Prior Step: Get and Transform Datasets
This Step: Cleaning of Text Data
Next Step: Extract from Clean Data
"""

""" Development-Note:
The previous steps "Transforming", "Sorting" and "Cleaning" have been merged into this one script.
"""

import glob # For reading multiple txt files and write them into a single file in one go
# https://stackoverflow.com/questions/17749058/combine-multiple-text-files-into-one-text-file-using-python 
import json
import logging
import os
import re
import shutil
import sys

#from datasets import load_dataset_builder
#from datasets import load_dataset
from datasets import load_from_disk

# Enable importing the other scripts by adding their location to the python-path
sys.path.append(r"./../../")

import utils.utilities_general as util_ge


"""
Transforming the collected Data into a normalized structure for easy processing.
"""
def transform_data(current_dataset_key, current_dataset_info, inputPath, outputPath):

    logging.debug(f'====== Transforming dataset')
    logging.debug(f'++++++ inputPath: {inputPath}')
    logging.debug(f'++++++ outputPath: {outputPath}')

    # #########################################################################
    # TODO - Simple txt format mainly in need of sorting
    # INPUT: "ccknt.txt"
    # OUTPUT: "kmr.kmr"
    if current_dataset_key == '2001HaigKurdishNewspaper':
        download_path = f'{inputPath}{current_dataset_key}/'
        transform_path = f'{outputPath}{current_dataset_key}/'
        current_filename = "ccknt.txt"

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Read the .txt file line-by-line
        input_lines = util_ge.read_text_file(f'{download_path}{current_filename}', file_encoding="latin-1")
        #input_lines = []
        #with open(f'{download_path}{current_filename}', 'r') as file:
        #    input_lines = file.readlines()

        # Remove news-article identifier such as "[AW69A1]", "Reuters", "Washington Post"
        output_lines = []
        for line in input_lines:
            if len(line) > 17: # TODO: check if this "len-"count is words or characters
                output_lines.append(line)

        # Write the text into a new file
        util_ge.write_text_file_lines(f'{transform_path}kmr.kmr', output_lines, file_encoding="UTF-8")
        #with open(f'{transform_path}kmr.kmr', 'w') as file:
        #    for line in input_lines:
        #        file.write(line)

    
    # #########################################################################
    # TODO - Data to be extracted
    # TODO - Data in form of many different files
    # INPUT: "Pewan.zip" which is a zip-file
    # OUTPUT: "Kurmanji/docs2/a_butload_of_files" (25.572 files)
    if current_dataset_key == '2013EsmailiPewan':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_filename = f'{download_path}Pewan.zip'

        # Create directory if not existing
        util_ge.create_directory(transform_path)
        util_ge.extract_zipped_file(f'{current_filename}', f'{transform_path}')

        transform_path_02 = transform_path + f'Kurmanji'
        current_filename_02 = f'{transform_path}Pewan/Corpora/Kurmanji.zip'

        # Create directory if not existing
        util_ge.create_directory(transform_path_02)
        util_ge.extract_zipped_file(f'{current_filename_02}', f'{transform_path_02}')

    # #########################################################################
    # TODO - Data to be extracted
    # TODO - Well-structured data in which each line holds one item (sentence or word)
    # INPUT: "train.de.gz", "train.en.gz", "train.fr.gz", "val.de.gz", "val.en.gz", "val.fr.gz"
    # OUTPUT: "train-eng_fra.deu", "train-fra_deu.eng", ...
    if current_dataset_key == '2016ElliottMulti30k':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                
                # Get current filename and split it into the three components used in this dataset
                current_filename = util_ge.get_filename_with_extension(f)
                    # → "train.de.gz"
                current_filename_extension = current_filename.split('.')[-1]
                    # "train.de.gz" → "gz"
                current_filename_ending = current_filename.split('.')[-2]
                    # "train.de.gz" → "de"
                current_filename_beginning = current_filename.split('.')[-3]
                    # "train.de.gz" → "train"

                # Extract gz-file
                text_content_from_compressed_file = util_ge.read_compressed_file_gz_text(f)
                
                # German text file
                if current_filename_ending == 'de':
                    new_extension = 'deu'
                    new_aligned_lang = 'eng_fra'
                    new_filename = f'{current_filename_beginning}-{new_aligned_lang}.{new_extension}'
                    # Write the text into a new file
                    with open(f'{transform_path}{new_filename}', 'w') as file:
                        for line in text_content_from_compressed_file:
                            file.write(line)

                # English text file
                elif current_filename_ending == 'en':
                    new_extension = 'eng'
                    new_aligned_lang = 'fra_deu'
                    new_filename = f'{current_filename_beginning}-{new_aligned_lang}.{new_extension}'
                    # Write the text into a new file
                    with open(f'{transform_path}{new_filename}', 'w') as file:
                        for line in text_content_from_compressed_file:
                            file.write(line)

                # French text file
                elif current_filename_ending == 'fr':
                    new_extension = 'fra'
                    new_aligned_lang = 'deu_eng'
                    new_filename = f'{current_filename_beginning}-{new_aligned_lang}.{new_extension}'
                    # Write the text into a new file
                    with open(f'{transform_path}{new_filename}', 'w') as file:
                        for line in text_content_from_compressed_file:
                            file.write(line)

    # #########################################################################
    # TODO - Other format mainly in need of transforming              
    # TODO - Extract linguistic information for each entry
    # Entries have the format: "bêdengî	bêdengîên	DEF;LGSPEC1;N;PL;VOC" (seperated by tabs)
    # INPUT: "kmr"
    # OUTPUT: "kmr.kmr"
    if current_dataset_key == '2016UniMorphNorthernKurdish':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_input_filename = f'{download_path}kmr.txt'
        current_output_filename = f'{transform_path}kmr.kmr'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        text_content = util_ge.read_text_file(current_input_filename)
        #text_lines = util_ge.read_text_file(current_input_filename)
        #for line in text_lines:
        #    first_word_in_line = line.split('\t')
        #    text_content.append(first_word_in_line)
        
        util_ge.write_text_file(f'{current_output_filename}', text_content)


    # #########################################################################
    # TODO - Well-structured data in which each line holds one item (sentence or word)
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2017LuongNMT':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        #dataset_ids = ["https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/CKB-KMR/CKB-KMR_kmr_no_tag.txt",
                       #"https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/CKB-KMR/CKB-KMR_ckb_no_tag.txt",
                       #"https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/KMR-ENG/KMR-ENG.ENG_no_tag.txt",
                       #"https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/KMR-ENG/KMR-ENG.KMR_no_tag.txt"]
        dataset_ids = current_dataset_info['Platform ID']

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        current_dataset = '2017LuongNMT'
        logging.debug(f'====   Dataset: {current_dataset}')

        download_path = inputPath + f'{current_dataset}/'
        transform_path = outputPath + f'{current_dataset}/'

        # Create directory if not existing
        util_ge.create_directory(transform_path)
        
        input_lines = []

        # Read the .txt file line-by-line
        with open(download_path+'nmt/nmt/testdata/iwslt15.tst2013.100.en') as file:
            input_lines = file.readlines()

        # Write the text into a new file
        with open(transform_path+'vie.eng', 'w') as file:
            for line in input_lines:
                file.write(line)

        input_lines = []

        # Read the .txt file line-by-line
        with open(download_path+'nmt/nmt/testdata/iwslt15.tst2013.100.vi') as file:
            input_lines = file.readlines()

        # Write the text into a new file
        with open(transform_path+'eng.vie', 'w') as file:
            for line in input_lines:
                file.write(line)

    # #########################################################################
    # TODO - Data in form of many different files
    # TODO - Move this to later step and just keep track of filenames here
    # INPUT: "barzani_newroz.kmr.txt", "kurdistannews.txt", "xurmatu.txt", "xurm-trans-hand.txt"
    # OUTPUT: "kmr.kmr"
    if current_dataset_key == '2018CraveApertiumNorthernKurdish':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_output_filename = f'{transform_path}kmr.kmr'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        text_content = []
        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                current_text_lines = util_ge.read_text_file(f)
                for line in current_text_lines:
                    text_content.append(line)
                
        util_ge.write_text_file_lines(f'{current_output_filename}', text_content)

    # #########################################################################
    # TODO - Simple txt format mainly in need of cleaning
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2020FatihkurtKurdishTwitter':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_input_filename = "twitter-data.txt"

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Read the .txt file line-by-line
        output_lines = util_ge.read_text_file(f'{download_path}{current_input_filename}')

        # Write the text into a new file
        util_ge.write_text_file(f'{transform_path}kmr.kmr', output_lines)

    # #########################################################################
    # TODO - Data in form of many different files
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2021BfsujasonMAC':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_output_filename_zho = f'{transform_path}eng.zho'
        current_output_filename_eng = f'{transform_path}zho.eng'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        text_content_zho = []
        text_content_eng = []
        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                if not util_ge.get_filename_without_extension(f).startswith('meta'):
                    current_text_lines = util_ge.read_text_file(f)
                    for line in current_text_lines:
                        zho_line = line.split('\t')[0]
                        eng_line = line.split('\t')[1]
                        text_content_zho.append(zho_line)
                        text_content_eng.append(eng_line)
        # End of zho content is start of eng content- but end of eng content is linebreak
        util_ge.write_text_file_lines(f'{current_output_filename_zho}', text_content_zho)
        util_ge.write_text_file(f'{current_output_filename_eng}', text_content_eng)

    # #########################################################################
    # TODO - Other Datasets acquired via Requests or otherwise
    # TODO - Data in form of many different files
    # This dataset contains text data for "tokenization" and "detokenization"
    #  - Each split into "train", "dev", "test"
    #  - Each in "en" (English) and "vi" (Vietnamese)
    # INPUT: "detokenization/train/train.en"
    # OUTPUT: "train-vie.eng"
    if current_dataset_key == '2021DoanPhoMT':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        
        current_dataset_files = [
            "detokenization/train/train.en", "detokenization/train/train.vi", 
            "detokenization/dev/dev.en", "detokenization/dev/dev.vi",
            "detokenization/test/test.en", "detokenization/test/test.vi"]
        
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        for current_filename in current_dataset_files:
            raw_data_path = f'{download_path}{current_filename}'
            current_filename_withoutextension = util_ge.get_filename_without_extension(raw_data_path)
            current_extension = util_ge.get_fileextension(raw_data_path)
            
            # For Vietnamese text data
            if current_extension == 'vi':
                new_extension = 'vie'
                new_aligned_lang = 'eng'
                new_filename = f'{current_filename_withoutextension}-{new_aligned_lang}.{new_extension}'
                """
                INPUT: "train.vi"
                OUTPUT: "train-eng.vie"
                """
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}{new_filename}', 'w') as file:
                    for line in input_lines:
                        file.write(line)

            # For English text data
            elif current_extension == 'en':
                new_extension = 'eng'
                new_aligned_lang = 'vie'
                new_filename = f'{current_filename_withoutextension}-{new_aligned_lang}.{new_extension}'
                """
                INPUT: "train.en"
                OUTPUT: "train-vie.eng"
                """
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}{new_filename}', 'w') as file:
                    for line in input_lines:
                        file.write(line)

    
    # #########################################################################
    # TODO - Well-structured data in which each line holds one item (sentence or word)
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2022AhmadiInterdialect':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        #dataset_ids = ["https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/CKB-KMR/CKB-KMR_kmr_no_tag.txt",
                       #"https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/CKB-KMR/CKB-KMR_ckb_no_tag.txt",
                       #"https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/KMR-ENG/KMR-ENG.ENG_no_tag.txt",
                       #"https://raw.githubusercontent.com/KurdishBLARK/InterdialectCorpus/master/KMR-ENG/KMR-ENG.KMR_no_tag.txt"]
        dataset_ids = current_dataset_info['Platform ID']

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        for dataset_id in dataset_ids:
            # Get current_filename from dataset_ids (work for GitHub data)
            current_filename = util_ge.get_filename_with_extension(dataset_id)

            # Northern Kurdish Text (aligned with English)
            if current_filename == "KMR-ENG.KMR_no_tag.txt":
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}eng.kmr', 'w') as file:
                    for line in input_lines:
                        file.write(line)

            # English Text (aligned with Northern Kurdish)
            elif current_filename == "KMR-ENG.ENG_no_tag.txt":
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}kmr.eng', 'w') as file:
                    for line in input_lines:
                        file.write(line)

            # Northern Kurdish Text (aligned with Central Kurdish)
            elif current_filename == "CKB-KMR_kmr_no_tag.txt":
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}kmr.eng', 'w') as file:
                    for line in input_lines:
                        file.write(line)

            # Central Kurdish Text (aligned with Northern Kurdish)
            elif current_filename == "CKB-KMR_ckb_no_tag.txt":
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}kmr.eng', 'w') as file:
                    for line in input_lines:
                        file.write(line)

    # #########################################################################
    # TODO - HuggingFace Datasets
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2022DabreMorisienMT':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        #dataset_id = "prajdabre/KreolMorisienMT"
        #dataset_id = current_dataset_info['Platform ID']

        # Create directory if not existing
        util_ge.create_directory(transform_path)
    
        # The "download_from_huggingface()" from "download.py" should have downloaded the dataset by this point
        # The dataset is stored in the location "f'{dataset_path}{dataset_key}'"
        #   - dataset_path = Local path to download to
	    #       e.g. "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/raw/datasets/"
        #   - dataset_key = Identifier for local dataset location
	    #       e.g. "2022DabreMorisienMT"
        # → "/data/raw/datasets/2022DabreMorisienMT/"
        
        # To load the dataset from local location
        loaded_local_dataset = load_from_disk(f'{download_path}/local')

        # Load current dataset (This reinitiated a new download of the data, which should not be necessary!)
        #loaded_local_dataset = load_dataset(dataset_id, cache_dir=download_path, split='train')

        """ # Outputs while inspecting the dataset and its structure
        print(len(loaded_local_dataset)) # → 85415
        print(loaded_local_dataset[0]) # → {'input': '', 'target': ''}
        print(loaded_local_dataset.shape) # → (85415, 2)
        print(loaded_local_dataset.num_columns) # → 2
        print(loaded_local_dataset.column_names) # → ['input', 'target']
        print(loaded_local_dataset.num_rows) # → 85415
        print(loaded_local_dataset.features) # → {'input': Value(dtype='string', id=None), 'target': Value(dtype='string', id=None)}
        """

        logging.debug(f'Length of loaded_local_dataset: {len(loaded_local_dataset)}') # → 1
        logging.debug(f'Length of loaded_local_dataset["train"]: {len(loaded_local_dataset["train"])}') # → 85415
        
        """ This is python-logic! We need huggingface-logic!
        for dataset_row in data_morisien[0:45367]:
            with open(transform_path+'dabre_dataset.mor', 'w') as file:
                file.write(str(dataset_row))
                file.write('\n')
        for dataset_row in data_morisien[45367:68677]:
            with open(transform_path+'dabre_dataset.eng', 'w') as file:
                file.write(str(dataset_row))
                file.write('\n')
        for dataset_row in data_morisien[68677:-1]:
            with open(transform_path+'dabre_dataset.fra', 'w') as file:
                file.write(str(dataset_row))
                file.write('\n')
        """

        data_morisien_mor = loaded_local_dataset['train'][3:45366]
        #for dataset_row in data_morisien_mor:
        logging.debug(f'Length of data_morisien_mor: {len(data_morisien_mor)}')
        #print(transform_path+'mor.mor')
        with open(transform_path+'mor.mor', 'w') as file:
            mormor = data_morisien_mor['input']
            for line in mormor:
                file.write(line)
                file.write('\n')

        data_morisien_eng = loaded_local_dataset['train'][45366:68676]
        logging.debug(f'Length of data_morisien_eng: {len(data_morisien_eng)}')
        #print(transform_path+'mor.eng')
        with open(transform_path+'mor.eng', 'w') as file:
            engeng = data_morisien_eng['input']
            for line in engeng:
                file.write(line)
                file.write('\n')

        with open(transform_path+'eng.mor', 'w') as file:
            engmor = data_morisien_eng['target']
            for line in engmor:
                file.write(line)
                file.write('\n')

        data_morisien_fra = loaded_local_dataset['train'][68676:]
        logging.debug(f'Length of data_morisien_fra: {len(data_morisien_fra)}')
        with open(transform_path+'mor.fra', 'w') as file:
            frafra = data_morisien_fra['input']
            for line in frafra:
                file.write(line)
                file.write('\n')

        with open(transform_path+'fra.mor', 'w') as file:
            framor = data_morisien_fra['target']
            for line in framor:
                file.write(line)
                file.write('\n')


    # #########################################################################
    # TODO - Data in form of many different files
    # TODO - Consider just cloning the entire repository and then work based on directory structure
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2022NgoSynthetic':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)
        
        files_cn_vi = ['train.tok.cn', 'train.tok.true.vi']
        files_en_vi = ['train.tok.en', 'train.tok.vi']
        files_fr_vi = ['train.fr', 'train.vi']
        files_ja_vi = ['train.ja-vi.ky.ja', 'train.ja-vi.tok.true.vi']

        current_dataset_files = [
            "train.fr", "/dekoenization/train/train.vi", 
            "/dekoenization/dev/dev.en", "/dekoenization/dev/dev.vi",
            "/dekoenization/test/test.en", "/dekoenization/test/test.vi"]
        
        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                current_extension = util_ge.get_fileextension(filename)
                # TODO: Once "dev" and/or "test" data is included, the naming has to be adjusted
                #current_filename_withoutextension = util_ge.get_filename_without_extension(filename)
                current_filename_withoutextension = "train"

                # Vietnamese - Chinese
                if filename in files_cn_vi:
                    if current_extension == 'vi':
                        new_extension = 'vie'
                        new_aligned_lang = 'zho'
                    elif current_extension == 'cn':
                        new_extension = 'zho'
                        new_aligned_lang = 'vie'

                # Vietnamese - English
                if filename in files_en_vi:
                    if current_extension == 'vi':
                        new_extension = 'vie'
                        new_aligned_lang = 'eng'
                    elif current_extension == 'en':
                        new_extension = 'eng'
                        new_aligned_lang = 'vie'

                # Vietnamese - French
                if filename in files_fr_vi:
                    if current_extension == 'vi':
                        new_extension = 'vie'
                        new_aligned_lang = 'fra'
                    elif current_extension == 'fr':
                        new_extension = 'fra'
                        new_aligned_lang = 'vie'

                # Vietnamese - Japanese
                if filename in files_ja_vi:
                    if current_extension == 'vi':
                        new_extension = 'vie'
                        new_aligned_lang = 'jap'
                    elif current_extension == 'ja':
                        new_extension = 'jap'
                        new_aligned_lang = 'vie'


                new_filename = f'{current_filename_withoutextension}-{new_aligned_lang}.{new_extension}'
                
                # Read the .txt file line-by-line
                text_lines = util_ge.read_text_file(f)

                # Write the text into a new file
                util_ge.write_text_file(f'{transform_path}{new_filename}', text_lines)

    # #########################################################################
    # TODO - Well-structured data in which each line holds one item (sentence or word)
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2023AhmadiSouthernCorpus':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        #dataset_ids = ["https://raw.githubusercontent.com/sinaahmadi/KurdishLID/main/datasets/NorthernKurdish-latn_train.txt",
                       #"https://raw.githubusercontent.com/sinaahmadi/KurdishLID/main/datasets/NorthernKurdish-arab_train.txt"]
        dataset_ids = current_dataset_info['Platform ID']

        current_dataset_files = [
            "NorthernKurdish-latn_train.txt"
            ]
        
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        for current_filename in current_dataset_files:
            raw_data_path = f'{download_path}{current_filename}'
            current_filename_withoutextension = util_ge.get_filename_without_extension(raw_data_path)
            current_extension = util_ge.get_fileextension(raw_data_path)
            
            # For Vietnamese text data
            if current_filename_withoutextension == 'NorthernKurdish-latn_train':
                new_extension = 'kmr'
                new_filename = f'{new_extension}.{new_extension}'
                """
                INPUT: "NorthernKurdish-latn_train.txt"
                OUTPUT: "kmr.kmr"
                """
                input_lines = []

                # Read the .txt file line-by-line
                with open(f'{download_path}{current_filename}', 'r') as file:
                    input_lines = file.readlines()

                # Write the text into a new file
                with open(f'{transform_path}{new_filename}', 'w') as file:
                    for line in input_lines:
                        file.write(line)

    
    # #########################################################################
    # TODO - Well-structured data in which each line holds one item (sentence or word)
    # INPUT: "eng_Latn"
    # OUTPUT: "nllbseed.eng"
    if current_dataset_key == '2023NLLBSeed':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_input_filename = "eng_Latn"
        current_output_filename = "nllbseed.eng"

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Read the .txt file line-by-line
        text_lines = util_ge.read_text_file(f'{download_path}{current_input_filename}')
        
        # Write the text into a new file
        util_ge.write_text_file(f'{transform_path}{current_input_filename}', text_lines)


    # #########################################################################
    # TODO - HuggingFace Datasets
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2023SaichyshynaMulti30k':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        #dataset_id = "turuta/Multi30k-uk"
        #dataset_id = current_dataset_info['Platform ID']

        # Create directory if not existing
        util_ge.create_directory(transform_path)
        
        # To load the dataset from local location
        loaded_local_dataset = load_from_disk(f'{download_path}/local')

        # Load current dataset (This reinitiated a new download of the data, which should not be necessary!)
        #loaded_local_dataset = load_dataset(dataset_id, cache_dir=download_path, split='train')

        """ # Outputs while inspecting the dataset and its structure
        print(len(loaded_local_dataset['train'])) # → 29000
        print(loaded_local_dataset['train'][0]) # → {'en': 'Two young, White males are outside near many bushes.', 'uk': 'Двоє молодих білих чоловіків біля багатьох кущів.'}
        print(loaded_local_dataset['train'].shape) # → (29000, 2)
        print(loaded_local_dataset['train'].num_columns) # → 2
        print(loaded_local_dataset['train'].column_names) # → ['en', 'uk']
        print(loaded_local_dataset['train'].num_rows) # → 29000
        print(loaded_local_dataset['train'].features) # → {'en': Value(dtype='string', id=None), 'uk': Value(dtype='string', id=None)}
        """

        logging.debug(f'Length of loaded_local_dataset: {len(loaded_local_dataset)}') # → 1
        logging.debug(f'Length of loaded_local_dataset["train"]: {len(loaded_local_dataset["train"])}') # → 29000

        data_ukr_eng = loaded_local_dataset['train']
        logging.debug(f'Length of data_ukrainian_eng: {len(data_ukr_eng)}') # → 29000
        
        with open(transform_path+'ukr.eng', 'w') as file:
            ukreng = data_ukr_eng['en']
            for line in ukreng:
                file.write(line)
                file.write('\n')

        with open(transform_path+'eng.ukr', 'w') as file:
            engukr = data_ukr_eng['uk']
            for line in engukr:
                file.write(line)
                file.write('\n')


"""
Sorting the (collected and) transformed Data into a normalized structure for easy processing.
INPUT: Various combinations of files, monolingual, bilingual, multilingual text data.
OUTPUT: Single file for "words" and for "sentences" per language of dataset.

Some datasets can already be considered to be "sorted" at this point and will just be copied to the new location.
"""
def sort_data(current_dataset_key, current_dataset_info, input_path, output_path):

    logging.debug(f'====== Sorting dataset')
    logging.debug(f'++++++ inputPath: {input_path}')
    logging.debug(f'++++++ outputPath: {output_path}')

    if current_dataset_key == '2001HaigKurdishNewspaper':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}kmr.kmr'
        output_file = f'{sort_path}kmr.kmr'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_sorted = []

        # TODO: Turn into "Paragraphs" instead of into "Sentences"

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        
        text_lines_fullstops = util_ge.text_lines_add_fullstop_end(text_lines_no_empty)
        # Add full stop at end of lines without one (like article headlines) 
        #   this is in order for them not to get mixed up in the following step, 
        #   in which the text lines will be split into sentences.
        text_lines_sorted = util_ge.text_lines_to_sentences_sophisticated(text_lines_fullstops)

        # Sort sentences into text lines
        #text_lines_sorted = util_ge.text_lines_long_to_sentences(text_lines_no_empty)
        
        text_lines_cleaned = util_ge.text_lines_remove_almost_empty_lines(text_lines_sorted)
        text_lines_output = util_ge.text_lines_remove_excessive_punctuation(text_lines_cleaned)

        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_output)

    
    if current_dataset_key == '2013EsmailiPewan':
        transform_path = f'{input_path}{current_dataset_key}/Kurmanji/docs2/'
        sort_path = f'{output_path}{current_dataset_key}/'
        output_file = f'{sort_path}kmr.kmr'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_input = []

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                for line in text_lines_current_file:
                    text_lines_input.append(line)

        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_long_to_sentences(text_lines_no_empty)
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)


    if current_dataset_key == '2016ElliottMulti30k':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        output_file_name_fra = f'{sort_path}deu_eng.fra'
        output_file_name_deu = f'{sort_path}eng_fra.deu'
        output_file_name_eng = f'{sort_path}fra_deu.eng'

        text_lines_fra_train = []
        text_lines_deu_train = []
        text_lines_eng_train = []
        text_lines_fra_val = []
        text_lines_deu_val = []
        text_lines_eng_val = []

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                if util_ge.get_fileextension(f) == 'fra':
                    if util_ge.get_filename_without_extension(f)[0] == 't':
                        for line in text_lines_current_file:
                            text_lines_fra_train.append(line)
                    elif util_ge.get_filename_without_extension(f)[0] == 'v':
                        for line in text_lines_current_file:
                            text_lines_fra_val.append(line)

                elif util_ge.get_fileextension(f) == 'deu':
                    if util_ge.get_filename_without_extension(f)[0] == 't':
                        for line in text_lines_current_file:
                            text_lines_deu_train.append(line)
                    elif util_ge.get_filename_without_extension(f)[0] == 'v':
                        for line in text_lines_current_file:
                            text_lines_deu_val.append(line)

                elif util_ge.get_fileextension(f) == 'eng':
                    if util_ge.get_filename_without_extension(f)[0] == 't':
                        for line in text_lines_current_file:
                            text_lines_eng_train.append(line)
                    elif util_ge.get_filename_without_extension(f)[0] == 'v':
                        for line in text_lines_current_file:
                            text_lines_eng_val.append(line)
        # Combine "train" and "val" data
        text_lines_fra = []
        for line in text_lines_fra_train:
            text_lines_fra.append(line)
        for line in text_lines_fra_val:
            text_lines_fra.append(line)

        text_lines_deu = []
        for line in text_lines_deu_train:
            text_lines_deu.append(line)
        for line in text_lines_deu_val:
            text_lines_deu.append(line)

        text_lines_eng = []
        for line in text_lines_eng_train:
            text_lines_eng.append(line)
        for line in text_lines_eng_val:
            text_lines_eng.append(line)

        # Save text file
        util_ge.write_text_file(output_file_name_fra, text_lines_fra)
        util_ge.write_text_file(output_file_name_deu, text_lines_deu)
        util_ge.write_text_file(output_file_name_eng, text_lines_eng)

    if current_dataset_key == '2016MatrasKurdishDialectDatabase':
        pass

    if current_dataset_key == '2016UniMorphNorthernKurdish':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}kmr.kmr'
        output_file = f'{sort_path}kmr.kmr'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_sorted = []

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Only keep second word of line
        for line in text_lines_input:
            text_lines_sorted.append(line.split('\t')[1])
        
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)

    if current_dataset_key == '2017LuongNMT':
        pass

    if current_dataset_key == '2018CraveApertiumNorthernKurdish':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}kmr.kmr'
        output_file = f'{sort_path}kmr.kmr'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_input)

    if current_dataset_key == '2018GraveFasttextWordVectors':
        pass

    if current_dataset_key == '2020AhmadiKurdishTokenization':
        pass

    if current_dataset_key == '2020FatihkurtKurdishTwitter':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}kmr.kmr'
        output_file = f'{sort_path}kmr.kmr'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Remove special characters such as emoticons
        text_lines_sorted = util_ge.text_lines_remove_special_characters(text_lines_input)
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)

    if current_dataset_key == '2020LeichtfußFreeDict':
        pass

    if current_dataset_key == '2021BfsujasonMAC':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)

                if util_ge.get_fileextension(f) == 'zho':
                    output_file = f'{sort_path}eng.zho'
                    # Save text file
                    util_ge.write_text_file(output_file, text_lines_current_file)

                elif util_ge.get_fileextension(f) == 'eng':
                    output_file = f'{sort_path}zho.eng'
                    # Save text file
                    util_ge.write_text_file(output_file, text_lines_current_file)

            

    if current_dataset_key == '2021DoanPhoMT':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        output_file_name_vie = f'{sort_path}eng.vie'
        output_file_name_eng = f'{sort_path}vie.eng'

        text_lines_vie = []
        text_lines_eng = []

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                if util_ge.get_fileextension(f) == 'vie':
                    for line in text_lines_current_file:
                        text_lines_vie.append(line)
                elif util_ge.get_fileextension(f) == 'eng':
                    for line in text_lines_current_file:
                        text_lines_eng.append(line)

        # Save text file
        util_ge.write_text_file(output_file_name_vie, text_lines_vie)
        util_ge.write_text_file(output_file_name_eng, text_lines_eng)

    
    if current_dataset_key == '2022DabreMorisienMT':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        #TODO: Turn the sorting for words vs. sentences into a function again!
        #TODO: Also keep track of the alignment while sorting for words vs. sentences
        #      Just because a concept only needs a word in language A, does not mean, it will be short in language B!
        
        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Save text file
                util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)

    if current_dataset_key == '2022NgoSynthetic':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)
        
        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Save text file
                util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)

    if current_dataset_key == '2023AhmadiSouthernCorpus':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)
        
        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Save text file
                util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)


    if current_dataset_key == '2023NLLBSeed':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)
        
        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = "eng.eng"
                
                # Save text file
                util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)

    if current_dataset_key == '2023SaichyshynaMulti30k':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(sort_path)
        
        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Save text file
                util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)


"""
Cleaning the (collected and transformed and) sorted Data into a normalized structure for easy processing.
INPUT: Single file for "words" and for "sentences" per language of dataset.
OUTPUT: The same files, but now containing cleaned text (normalized encoding, no special characters, removal of weird formatting).

Some datasets can already be considered to be "cleaned" at this point and will just be copied to the new location.
"""
def clean_data(current_dataset_key, current_dataset_info, input_path, output_path):

    logging.debug(f'====== Cleaning dataset')
    logging.debug(f'++++++ inputPath: {input_path}')
    logging.debug(f'++++++ outputPath: {output_path}')

    if current_dataset_key == '2001HaigKurdishNewspaper':
        # Cleaning happens in sorting step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2013EsmailiPewan':
        #util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)
        # TODO: Turn into "Paragraphs" instead of into "Sentences"
        sort_path = f'{input_path}{current_dataset_key}/'
        clean_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(clean_path)

        # Iterate over files in that directory
        for filename in os.listdir(sort_path):
            f = os.path.join(sort_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Remove empty lines
                text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_current_file)
                logging.debug(f'text_lines_no_empty[0]: {text_lines_no_empty[0]}')

                # Add full stop at end of lines without one (like article headlines) 
                text_lines_fullstops = util_ge.text_lines_add_fullstop_end(text_lines_no_empty)
                logging.debug(f'text_lines_fullstops[0]: {text_lines_fullstops[0]}')

                # From text lines to clean sentences (per line)
                text_lines_sorted = util_ge.text_lines_to_sentences_sophisticated(text_lines_fullstops)
                logging.debug(f'text_lines_sorted[0]: {text_lines_sorted[0]}')

                # Some minor post-processing
                #text_lines_cleaned = util_ge.text_lines_remove_almost_empty_lines(text_lines_sorted)
                #logging.debug(f'text_lines_cleaned[0]: {text_lines_cleaned[0]}')
                #text_lines_output = util_ge.text_lines_remove_excessive_punctuation(text_lines_cleaned)
                #logging.debug(f'clean_path+current_filename: {clean_path}{current_filename}')
                #logging.debug(f'text_lines_output[0]: {text_lines_output[0]}')
                
                # Save text file
                util_ge.write_text_file_lines(f'{clean_path}{current_filename}', text_lines_sorted)


    if current_dataset_key == '2016ElliottMulti30k':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2016MatrasKurdishDialectDatabase':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2016UniMorphNorthernKurdish':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2017LuongNMT':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2018CraveApertiumNorthernKurdish':
        sort_path = f'{input_path}{current_dataset_key}/'
        clean_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(clean_path)

        # Iterate over files in that directory
        for filename in os.listdir(sort_path):
            f = os.path.join(sort_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Remove empty lines
                text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_current_file)
                logging.debug(f'text_lines_no_empty[0]: {text_lines_no_empty[0]}')

                # Add full stop at end of lines without one (like article headlines) 
                text_lines_fullstops = util_ge.text_lines_add_fullstop_end(text_lines_no_empty)
                logging.debug(f'text_lines_fullstops[0]: {text_lines_fullstops[0]}')

                # From text lines to clean sentences (per line)
                text_lines_sorted = util_ge.text_lines_to_sentences_sophisticated(text_lines_fullstops)
                logging.debug(f'text_lines_sorted[0]: {text_lines_sorted[0]}')

                # Some minor post-processing
                text_lines_cleaned = util_ge.text_lines_remove_almost_empty_lines(text_lines_sorted)
                logging.debug(f'text_lines_cleaned[0]: {text_lines_cleaned[0]}')

                text_lines_output = util_ge.text_lines_remove_excessive_punctuation(text_lines_cleaned)
                logging.debug(f'text_lines_output[0]: {text_lines_output[0]}')

                logging.debug(f'clean_path+current_filename: {clean_path}{current_filename}')
                logging.debug(f'text_lines_output[0]: {text_lines_output[0]}')
                # Save text file
                util_ge.write_text_file_lines(f'{clean_path}{current_filename}', text_lines_output)



    if current_dataset_key == '2018GraveFasttextWordVectors':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2020AhmadiKurdishTokenization':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2020FatihkurtKurdishTwitter':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2020LeichtfußFreeDict':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2021BfsujasonMAC':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2021DoanPhoMT':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2022AhmadiInterdialect':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2022DabreMorisienMT':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2022NgoSynthetic':
        sort_path = f'{input_path}{current_dataset_key}/'
        clean_path = f'{output_path}{current_dataset_key}/'
        # Create directory if not existing
        util_ge.create_directory(clean_path)

        # Iterate over files in that directory
        for filename in os.listdir(sort_path):
            f = os.path.join(sort_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                current_filename = util_ge.get_filename_with_extension(f)
                
                # Remove empty lines
                text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_current_file)
                #logging.debug(f'text_lines_no_empty[0]: {text_lines_no_empty[0]}')

                # Add full stop at end of lines without one (like article headlines) 
                text_lines_fullstops = util_ge.text_lines_add_fullstop_end(text_lines_no_empty)
                #logging.debug(f'text_lines_fullstops[0]: {text_lines_fullstops[0]}')

                # From text lines to clean sentences (per line)
                text_lines_sorted = util_ge.text_lines_to_sentences_sophisticated(text_lines_fullstops)
                #logging.debug(f'text_lines_sorted[0]: {text_lines_sorted[0]}')

                # Some minor post-processing
                text_lines_cleaned = util_ge.text_lines_remove_almost_empty_lines(text_lines_sorted)
                #logging.debug(f'text_lines_cleaned[0]: {text_lines_cleaned[0]}')

                text_lines_output = util_ge.text_lines_remove_excessive_punctuation(text_lines_cleaned)
                #logging.debug(f'text_lines_output[0]: {text_lines_output[0]}')

                text_lines_detokenized = util_ge.text_lines_detokenize(text_lines_output)

                # Save text file
                util_ge.write_text_file_lines(f'{clean_path}{current_filename}', text_lines_detokenized)


        #util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)
        util_ge.rename_files_in_directory(f'{output_path}{current_dataset_key}/', "right", 3)
        # input_path, direction_to_keep, number_chars_of_name_to_keep

    if current_dataset_key == '2023AhmadiSouthernCorpus':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2023NLLBSeed':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)

    if current_dataset_key == '2023SaichyshynaMulti30k':
        # TODO: Implement cleaning - For now: Copy content from Sort-Step
        util_ge.move_files_from_directory(input_path, output_path, current_dataset_key)



""" INPUT parameter: 
    info_datasets_ready,          # Only select datasets marked "ready"
    data_raw_dataset_path,        # Location of raw data to clean
    data_transform_datasets_path, # (Temp) Location for transformed data
    data_sort_datasets_path,      # (Temp) Location for sorted data
    data_clean_datasets_path,     # Location for cleaned data
    execute_transforming,         # Flag if transforming step should be done (default=True)
    execute_sorting,              # Flag if sorting step should be done (default=True)
    execute_cleaning              # Flag if cleaning step should be done (default=True) 
"""
def main(info_datasets_ready, 
         data_raw_dataset_path, 
         data_transform_datasets_path, 
         data_sort_datasets_path, 
         data_clean_datasets_path,
         execute_transforming,
         execute_sorting,
         execute_cleaning):

    # Process all datasets for which info was provided:
    for key in info_datasets_ready.keys():
        current_dataset_key = key

        # Processing capabilities guaranteed for following datasets
        available_dataset_keys = [
            '2001HaigKurdishNewspaper',
            '2013EsmailiPewan',
            '2016ElliottMulti30k',
            #'2016MatrasKurdishDialectDatabase',
            '2016UniMorphNorthernKurdish',
            '2017LuongNMT',
            '2018CraveApertiumNorthernKurdish',
            #'2018GraveFasttextWordVectors',
            #'2020AhmadiKurdishTokenization',
            '2020FatihkurtKurdishTwitter',
            #'2020LeichtfußFreeDict',
            '2021BfsujasonMAC',
            '2021DoanPhoMT',
            '2022AhmadiInterdialect',
            '2022DabreMorisienMT',
            '2022NgoSynthetic',
            '2023AhmadiSouthernCorpus',
            '2023NLLBSeed',
            '2023SaichyshynaMulti30k']
        
        if current_dataset_key in available_dataset_keys:
            logging.debug(f'====   Dataset: {current_dataset_key}')
            
            # Take the entire dataset (info) and continue
            current_dataset_info = info_datasets_ready[key]

            if execute_transforming == True:
                transform_data(current_dataset_key,
                               current_dataset_info,
                               data_raw_dataset_path,
                               data_transform_datasets_path)

            if execute_sorting == True:
                sort_data(current_dataset_key,
                          current_dataset_info,
                          data_transform_datasets_path,
                          data_sort_datasets_path)

            if execute_cleaning == True:
                clean_data(current_dataset_key,
                           current_dataset_info,
                           data_sort_datasets_path,
                           data_clean_datasets_path)


if __name__ == "__main__":
    main()