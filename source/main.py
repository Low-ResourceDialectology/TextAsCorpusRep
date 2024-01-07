# -*- coding: utf-8 -*-
# Python Script for Multilingual Text as Corpus Repository (MTACR) project
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import argparse
import configparser
import json
import logging
import os
import sys
import textwrap

import data.datasets.download as down_ds
import data.datasets.clean as clean_ds
import data.datasets.extract_data as extract_ds
import data.webdata.download as down_wd
import data.webdata.clean as clean_wd
import data.webdata.assess_quality as assess_wd
import evals.language_ident as lid_wd
import evals.analyse_text as anal_text

""" Setup: ====================================================================
    # Navigate to "environments" folder of project-directory
cd YOUR_PATH_HERE/TextAsCorpusRep/environments
(For Christian:) cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/environments

    # Create virtual environment
python -m venv venvMTACR
    
    # Activate virtual environment
source venvMTACR/bin/activate

    # Install requirements
pip install -r ./../requirements.txt
"""

""" Usage: ====================================================================
    # Navigate to "source" folder of project-directory
cd YOUR_PATH_HERE/TextAsCorpusRep/source
(For Christian:) 
cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/source

    # Activate virtual environment
source ./../environments/venvMTACR/bin/activate

    # Run script with arguments (shown below for each step with examples)
    # --configPath is by default './../configs/general/paths.ini'
python main.py --languages mfe   # This does not anything but check that there is no crash
"""

