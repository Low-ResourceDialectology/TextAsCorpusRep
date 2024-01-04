# -*- coding: utf-8 -*-
# Python Script for transforming, sorting and cleaning collected text data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################
"""
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
    # INPUT: "2001HaigKurdishNewspaper/ccknt.txt"
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
    # TODO - Data in PDF format
    # INPUT: "2012MorisienGramer/GRAMER_KREOL_MORISIEN_Volim_1_Dokiman_Re-2.pdf"
    # OUTPUT: "mor.mor"
    if current_dataset_key == '2012MorisienGramer':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'mor.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{output_file}')

    # #########################################################################
    # TODO - Data to be extracted
    # TODO - Data in form of many different files
    # INPUT: "2013EsmailiPewan/Pewan.zip" which is a zip-file
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
    # INPUT: "2016UniMorphNorthernKurdish/kmr"
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
    # INPUT: "2018CraveApertiumNorthernKurdish/barzani_newroz.kmr.txt", "kurdistannews.txt", "xurmatu.txt", "xurm-trans-hand.txt"
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
    # INPUT: "2021DoanPhoMT/detokenization/train/train.en"
    # OUTPUT: "2021DoanPhoMT/train-vie.eng"
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
    # TODO - Data in PDF format
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2021MorisienDictionaryEnglish':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'eng.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{output_file}')

    # #########################################################################
    # TODO - Data in PDF format
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2021MorisienEducationalBooksPupil':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'mor.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{filename}-{output_file}')

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
        
        # Write the Morisien text into a new file
        #with open(transform_path+'dabre_dataset', 'w') as file:
        #	for dataset_row in data_morisien:
        #		file.write(str(dataset_row))
        #		file.write('\n')
        #print(data_morisien)

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
                current_filename_withoutextension = util_ge.get_filename_without_extension(filename)

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
                util_ge.write_text_file_lines(f'{transform_path}{new_filename}', text_lines)

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
    # TODO - Data in form of many different files
    # INPUT: ""
    # OUTPUT: ""
    if current_dataset_key == '2023DevVirahsawmyBoukieBananePDF':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
    
        # Create directory if not existing
        util_ge.create_directory(transform_path)

        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        output_file = 'mor.mor'

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Iterate over files in that directory
        for filename in os.listdir(download_path):
            f = os.path.join(download_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                util_ge.pdf_to_txt_file(f, f'{transform_path}{filename}-{output_file}')

    # #########################################################################
    # TODO - Simple txt format mainly in need of sorting
    # INPUT: "2023DevVirahsawmyBoukieBananeWeb/mor-boukiebanane_com.txt"
    # OUTPUT: "mor-boukiebanane_com.mor"
    if current_dataset_key == '2023DevVirahsawmyBoukieBananeWeb':
        download_path = inputPath + f'{current_dataset_key}/'
        transform_path = outputPath + f'{current_dataset_key}/'
        current_input_filename = "mor-boukiebanane_com.txt"
        current_output_filename = "mor-boukiebanane_com.mor"

        # Create directory if not existing
        util_ge.create_directory(transform_path)

        # Read the .txt file line-by-line
        input_lines = util_ge.read_text_file(f'{download_path}{current_input_filename}')
        output_lines = []

        for line in input_lines:
            if not line == '':
                output_lines.append(line)

        # Write the text into a new file
        util_ge.write_text_file(f'{transform_path}{current_output_filename}', output_lines)

    # #########################################################################
    # TODO - Well-structured data in which each line holds one item (sentence or word)
    # INPUT: "2023NLLBSeed/eng_Latn"
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


        #

        # # Monolingual
        # # Read data from json file (jsonl is just a "long json")
        # # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
        # input_lines = [json.loads(line)
        #     for line in open(download_path+'data/cr/cr_train.jsonl', 'r', encoding='utf-8')]

        # # The input is on the format:   {"input": "morisien_text_here", "target": ""}
        # # Extracting the Morisien texts and store them in data
        # data = [input_lines[index]['input']
        #     for index in range(len(input_lines))]

        # # Removing the first (empty) element from the list of text lines
        # data.pop(0)

        # #print(data[3]) # Debugging to check content

        # # Write the Morisien text into a new file
        # with open(transform_path+'mor.mor', 'w') as file:
        #     for line in data:
        #         file.write(line)
        #         file.write('\n')

        # # Bilingual - English
        # # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
        # #input_lines_dev = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
        # #input_lines_test = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
        # input_lines_train = [json.loads(line)
        #         for line in open(download_path+'data/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
        # #input_lines = input_lines_dev + input_lines_test + input_lines_train
        # input_lines = input_lines_train

        # # The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
        # # Extracting the English and Morisien texts and store them in data
        # data_eng_mor = [input_lines[index]['input']
        #         for index in range(len(input_lines))]
        # data_mor_eng = [input_lines[index]['target']
        #         for index in range(len(input_lines))]

        # # Write the English text (aligned with Morisien) into a new file
        # with open(transform_path+'mor.eng', 'w') as file:
        #     for line in data_eng_mor:
        #         file.write(line)
        #         file.write('\n')
        # # Write the Morisien text (aligned with English) into a new file
        # with open(transform_path+'eng.mor', 'w') as file:
        #     for line in data_mor_eng:
        #         file.write(line)
        #         file.write('\n')

        # # Bilingual - Fench 
        # # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
        # #input_lines_dev = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
        # #input_lines_test = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
        # input_lines_train = [json.loads(line)
        #         for line in open(download_path+'data/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
        # #input_lines = input_lines_dev + input_lines_test + input_lines_train
        # input_lines = input_lines_train

        # # The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
        # # Extracting the English and Morisien texts and store them in data
        # data_fra_mor = [input_lines[index]['input']
        #         for index in range(len(input_lines))]
        # data_mor_fra = [input_lines[index]['target']
        #         for index in range(len(input_lines))]

        # # Write the French text (aligned with Morisien) into a new file
        # with open(transform_path+'mor.fra', 'w') as file:
        #     for line in data_fra_mor:
        #         file.write(line)
        #         file.write('\n')
        # # Write the Morisien text (aligned with French) into a new file
        # with open(transform_path+'fra.mor', 'w') as file:
        #     for line in data_mor_fra:
        #         file.write(line)
        #         file.write('\n')

        # """
        # Backup due to loading with huggingface instead of downloading files directly now
        # # Monolingual
        # # Read data from json file (jsonl is just a "long json")
        # # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
        # input_lines = [json.loads(line)
        #     for line in open(download_path+'data/cr/cr_train.jsonl', 'r', encoding='utf-8')]

        # # The input is on the format:   {"input": "morisien_text_here", "target": ""}
        # # Extracting the Morisien texts and store them in data
        # data = [input_lines[index]['input']
        #     for index in range(len(input_lines))]

        # # Removing the first (empty) element from the list of text lines
        # data.pop(0)

        # #print(data[3]) # Debugging to check content

        # # Write the Morisien text into a new file
        # with open(transform_path+'mor.mor', 'w') as file:
        #     for line in data:
        #         file.write(line)
        #         file.write('\n')

        # # Bilingual - English
        # # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
        # #input_lines_dev = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
        # #input_lines_test = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
        # input_lines_train = [json.loads(line)
        #         for line in open(download_path+'data/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
        # #input_lines = input_lines_dev + input_lines_test + input_lines_train
        # input_lines = input_lines_train

        # # The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
        # # Extracting the English and Morisien texts and store them in data
        # data_eng_mor = [input_lines[index]['input']
        #         for index in range(len(input_lines))]
        # data_mor_eng = [input_lines[index]['target']
        #         for index in range(len(input_lines))]

        # # Write the English text (aligned with Morisien) into a new file
        # with open(transform_path+'mor.eng', 'w') as file:
        #     for line in data_eng_mor:
        #         file.write(line)
        #         file.write('\n')
        # # Write the Morisien text (aligned with English) into a new file
        # with open(transform_path+'eng.mor', 'w') as file:
        #     for line in data_mor_eng:
        #         file.write(line)
        #         file.write('\n')

        # # Bilingual - Fench 
        # # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
        # #input_lines_dev = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
        # #input_lines_test = [json.loads(line)
        # #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
        # input_lines_train = [json.loads(line)
        #         for line in open(download_path+'data/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
        # #input_lines = input_lines_dev + input_lines_test + input_lines_train
        # input_lines = input_lines_train

        # # The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
        # # Extracting the English and Morisien texts and store them in data
        # data_fra_mor = [input_lines[index]['input']
        #         for index in range(len(input_lines))]
        # data_mor_fra = [input_lines[index]['target']
        #         for index in range(len(input_lines))]

        # # Write the French text (aligned with Morisien) into a new file
        # with open(transform_path+'mor.fra', 'w') as file:
        #     for line in data_fra_mor:
        #         file.write(line)
        #         file.write('\n')
        # # Write the Morisien text (aligned with French) into a new file
        # with open(transform_path+'fra.mor', 'w') as file:
        #     for line in data_mor_fra:
        #         file.write(line)
        #         file.write('\n')
        # """



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

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_long_to_sentences(text_lines_no_empty)
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)

    # TODO: Something weird going on here that messed up some of the lines
    # such as: "K o u m a  f i n n  d e z a  s o u l igne dan rapor lortograf, Akademi Kreol Morisien"
    if current_dataset_key == '2012MorisienGramer':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}mor.mor'
        output_file = f'{sort_path}mor.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = []
        #text_lines_sorted = util_ge.text_lines_to_sentences(text_lines_no_empty)
        for line in text_lines_no_empty:
            fixed_line = ""

            # WHAT AM I EVEN DOING HERE?! COUNTING EMPTY SPACES IN TEXT LINES?!?!
            # Just do it for every line and be done with it!
            # Oh... Right... That's why! → Back to the idiotic way (at least it works!)
            """
            for index in range(len(line)):
                if not line[index] == ' ':
                    fixed_line = fixed_line + line[index]
                elif line[index] == ' ' and line[index+1] == ' ':
                    fixed_line = fixed_line + line[index]
            text_lines_sorted.append(fixed_line)
            """
            
            if len(line) > 7 and len(line) < 25:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 24 and len(line) < 35:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 34 and len(line) < 45:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 44 and len(line) < 55:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[35] == ' ' and line[37] == ' ' and line[39] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[36] == ' ' and line[38] == ' ' and line[40] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 54 and len(line) < 65:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[35] == ' ' and line[37] == ' ' and line[39] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[36] == ' ' and line[38] == ' ' and line[40] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)

            elif len(line) > 64:
                # Detect annomaly at start of line
                if line[1] == ' ' and line[3] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly at end of line
                elif line[-2] == ' ' and line[-4] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[19] == ' ' and line[21] == ' ' and line[23] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[20] == ' ' and line[22] == ' ' and line[24] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[29] == ' ' and line[31] == ' ' and line[33] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[30] == ' ' and line[32] == ' ' and line[34] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[35] == ' ' and line[37] == ' ' and line[39] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[36] == ' ' and line[38] == ' ' and line[40] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[43] == ' ' and line[45] == ' ' and line[47] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[44] == ' ' and line[46] == ' ' and line[48] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[47] == ' ' and line[49] == ' ' and line[51] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[57] == ' ' and line[59] == ' ' and line[61] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[58] == ' ' and line[60] == ' ' and line[62] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[59] == ' ' and line[61] == ' ' and line[63] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                # Detect annomaly in middle of line
                elif line[60] == ' ' and line[62] == ' ' and line[64] == ' ':
                    for index in range(len(line)):
                        if not line[index] == ' ':
                            fixed_line = fixed_line + line[index]
                        elif line[index] == ' ' and line[index+1] == ' ':
                            fixed_line = fixed_line + line[index]
                    text_lines_sorted.append(fixed_line)
                else:
                    text_lines_sorted.append(line)
            else:
                text_lines_sorted.append(line)
            
        # Dirty Quick-Fix for handling full stops such as "Dr." or "..."
        text_lines_replaced = []
        for line in text_lines_sorted:
            text_lines_replaced.append(line.replace('Dr.', 'Doctor').replace('M.A.', 'MA').replace('Mm.','Mademoiselle').replace('Mm ','Mademoiselle ').replace('M. ','Monsieur '))

        text_lines_dirty_fix = util_ge.text_lines_short_to_sentences(text_lines_replaced)

        text_lines_output = []
        # Remove lines only containing a full stop
        for line in text_lines_dirty_fix:
            if not line == '.':
                text_lines_output.append(line)

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

        text_lines_fra = []
        text_lines_deu = []
        text_lines_eng = []

        # Iterate over files in that directory
        for filename in os.listdir(transform_path):
            f = os.path.join(transform_path, filename)
            # Checking if it is a file
            if os.path.isfile(f):
                # Read text file to text lines
                text_lines_current_file = util_ge.read_text_file(f)
                if util_ge.get_fileextension == 'fra':
                    for line in text_lines_current_file:
                        text_lines_fra.append(line)
                elif util_ge.get_fileextension == 'deu':
                    for line in text_lines_current_file:
                        text_lines_deu.append(line)
                elif util_ge.get_fileextension == 'eng':
                    for line in text_lines_current_file:
                        text_lines_eng.append(line)

        # Save text file
        util_ge.write_text_file_lines(output_file_name_fra, text_lines_fra)
        util_ge.write_text_file_lines(output_file_name_deu, text_lines_deu)
        util_ge.write_text_file_lines(output_file_name_eng, text_lines_eng)

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

        text_lines_sorted = []

        # Read text file to text lines
        text_lines_input = util_ge.read_text_file(input_file)
        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_long_to_sentences(text_lines_no_empty)
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)

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
        util_ge.write_text_file_lines(output_file_name_vie, text_lines_vie)
        util_ge.write_text_file_lines(output_file_name_eng, text_lines_eng)

    """
    Each page of this dictionary is of the form

        DIKS YON ER KREOL MORISYEN  
 
        3 
        A 
        abandone  (abandon) [from Fre 
        abandonner] : to abandon. Akoz samem, 
        ler mo ti ena sizan mo ti abandon 
        posibilite vinn enn gran pent = Because 
        (of) that, when I was six years old I 
        missed the  chance to become a great 
        painter.  Mo finn abandon li tusel lakaz = I 
        left him alone at home.  
        abba  : in vain. Mo'nn seye me abba = I've 
        tried but in vain.  
        abi [from Fre abus] : abuse  
        abitan  [from Fre habitant] : inhabitant.  So 
        abitan zot katorz = Its inhab itants number 
        fourteen.  
        abite  [from Fre habiter] : to inhabit. 
        Dezyem  planet la ti abite par enn vantar = 

    Idea: 
    1. Remove the headline
    2. Remove the page number
    3. Remove the letter-indicator
    4. Put everything into a single string/text line
    5. Split at the ":"
        → abandone  (abandon) [from Fre abandonner] 
        → : to abandon. Akoz samem, ler mo ti ena sizan mo ti abandon posibilite vinn enn gran pent = Because (of) that, when I was six years old I missed the  chance to become a great painter.  Mo finn abandon li tusel lakaz = I left him alone at home.  abba  
        → : in vain. Mo'nn seye me abba = I've tried but in vain.  abi [from Fre abus] 
    6. Now split at the last full stop
        → abandone  (abandon) [from Fre abandonner] 
        → : to abandon. Akoz samem, ler mo ti ena sizan mo ti abandon posibilite vinn enn gran pent = Because (of) that, when I was six years old I missed the  chance to become a great painter.  Mo finn abandon li tusel lakaz = I left him alone at home
            .  
            abba  
        → : in vain. Mo'nn seye me abba = I've tried but in vain
            .  
            abi [from Fre abus] 
    7. Recombine 
        For the very first item:
            Element in front of : with element behind the : but without the part after the .
        For each following item:
            Element after the . but in front of : with element behind the : but without the part after the .
    """
    if current_dataset_key == '2021MorisienDictionaryEnglish':
        # TODO: The above steps
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}eng.mor'
        output_file = f'{sort_path}eng.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)

        text_lines_input = []

        # Iterate over files in that directory
        # Read text file to text lines
        text_lines_current_file = util_ge.read_text_file(input_file)
        text_lines_useful = text_lines_current_file[40:9010]

        for line in text_lines_useful:
            if not line == "    DIKS YON ER KREOL MORISYEN  ":
                text_lines_input.append(line)

        # Remove empty lines
        text_lines_no_empty = util_ge.text_lines_remove_empty_lines(text_lines_input)
        # Sort sentences into text lines
        text_lines_sorted = util_ge.text_lines_short_to_sentences(text_lines_no_empty)
        # Save text file
        util_ge.write_text_file_lines(output_file, text_lines_sorted)

    if current_dataset_key == '2021MorisienEducationalBooksPupil':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        output_file = f'{sort_path}mor.mor'
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
        text_lines_sorted = util_ge.text_lines_short_to_sentences(text_lines_no_empty)
        # Remove some of the silly transformations such as "." as a single line
        text_lines_output = []
        for line in text_lines_sorted:
            if len(line) > 4:
                text_lines_output.append(line)

        # Save text file        
        util_ge.write_text_file_lines(output_file, text_lines_output)

    if current_dataset_key == '2021MorisienEducationalBooksTeacher':
        pass

    if current_dataset_key == '2022AhmadiInterdialect':
        # TODO: Add full stop (.) at end of each sentence.
        # Remove special characters spanning text-lines "line_1, line_2, line_3"
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

    if current_dataset_key == '2023DevVirahsawmyBoukieBananePDF':
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
                
                # ================================
                # Sentences
                current_content = []

                # Combine all lines into one
                one_line = ""

                for line in text_lines_current_file:
                    # Also remove all line breaks
                    one_line = one_line + line.replace('\n', '')

                # Replace all special characters with a space
                one_line_no_special = re.sub('[^A-Za-z0-9.,!?:;()]+', ' ', one_line)

                # Replace all single characters with a space
                one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
                
                # Replace all double spaces with one space
                one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
                
                # Remove leading and trailing spaces
                one_line_stripped = one_line_no_doublespace.strip()
                

                one_line_split = one_line_stripped.split('.')
                #logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

                for sentence in one_line_split:
                    current_content.append(sentence+'.')

                # Save text file
                util_ge.write_text_file_lines(f'{sort_path}{current_filename}', current_content)

    if current_dataset_key == '2023DevVirahsawmyBoukieBananeWeb':
        transform_path = f'{input_path}{current_dataset_key}/'
        sort_path = f'{output_path}{current_dataset_key}/'
        input_file = f'{transform_path}mor-boukiebanane_com.mor'
        # Create directory if not existing
        util_ge.create_directory(sort_path)
    
        # Read text file to text lines
        text_lines_current_file = util_ge.read_text_file(input_file)
        current_filename = util_ge.get_filename_with_extension(input_file)
        current_file_out = f'{sort_path}{current_filename}'
        
        # ================================
        # Sentences
        current_content = []

        # Combine all lines into one
        one_line = ""

        for line in text_lines_current_file:
            # Also remove all line breaks
            one_line = one_line + line.replace('\n', '')

        # Replace all special characters with a space
        one_line_no_special = re.sub('[^A-Za-z0-9.,!?:;()]+', ' ', one_line)

        # Replace all single characters with a space
        one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
        
        # Replace all double spaces with one space
        one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
        
        # Remove leading and trailing spaces
        one_line_stripped = one_line_no_doublespace.strip()
        

        one_line_split = one_line_stripped.split('.')
        #logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

        for sentence in one_line_split:
            current_content.append(sentence+'.')

        util_ge.write_text_file_lines(current_file_out, current_content)
        #with open(current_file_out, 'w') as file:
            #for line in one_line_split:
                #if util.check_for_non_empty_string(line):
                #    file.write(line.strip().replace('  ',' '))
                #    file.write('\n')

        """
        # ================================
        # Words
        # Combine all lines into one
        one_line = ""

        for line in text_lines_current_file:
            # Also remove all line breaks
            one_line = one_line + line

        #logging.debug(f'one_line[0:100] = {one_line[0:100]}')

        #one_line_split = one_line.split('.')
        #logging.debug(f'one_line_split[0:10] = {one_line_split[0:10]}')

        # Replace all line breaks with a space
        one_line_no_breaks = re.sub('\n', ' ', one_line)
        
        # Replace all special characters with a space
        one_line_no_special = re.sub('[^A-Za-z0-9]+', ' ', one_line_no_breaks)

        # Replace all single characters with a space
        one_line_no_singlechar = re.sub(r'\b[a-zA-Z]\b', ' ', one_line_no_special)
        
        # Replace all double spaces with one space
        one_line_no_doublespace = re.sub(' +', ' ', one_line_no_singlechar)
        
        # Remove leading and trailing spaces
        one_line_stripped = one_line_no_doublespace.strip()

        # Make all text lower case
        one_line_no_uppercase = one_line_stripped.lower()

        words = one_line_no_uppercase.split(" ")

        word_count = {}

        for word in words:
            if word not in word_count:
                word_count[word] = 1
            elif word in word_count:
                word_count[word] += 1
            
        #current_content.append(sentence)

        # Sort dictionary 
        sorted_word_count = sorted(word_count.items(), key=lambda x:x[1], reverse = True)
        sorted_word_count_dict = dict(sorted_word_count)

        # Serializing json
        json_object = json.dumps(sorted_word_count_dict, indent=4)
        
        # Writing to sample.json
        with open(analyze_path_pdf+filename+'.json', "w") as outfile:
            outfile.write(json_object)
        """
        # Save text file
        #util_ge.write_text_file(f'{sort_path}{current_filename}', text_lines_current_file)

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

    sys.exit()

    # ===========================================
    # MONOLINGUAL
    # ===========================================
    def sort_dataset(transform_path, sort_path):

        # Create directory if not existing
        util_ge.create_directory(sort_path)

        # For each file in the directory
        for filename in os.listdir(transform_path):
            # Combine the directory path with the filename
            text_file = os.path.join(transform_path, filename)
            
            # Checking if it is a file
            if os.path.isfile(text_file):
                        
                logging.debug(f'  Sorting: {text_file}')

                # Get file information
                f_basename = util_ge.get_basename(text_file)
                #logging.debug(f'    f_basename: {f_basename}')
                f_ending = util_ge.get_fileextension(text_file)
                #logging.debug(f'    f_ending: {f_ending}')
                #f_size = util_ge.get_filesize_b(text_file)
                #logging.debug(f'    f_size: {f_size}')

                #
                # Monolingual vs. Bilingual → Monolingual
                #
                if f_basename == f_ending:
                    
                    sort_path_mono = sort_path + 'Monolingual/'
                    util_ge.create_directory(sort_path_mono)

                    text_words = []
                    text_sents = []

                    text_data = util_ge.read_text_file(text_file)

                    for line in text_data:

                        # Check if only a single word
                        if len(line.split(' ')) == 1:
                            text_words.append(line)
                        
                        # Otherwise multiple words
                        else:
                            text_sents.append(line)
                    
                    # Once all lines have been checked, write text (words & sents) to file

                    # In case the data contained single words
                    if len(text_words) > 0:
    
                        output_file_words = sort_path_mono + 'Words/'
                        util_ge.create_directory(output_file_words)
                        util_ge.write_text_file(output_file_words+f'{f_basename}.{f_ending}', text_words)

                    # In case the data contained sentences
                    if len(text_sents) > 0:

                        output_file_sents = sort_path_mono + 'Sentences/'
                        util_ge.create_directory(output_file_sents)
                        util_ge.write_text_file(output_file_sents+f'{f_basename}.{f_ending}', text_sents)
                    # util_ge..write_text_file(output_file, text_words)
                    # or
                    # write_text_file_lines(output_file, text_words)
                
                #
                # Monolingual vs. Bilingual → Bilingual
                #
                elif f_basename != f_ending:

                    logging.debug(f'  Sorting bilingual data for: {f_basename} and {f_ending}')
                    sort_path_bili = sort_path + 'Bilingual/'
                    util_ge.create_directory(sort_path_bili)

                    text_words = []
                    text_sents = []

                    text_data = util_ge.read_text_file(text_file)

                    for line in text_data:

                        # Check if only a single word
                        if len(line.split(' ')) == 1:
                            text_words.append(line)
                        
                        # Otherwise multiple words
                        else:
                            text_sents.append(line)
                    
                    # Once all lines have been checked, write text (words & sents) to file

                    # In case the data contained single words
                    if len(text_words) > 0:
    
                        output_file_words = sort_path_bili + 'Words/'
                        util_ge.create_directory(output_file_words)
                        util_ge.write_text_file(output_file_words+f'{f_basename}.{f_ending}', text_words)

                    # In case the data contained sentences
                    if len(text_sents) > 0:

                        output_file_sents = sort_path_bili + 'Sentences/'
                        util_ge.create_directory(output_file_sents)
                        util_ge.write_text_file(output_file_sents+f'{f_basename}.{f_ending}', text_sents)
                    # util_ge..write_text_file(output_file, text_words)
                    # or
                    # write_text_file_lines(output_file, text_words)
                else:
                    logging.debug(f'  Filename not properly formated: {text_file}')
    

    # ===========================================
    # Morisien 
    # ===========================================
    if '2022DabreMorisienMT' in dataset_list:

        transform_path = inputPath + '2022DabreMorisienMT/'
        sort_path = outputPath + '2022DabreMorisienMT/'
        logging.debug(f'  transform_path: {transform_path}')
        logging.debug(f'  sort_path: {sort_path}')
        sort_dataset(transform_path, sort_path)
        

    # ===========================================
    # Kurmanji 
    # ===========================================
    if '2022AhmadiInterdialect' in dataset_list:

        transform_path = inputPath + '2022AhmadiInterdialect/'
        sort_path = outputPath + '2022AhmadiInterdialect/'
        logging.debug(f'  transform_path: {transform_path}')
        logging.debug(f'  sort_path: {sort_path}')
        sort_dataset(transform_path, sort_path)
        

    # ===========================================
    # Vietnamese 
    # ===========================================
    if '2017LuongNMT' in dataset_list:

        transform_path = inputPath + '2017LuongNMT/'
        sort_path = outputPath + '2017LuongNMT/'
        logging.debug(f'  transform_path: {transform_path}')
        logging.debug(f'  sort_path: {sort_path}')
        sort_dataset(transform_path, sort_path)