""" 
# ============================================
# ===== Steps of this Project's Workflow =====
# ============================================

# ============================================
# Clone Project GitHub Repository
# INPUT: Project_Directory
# OUTPUT: Local copy of project code & data
# DESCRIPTION: 


# ============================================
# Prepare Configuration Files
# INPUT: Manual parameters according to experiment
# OUTPUT: Configuration files
# DESCRIPTION: 



    # ============================================
    # Get and Transform Datasets
    # INPUT: Configuration file + dataset information
    #   1. paths.ini
    #   2. datasets.json
    # OUTPUT: Raw (language/text) data
    # DESCRIPTION: 
# For a language
python main.py --getDatasets --languages mfe --debug
# For multiple languages
python main.py --getDatasets --languages mfe kmr vie deu eng zho ukr --debug
# For a specific dataset
python main.py --getDatasets --debug --specificDataset 2001HaigKurdishNewspaper
python main.py --getDatasets --debug --specificDataset 2012MorisienGramer
python main.py --getDatasets --debug --specificDataset 2013EsmailiPewan
python main.py --getDatasets --debug --specificDataset 2016ElliottMulti30k
python main.py --getDatasets --debug --specificDataset #2016MatrasKurdishDialectDatabase
python main.py --getDatasets --debug --specificDataset 2016UniMorphNorthernKurdish
python main.py --getDatasets --debug --specificDataset 2017LuongNMT
python main.py --getDatasets --debug --specificDataset 2018CraveApertiumNorthernKurdish
python main.py --getDatasets --debug --specificDataset #2018GraveFasttextWordVectors
python main.py --getDatasets --debug --specificDataset #2020AhmadiKurdishTokenization
python main.py --getDatasets --debug --specificDataset 2020FatihkurtKurdishTwitter
python main.py --getDatasets --debug --specificDataset #2020LeichtfußFreeDict
python main.py --getDatasets --debug --specificDataset 2021BfsujasonMAC
python main.py --getDatasets --debug --specificDataset 2021DoanPhoMT
python main.py --getDatasets --debug --specificDataset 2022AhmadiInterdialect
python main.py --getDatasets --debug --specificDataset 2022DabreMorisienMT
python main.py --getDatasets --debug --specificDataset 2022NgoSynthetic
python main.py --getDatasets --debug --specificDataset 2023AhmadiSouthernCorpus
python main.py --getDatasets --debug --specificDataset 2023NLLBSeed
python main.py --getDatasets --debug --specificDataset 2023SaichyshynaMulti30k
    
    
    
    # ============================================
    # Get and Transform Webdata
    # INPUT: Configuration file + URLs
    # OUTPUT: Raw (language/text) data
    # DESCRIPTION: 
    #   1. paths.ini
    #   2. webdata.json
# For a language
python main.py --getWebdata --languages mfe --debug
# For multiple languages
python main.py --getWebdata --languages mfe kmr vie deu eng zho ukr --debug
# For a specific URL
python main.py --getWebdata --debug --specificURL #TODO: How to parse URLs without issues?
python main.py --getWebdata --debug --specificURL #TODO: Parsing&Storing? 2021MorisienDictionaryEnglish
python main.py --getWebdata --debug --specificURL #TODO: Parsing&Storing? 2021MorisienEducationalBooksPupil
python main.py --getWebdata --debug --specificURL #TODO: Parsing&Storing? #2021MorisienEducationalBooksTeacher
python main.py --getWebdata --debug --specificURL #TODO: Parsing&Storing? 2023DevVirahsawmyBoukieBananePDF
python main.py --getWebdata --debug --specificURL #TODO: Parsing&Storing? 2023DevVirahsawmyBoukieBananeWeb


# ============================================
# Cleaning of Text Data (Datasets)
# INPUT: Configuration file + Raw (language/text) data
# OUTPUT: Clean data (Each line 1 sentence or word)
# DESCRIPTION: 
# For a language
python main.py --cleaningOfTextData --languages mfe --debug
# For multiple languages
python main.py --cleaningOfTextData --languages mfe kmr vie deu eng zho ukr --debug
# For a specific dataset
python main.py --cleaningOfTextData --debug --specificDataset 2001HaigKurdishNewspaper
python main.py --cleaningOfTextData --debug --specificDataset 2012MorisienGramer
python main.py --cleaningOfTextData --debug --specificDataset 2013EsmailiPewan
python main.py --cleaningOfTextData --debug --specificDataset 2016ElliottMulti30k
python main.py --cleaningOfTextData --debug --specificDataset #2016MatrasKurdishDialectDatabase # Entries marked with # are still work in progress
python main.py --cleaningOfTextData --debug --specificDataset 2016UniMorphNorthernKurdish
python main.py --cleaningOfTextData --debug --specificDataset 2017LuongNMT
python main.py --cleaningOfTextData --debug --specificDataset 2018CraveApertiumNorthernKurdish
python main.py --cleaningOfTextData --debug --specificDataset #2018GraveFasttextWordVectors
python main.py --cleaningOfTextData --debug --specificDataset #2020AhmadiKurdishTokenization
python main.py --cleaningOfTextData --debug --specificDataset 2020FatihkurtKurdishTwitter
python main.py --cleaningOfTextData --debug --specificDataset #2020LeichtfußFreeDict
python main.py --cleaningOfTextData --debug --specificDataset 2021BfsujasonMAC
python main.py --cleaningOfTextData --debug --specificDataset 2021DoanPhoMT
python main.py --cleaningOfTextData --debug --specificDataset 2022AhmadiInterdialect
python main.py --cleaningOfTextData --debug --specificDataset 2022DabreMorisienMT
python main.py --cleaningOfTextData --debug --specificDataset 2022NgoSynthetic
python main.py --cleaningOfTextData --debug --specificDataset 2023AhmadiSouthernCorpus
python main.py --cleaningOfTextData --debug --specificDataset 2023NLLBSeed
python main.py --cleaningOfTextData --debug --specificDataset 2023SaichyshynaMulti30k

# The cleaning process includes "transforming", "sorting", and "cleaning" 
#   each of these steps can be deactivated, to then only execute the remaining ones.
python main.py --cleaningOfTextData --cleaningNoTransform --languages mfe --debug
python main.py --cleaningOfTextData --cleaningNoSort --languages mfe --debug
python main.py --cleaningOfTextData --cleaningNoClean --languages mfe --debug
# Only the final cleaning-step of the cleaning-process for all languages
python main.py --cleaningOfTextData --cleaningNoTransform --cleaningNoSort --languages mfe kmr vie deu eng zho ukr --debug


# ============================================
# Cleaning of Text Data (Webdata)
# INPUT: Configuration file + Raw (language/text) data
# OUTPUT: Clean data (Each line 1 sentence or word)
# DESCRIPTION: 
# For a language
python main.py --cleaningOfWebData --languages mfe --debug
# For multiple languages
python main.py --cleaningOfWebData --languages mfe kmr vie deu eng zho ukr --debug
# For a specific URL
python main.py --cleaningOfWebData --debug --specificURL #TODO: How to parse URLs without issues?
python main.py --cleaningOfWebData --debug --specificURL #TODO: Parsing&Storing? 2021MorisienDictionaryEnglish
python main.py --cleaningOfWebData --debug --specificURL #TODO: Parsing&Storing? 2021MorisienEducationalBooksPupil
python main.py --cleaningOfWebData --debug --specificURL #TODO: Parsing&Storing? #2021MorisienEducationalBooksTeacher
python main.py --cleaningOfWebData --debug --specificURL #TODO: Parsing&Storing? 2023DevVirahsawmyBoukieBananePDF
python main.py --cleaningOfWebData --debug --specificURL #TODO: Parsing&Storing? 2023DevVirahsawmyBoukieBananeWeb


# ============================================
# Language Identification
# INPUT: Configuration file + Clean data + Confidence thresholds
#   1. experiment_mtacr_a.ini (with Confidence thresholds)
# OUTPUT: Language data (Each line with identified language & confidence)
# DESCRIPTION: 
python main.py --languageIdentification --configPath ./../configs/experiment/mtacr_a.ini --languages mfe --debug


    # ============================================
    # Author Review by Rarity Classes

    # ============================================
    # Native Speaker Review by Rarity Classes

# ============================================
# Native Speaker Monolingual Annotation
# INPUT: Subset of language data + Potato setup
# OUTPUT: Annotated (language/text) data
# DESCRIPTION: 


# ============================================
# Post-Process and Review Annotated Data
# INPUT: Annotated (language/text) data
# OUTPUT: Gold language data (monolingual)
# DESCRIPTION: 


# ============================================
# Native Speaker Linguistic Experts Monolingual Annotation
# INPUT: Annotated (language/text) data
# OUTPUT: Platinum language data (monolingual)
# DESCRIPTION: 


    # ============================================
    # Automatic Machine Trandslation
    # INPUT: Gold language data
    # OUTPUT: Bronze aligned data (bi-text)
    # DESCRIPTION: 

    # ============================================
    # Extract from Clean Data (Available Datasets & Crawled Webdata)
    # INPUT: Collected Datasets + Crawled Data
    # OUTPUT: Silver aligned data (bi-text) + Bronze-Quality Language Data (Monolingual)
    # DESCRIPTION: 
    python main.py --extractCleanData --debug

    # ============================================
    # Expert Translators Translation
    # INPUT: Gold language data
    # OUTPUT: Gold aligned data (bi-text)
    # DESCRIPTION: 

        # ============================================
        # Train Monolingual Language Model

            # ============================================
            # Automatic Evaluation via Metrics

            # ============================================
            # Native Speakers Evaluate Model

# ============================================
# Bilingual Native Speaker Annotation
# INPUT: Gold aligned data (bi-text)
# OUTPUT: Platinum aligned data (bi-text)
# DESCRIPTION: 


    # ============================================
    # Bilingual Native Speaker Annotation (Repeated)
    # INPUT: Gold OR Platinum aligned data (bi-text)
    # OUTPUT: Additional Platinum OR Higher-confidence Platinum aligned data (bi-text)
    # DESCRIPTION: 


# ============================================
# Train Multilingual Language Model
# INPUT: Platinum aligned data between various languages
# OUTPUT: Multilingual language model
# DESCRIPTION: 


# ============================================
# Train Multilingual Language Model
# INPUT: Platinum aligned data between various languages
# OUTPUT: Multilingual language model
# DESCRIPTION: 



# ============================================
# Analyze Text Data
# INPUT: Text in various level of quality
# OUTPUT: Tables & Plots
# DESCRIPTION: To better understand the data and how it changes in processing
# For a language
python main.py --analyzeText --languages mfe --debug
# For multiple languages
python main.py --analyzeText --languages mfe kmr vie deu eng zho ukr --debug


"""


""" TODO & INFO
Use of config files for parameter handling
# For paths to working directories see /configs/path/paths.json
# For dataset information see /configs/data/datasets.json
# For language information see /configs/data/languages.json
# For specific experiment parameters see /configs/experiment/name_of_experiment

# The use of a virtual environment is recommended.
# TODO: Automate the creation, activation and deactivation of virtual environments.
# TODO: Automate the installation of required packages.

# Activate virtual environment
# TODO: New naming-schema → source ./../../venvMTACR/bin/activate

# TODO: Add a tiny dataset and a tiny website URL as example data to fill the directories
#   Alternatively, include the creation of all required directories beforehand

# TODO: User-Guide to manual execution
"""


"""
Main script of project workflow
"""
def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    languages_selected = args.languages

    """
    Read general information from config file (such as path to download location)
    """
    # Create an instance of the ConfigParser class
    config = configparser.ConfigParser()  

    # Read the contents of the `config.ini` file
    config.read(f'{args.configPath}')

    # Access values from the configuration file
    # TODO: Only read required ones? That would create complexity for writing code, 
    #       but also reduce complexity for writing config-init-files for future experiments...
    # ==== Directory paths for this project / experiment
    config_data_datasets_path = config.get('General', 'config_data_datasets_path')
    config_data_webdata_path = config.get('General', 'config_data_webdata_path')
    config_data_languages = config.get('General', 'config_data_languages')

    data_raw_dataset_path = config.get('General', 'data_raw_dataset_path')
    data_raw_webdata_path = config.get('General', 'data_raw_webdata_path')
    data_temp_datasets_path = config.get('General', 'data_temp_datasets_path')
    data_temp_webdata_path = config.get('General', 'data_temp_webdata_path')
    data_transform_datasets_path = config.get('General', 'data_transform_datasets_path')
    data_transform_webdata_path = config.get('General', 'data_transform_webdata_path')
    data_sort_datasets_path = config.get('General', 'data_sort_datasets_path')
    data_sort_webdata_path = config.get('General', 'data_sort_webdata_path')
    data_clean_datasets_path = config.get('General', 'data_clean_datasets_path')
    data_clean_webdata_path = config.get('General', 'data_clean_webdata_path')
    
    data_monolingual_plain_path = config.get('General', 'data_monolingual_plain_path')
    data_monolingual_bronze_path = config.get('General', 'data_monolingual_bronze_path')
    data_monolingual_silver_path = config.get('General', 'data_monolingual_silver_path')
    data_monolingual_gold_path = config.get('General', 'data_monolingual_gold_path')
    data_monolingual_platinum_path = config.get('General', 'data_monolingual_platinum_path')
    
    data_multingual_plain_path = config.get('General', 'data_multingual_plain_path')
    data_multingual_bronze_path = config.get('General', 'data_multingual_bronze_path')
    data_multingual_silver_path = config.get('General', 'data_multingual_silver_path')
    data_multingual_gold_path = config.get('General', 'data_multingual_gold_path')
    data_multingual_platinum_path = config.get('General', 'data_multingual_platinum_path')
    
    data_model_download_path = config.get('General', 'data_model_download_path')
    data_model_monolingual_path = config.get('General', 'data_model_monolingual_path')
    data_model_multingual_path = config.get('General', 'data_model_multingual_path')

    logs_path = config.get('General', 'logs_path')

    # ==== Directory paths for this project / experiment
    # ++++ Here, the (default) paths from above can be changed as desired
    if args.languageIdentification == True:
        language_identification_confidence_thresholds = config.get('Language Identification', 'language_identification_confidence_thresholds')
        data_model_langid_path  = config.get('Language Identification', 'data_model_langid_path')

    info_datasets_ready = {}
    info_datasets_todo = {}
    info_webdata_ready = {}
    info_webdata_todo = {}

    #logging.debug(f'args.cleaningOfTextData: {args.cleaningOfTextData}')

    # ==== Select config file (paths) according to current operation argument
    # ++++ Datasets
    # ---- Read dataset information and filter according to parameter
    if args.getDatasets == True or args.cleaningOfTextData == True or args.extractCleanData == True:
        logging.debug(f'This is the path to the currently used dataset config file: {config_data_datasets_path}')

        with open(config_data_datasets_path, 'r') as json_file:
            info_datasets_all = json.load(json_file)
        
        # By default no specific dataset declared, keep selecting by "Language" and "Status"
        if args.specificDataset == "None":
            for key in info_datasets_all["Datasets"].keys():
                if info_datasets_all["Datasets"][key]["Language"] in languages_selected:
                    if info_datasets_all["Datasets"][key]["Status"] == "ready":
                        info_datasets_ready[key] = info_datasets_all["Datasets"][key]
                    elif info_datasets_all["Datasets"][key]["Status"] == "todo":
                        info_datasets_todo[key] = info_datasets_all["Datasets"][key]
                    else:
                        logging.info(f'Problematic Status for dataset key: {key}')
        # If specific dataset keys are provided, only select those from the datasets.json file
        else:
            logging.debug(f'Specified Datasets: {args.specificDataset}')
            for key in info_datasets_all["Datasets"].keys():
                if key in args.specificDataset:
                    info_datasets_ready[key] = info_datasets_all["Datasets"][key]

        for key in info_datasets_ready.keys():
            logging.info(f'Dataset ready: {key} for language: {info_datasets_ready[key]["Language"]}')
        for key in info_datasets_todo.keys():
            logging.info(f'Dataset todo: {key} for language: {info_datasets_todo[key]["Language"]}')

    # ++++ Webdata TODO: The following is a plain copy from the dataset-code above! Rework to properly handle webdata!
    elif args.getWebdata == True or args.cleaningOfWebData == True:
        logging.debug(f'This is the path to the currently used webdata config file: {config_data_webdata_path}')

        with open(config_data_webdata_path, 'r') as json_file:
            info_webdata_all = json.load(json_file)
        
        # By default no specific URL declared, keep selecting by "Language" and "Status"
        if args.specificURL == "None":
            for key in info_webdata_all["Webdata"].keys():
                if info_webdata_all["Webdata"][key]["Language"] in languages_selected:
                    if info_webdata_all["Webdata"][key]["Status"] == "ready":
                        info_webdata_ready[key] = info_webdata_all["Webdata"][key]
                    elif info_webdata_all["Webdata"][key]["Status"] == "todo":
                        info_webdata_todo[key] = info_webdata_all["Webdata"][key]
                    else:
                        logging.info(f'Problematic Status for URL key: {key}')
        # If specific URL keys are provided, only select those from the webdata.json file
        else:
            logging.debug(f'Specified Webdata: {args.specificURL}')
            for key in info_webdata_all["Webdata"].keys():
                if key in args.specificURL:
                    info_webdata_ready[key] = info_webdata_all["Webdata"][key]

        for key in info_webdata_ready.keys():
            logging.info(f'URL ready: {key} for language: {info_webdata_ready[key]["Language"]}')
        for key in info_webdata_todo.keys():
            logging.info(f'URL todo: {key} for language: {info_webdata_todo[key]["Language"]}')


    """
    Separate functions for each step of the workflow
    """
    def get_datasets():
        current_processing_step = "Get and Transform Datasets"
        logging.info(f'==== {current_processing_step} ====')
        down_ds.main(languages_selected,    # Languages selected via input arguments
                     info_datasets_ready,   # Only select datasets marked "ready"
                     data_raw_dataset_path, # Location to store downloaded data
                     args.specificDataset)  # Specific datasets (Default = None)


    def get_webdata():
        current_processing_step = "Get and Transform Webdata"
        logging.info(f'==== {current_processing_step} ====')
        down_wd.main() #TODO: Integrate Ramans Selenium Solution


    def cleaning_of_text_data():
        current_processing_step = "Cleaning of Text Data (Datasets)"
        logging.info(f'==== {current_processing_step} ====')
        clean_ds.main(info_datasets_ready,          # Only select datasets marked "ready"
                      data_raw_dataset_path,        # Location of raw data to clean
                      data_transform_datasets_path, # (Temp) Location for transformed data
                      data_sort_datasets_path,      # (Temp) Location for sorted data
                      data_clean_datasets_path,     # Location for cleaned data          
                      args.cleaningNoTransform,       # Flag if transforming step should be done (default=True)
                      args.cleaningNoSort,            # Flag if sorting step should be done (default=True)
                      args.cleaningNoClean)           # Flag if cleaning step should be done (default=True)


    def cleaning_of_web_data():
        current_processing_step = "Cleaning of Text Data (Webdata)"
        logging.info(f'==== {current_processing_step} ====')
        clean_wd.main #TODO: Implement properly (Ideally first finish get_webdata())


    def language_identification():
        current_processing_step = "Language Identification"
        logging.info(f'==== {current_processing_step} ====')
        lid_wd.main(info_datasets_ready,          # Only select datasets marked "ready"
                    data_sort_webdata_path,       # Location of sorted data (from webdata)
                    data_clean_webdata_path,      # Location of cleaned data (from webdata)
                    #data_clean_datasets_path,     # Location of cleaned data (from datasets)
                    #data_monolingual_plain_path,  # Location for identified monolingual data
                    data_model_download_path,     # Base-Location to cache models
                    data_model_langid_path,       # Location of current language identification model
                    language_identification_confidence_thresholds) # List of confidence thresholds


    def extract_clean_data():
        current_processing_step = "Extract from Clean Data"
        logging.info(f'==== {current_processing_step} ====')
        extract_ds.main(info_datasets_ready,          # Only select datasets marked "ready"
                        data_clean_datasets_path,     # Location of cleaned data (datasets)
                        data_clean_webdata_path,      # Location of cleaned data (webdata)
                        data_monolingual_plain_path,  # Location for (mono) clean/plain language data
                        data_multingual_plain_path)   # Location for (multi) clean/plain language data


    def author_review_by_rarity_classes():
        current_processing_step = "Author Review by Rarity Classes"
        logging.info(f'==== {current_processing_step} ====')
        pass


    def native_speaker_review_by_rarity_classes():
        current_processing_step = "Native Speaker Review by Rarity Classes"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def native_speaker_monolingual_annotation():
        current_processing_step = "Native Speaker Monolingual Annotation"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def post_process_and_review_annotated_data():
        current_processing_step = "Post-Process and Review Annotated Data"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def native_speaker_linguistic_experts_monolingual_annotation():
        current_processing_step = "Native Speaker Linguistic Experts Monolingual Annotation"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def automatic_machine_translation():
        current_processing_step = "Automatic Machine Trandslation"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def expert_translators_translation():
        current_processing_step = "Expert Translators Translation"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def bilingual_native_speaker_annotation():
        current_processing_step = "Bilingual Native Speaker Annotation"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def train_monolingual_language_model():
        current_processing_step = "Train Monolingual Language Model"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def train_multilingual_language_model():
        current_processing_step = "Train Multilingual Language Model"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def analyze_text():
        current_processing_step = "Analyze Text Data"
        logging.info(f'==== {current_processing_step} ====')
        list_of_data_paths_to_analyze = [
             # Datasets
            data_raw_dataset_path,           # Location to store downloaded data
            data_transform_datasets_path,    # (Temp) Location for transformed data
            data_sort_datasets_path,         # (Temp) Location for sorted data
            data_clean_datasets_path,        # Location for cleaned data  
            # Webdata
            data_raw_webdata_path,           #
            data_transform_webdata_path,     # 
            data_sort_webdata_path,          # 
            data_clean_webdata_path,         # Location of cleaned data (webdata)
            # Monolingual
            data_monolingual_plain_path,     # Location for (mono) clean language data
            data_monolingual_bronze_path,    #
            data_monolingual_silver_path,    # Location for (mono) clean language data
            data_monolingual_gold_path,      #
            data_monolingual_platinum_path,  #
            # Multilingual
            data_multingual_plain_path,     # 
            data_multingual_bronze_path,     # 
            data_multingual_silver_path,     # Location for (multi) clean language data
            data_multingual_gold_path,       #
            data_multingual_platinum_path    #
        ]
        anal_text.main(languages_selected,              # Languages selected via input arguments
                       #info_datasets_ready,            # Only select datasets marked "ready"
                       list_of_data_paths_to_analyze,   #
                       logs_path                        # Location for the analyzis logs
        )
        


    """
    Script execution based on input arguments
    """
    def mode_script():
        # Download public datasets
        if args.getDatasets:
            get_datasets()

        # Download webdata
        if args.getWebdata:
            get_webdata()

        # Clean collected text data (Datasets)
        if args.cleaningOfTextData:
            cleaning_of_text_data()

        # Clean collected text data (Webdata)
        if args.cleaningOfWebData:
            cleaning_of_web_data()

        # Identify language of clean text data
        if args.languageIdentification:
            language_identification()

        # Extract cleaned text data for each language (monolinual & multilingual)
        if args.extractCleanData:
            extract_clean_data()

        # 
        if args.authorReviewByRarityClasses:
            pass

        # 
        if args.nativeSpeakerReviewByRarityClasses:
            pass

        # 
        if args.nativeSpeakerMonolingualAnnotation:
            pass

        # 
        if args.postProcessAndReviewAnnotatedData:
            pass

        # 
        if args.nativeSpeakerLinguisticExpertsMonolingualAnnotation:
            pass

        # 
        if args.automaticMachineTranslation:
            pass

        # 
        if args.expertTranslatorsTranslation:
            pass

        # 
        if args.bilingualNativeSpeakerAnnotation:
            pass

        # 
        if args.trainMonolingualLanguageModel:
            pass

        # 
        if args.trainMultilingualLanguageModel:
            pass

        # 
        if args.analyzeText:
            pass



    mode_script()
    logging.info("Reached end of Script.")