"""
Cleaning the (collected and transformed and) sorted Data into a normalized structure for easy processing.
INPUT: Single file for "words" and for "sentences" per language of dataset.
OUTPUT: The same files, but now containing cleaned text (normalized encoding, no special characters, removal of weird formatting).

Some datasets can already be considered to be "cleaned" at this point and will just be copied to the new location.
"""
def clean_data(languages, dataset_list, inputPath, outputPath):

    print("TODO: Clean")
    return
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
        util_ge.create_directory(clean_path)

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
                                
                        #logging.debug(f'    Sorting: {text_file}')

                        f_basename = util_ge.get_basename(text_file)
                        f_ending = util_ge.get_fileending(text_file)

                        clean_path_mono_words = clean_path + 'Monolingual/Words/'
                        util_ge.create_directory(clean_path_mono_words)

                        text_words = []

                        text_data = util_ge.read_text_file(text_file)

                        for line in text_data:

                            # Only process non-empty lines
                            if util_ge.check_for_non_empty_string(line.replace("\n", "")):

                                # Remove punctuation at end of word
                                word = util_ge.remove_punctuation_end(line.replace("\n", ""))
                                text_words.append(word)

                            else:
                                pass
                        
                        util_ge.write_text_file_lines(clean_path_mono_words+f'{f_basename}.{f_ending}', text_words)

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
                                
                        #logging.debug(f'    Sorting: {text_file}')

                        f_basename = util_ge.get_basename(text_file)
                        f_ending = util_ge.get_fileending(text_file)

                        clean_path_mono_sents = clean_path + 'Monolingual/Sentences/'
                        util_ge.create_directory(clean_path_mono_sents)

                        text_sents = []

                        text_data = util_ge.read_text_file(text_file)

                        for line in text_data:

                            # TODO: clean sentences
                            #sent = util_ge.remove_punctuation_end(line)
                            #text_sents.append(sent)
                            text_sents.append(line.replace("\n", ""))
                        
                        #print(f'Some lines from text_sents: {text_sents[0:3]}')
                        #print(f'target for cleaned sents: {clean_path_mono_sents}{f_basename}.{f_ending}')
                        
                        util_ge.write_text_file_lines(clean_path_mono_sents+f'{f_basename}.{f_ending}', text_sents)


    # ===========================================
    # BILINGUAL
    # ===========================================
    def clean_bilingual(sort_path, clean_path):
        
        # Create directory if not existing
        util_ge.create_directory(clean_path)

        #
        # Check for bilingual data directories
        #
        if os.path.isdir(sort_path+'Bilingual'):
                
            #
            # Check for words data directories
            #
            if os.path.isdir(sort_path+'Bilingual/Words'):
                
                sort_path_bili_words = sort_path+'Bilingual/Words/'

                # For each file in the directory
                for filename in os.listdir(sort_path_bili_words):
                    # Combine the directory path with the filename
                    text_file = os.path.join(sort_path_bili_words, filename)
                    
                    # Checking if it is a file
                    if os.path.isfile(text_file):
                                
                        #logging.debug(f'    Sorting: {text_file}')

                        f_basename = util_ge.get_basename(text_file)
                        f_ending = util_ge.get_fileending(text_file)

                        clean_path_bili_words = clean_path + 'Bilingual/Words/'
                        util_ge.create_directory(clean_path_bili_words)

                        text_words = []

                        text_data = util_ge.read_text_file(text_file)

                        for line in text_data:

                            # Only process non-empty lines
                            if util_ge.check_for_non_empty_string(line.replace("\n", "")):

                                # Remove punctuation at end of word
                                #print(type(line)) → <class 'str'>
                                word = util_ge.remove_punctuation_end(line.replace("\n", ""))
                                text_words.append(word)
                        
                        util_ge.write_text_file_lines(clean_path_bili_words+f'{f_basename}.{f_ending}', text_words)

            #
            # Check for sentences data directories
            #
            if os.path.isdir(sort_path+'Bilingual/Sentences'):
                
                sort_path_bili_sents = sort_path+'Bilingual/Sentences/'

                # For each file in the directory
                for filename in os.listdir(sort_path_bili_sents):
                    # Combine the directory path with the filename
                    text_file = os.path.join(sort_path_bili_sents, filename)
                    
                    # Checking if it is a file
                    if os.path.isfile(text_file):
                                
                        #logging.debug(f'    Sorting: {text_file}')

                        f_basename = util_ge.get_basename(text_file)
                        f_ending = util_ge.get_fileending(text_file)

                        clean_path_bili_sents = clean_path + 'Bilingual/Sentences/'
                        util_ge.create_directory(clean_path_bili_sents)

                        text_sents = []

                        text_data = util_ge.read_text_file(text_file)

                        for line in text_data:

                            # TODO: clean sentences
                            #sent = util_ge.remove_punctuation_end(line)
                            #text_sents.append(sent)
                            text_sents.append(line.replace("\n", ""))
                        
                        #print(f'Some lines from text_sents: {text_sents[0:3]}')
                        #print(f'target for cleaned sents: {clean_path_bili_sents}{f_basename}.{f_ending}')
                        util_ge.write_text_file_lines(clean_path_bili_sents+f'{f_basename}.{f_ending}', text_sents)


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