# Standard boilerplate to call the main() function to begin the program.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        #prog='PROG',
        #description=__doc__,
        description=textwrap.dedent('''\
            Description of Script/Module
            ---------------------------------------------
            For more information check out the github repository:
            https://github.com/Low-ResourceDialectology/TextAsCorpusRep
            '''),
        epilog = "As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars = '@' )
        # Specify your real parameters here:
    parser.add_argument("--debug",action="store_true", help="printing for easy debugging.")
    parser.add_argument("--verbose",action="store_true", help="increase output verbosity.")
    parser.add_argument('--configPath', type=str, default='./../configs/general/paths.ini', help='path to config file.')
    parser.add_argument('--languages', type=str, nargs='+', default='None', help='list of language ids.')
    parser.add_argument('--specificDataset', type=str , default='None', help='single dataset-key for easy testing.')
    parser.add_argument('--specificURL', type=str , default='None', help='single website URL for easy testing.')
    
    parser.add_argument('--getDatasets', action="store_true", help='')
    parser.add_argument('--cleaningOfTextData', action="store_true", help='indicate to start the cleaning process.')
    
    parser.add_argument('--getWebdata', action="store_true", help='')
    parser.add_argument('--cleaningOfWebData', action="store_true", help='indicate to start the cleaning process.')
    parser.add_argument('--languageIdentification', action="store_true", help='')

    parser.add_argument('--cleaningNoTransform', action="store_false", help='cleaning process but without the transforming step.')
    parser.add_argument('--cleaningNoSort', action="store_false", help='cleaning process but without the sorting step.')
    parser.add_argument('--cleaningNoClean', action="store_false", help='cleaning process but without the cleaning step.')
    
    parser.add_argument('--extractCleanData', action="store_true", help='')
    parser.add_argument('--authorReviewByRarityClasses', action="store_true", help='')
    parser.add_argument('--nativeSpeakerReviewByRarityClasses', action="store_true", help='')
    parser.add_argument('--nativeSpeakerMonolingualAnnotation', action="store_true", help='')
    parser.add_argument('--postProcessAndReviewAnnotatedData', action="store_true", help='')
    parser.add_argument('--nativeSpeakerLinguisticExpertsMonolingualAnnotation', action="store_true", help='')

    parser.add_argument('--automaticMachineTranslation', action="store_true", help='')
    parser.add_argument('--expertTranslatorsTranslation', action="store_true", help='')
    parser.add_argument('--bilingualNativeSpeakerAnnotation', action="store_true", help='')
    parser.add_argument('--trainMonolingualLanguageModel', action="store_true", help='')
    parser.add_argument('--trainMultilingualLanguageModel', action="store_true", help='')

    parser.add_argument('--analyzeText', action="store_true", help='')
    # The 'action="store_true"' is used to store the default value "False" and only contain "True" if the flag has been set.
    # Example: we define --dwarf, action='store_true' and --fortress, action='store_false'
    #          we call the script with --dwarf --fortress → dwarf=True and fortress=False
    #          we call the script with --dwarf            → dwarf=True and fortress=True
    #          we call the script with         --fortress → dwarf=False and fortress=False
    #          we call the script with                    → dwarf=False and fortress=True

    args = parser.parse_args()
    
    #print("Debug: Argument parsing done")

    # Setup logging
    if args.debug:
        loglevel = logging.DEBUG
    elif args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.ERROR
    
    main(args, loglevel)