"""
Input parameter: 
    languages_selected,           # Languages selected via input arguments
    data_raw_dataset_path,        # Location of raw data to clean
    data_transform_datasets_path, # (Temp) Location for transformed data
    data_sort_datasets_path,      # (Temp) Location for sorted data
    data_clean_datasets_path,     # Location for cleaned data
    info_datasets_ready           # Only select datasets marked "ready"
"""
def main(info_datasets_ready, 
         data_raw_dataset_path, 
         data_transform_datasets_path, 
         data_sort_datasets_path, 
         data_clean_datasets_path):

    # Process all datasets for which info was provided:
    for key in info_datasets_ready.keys():
        current_dataset_key = key

        # Processing capabilities guaranteed for following datasets
        available_dataset_keys = [
            '2001HaigKurdishNewspaper',
            '2012MorisienGramer',
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
            '2021MorisienDictionaryEnglish',
            '2021MorisienEducationalBooksPupil',
            #'2021MorisienEducationalBooksTeacher',
            '2022AhmadiInterdialect',
            '2022DabreMorisienMT',
            '2022NgoSynthetic',
            '2023AhmadiSouthernCorpus',
            '2023DevVirahsawmyBoukieBananePDF',
            '2023DevVirahsawmyBoukieBananeWeb',
            '2023NLLBSeed',
            '2023SaichyshynaMulti30k']
        
        if current_dataset_key in available_dataset_keys:
            logging.debug(f'====   Dataset: {current_dataset_key}')
            
            # Take the entire dataset (info) and continue
            current_dataset_info = info_datasets_ready[key]

            transform_data(current_dataset_key,
                           current_dataset_info,
                           data_raw_dataset_path,
                           data_transform_datasets_path)

            sort_data(current_dataset_key,
                      current_dataset_info,
                      data_transform_datasets_path,
                      data_sort_datasets_path)

            clean_data(current_dataset_key,
                       current_dataset_info,
                       data_sort_datasets_path,
                       data_clean_datasets_path)


if __name__ == "__main__":
    main()