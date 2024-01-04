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
python main.py --languages mor   # This does not anything but check that there is no crash
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
    # INPUT: Configuration files + dataset information
    # OUTPUT: Raw (language/text) data
    # DESCRIPTION: 
python main.py --getAndTransformDatasets --languages mor --debug
python main.py --getAndTransformDatasets --languages mor kmr vie deu eng zho ukr --debug
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2001HaigKurdishNewspaper
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset 2012MorisienGramer
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2013EsmailiPewan
python main.py --getAndTransformDatasets --languages deu --debug --specificDataset 2016ElliottMulti30k
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset #2016MatrasKurdishDialectDatabase
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2016UniMorphNorthernKurdish
python main.py --getAndTransformDatasets --languages vie --debug --specificDataset 2017LuongNMT
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2018CraveApertiumNorthernKurdish
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset #2018GraveFasttextWordVectors
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset #2020AhmadiKurdishTokenization
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2020FatihkurtKurdishTwitter
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset #2020LeichtfußFreeDict
python main.py --getAndTransformDatasets --languages zho --debug --specificDataset 2021BfsujasonMAC
python main.py --getAndTransformDatasets --languages vie --debug --specificDataset 2021DoanPhoMT
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset 2021MorisienDictionaryEnglish
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset 2021MorisienEducationalBooksPupil
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset #2021MorisienEducationalBooksTeacher
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2022AhmadiInterdialect
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset 2022DabreMorisienMT
python main.py --getAndTransformDatasets --languages vie --debug --specificDataset 2022NgoSynthetic
python main.py --getAndTransformDatasets --languages kmr --debug --specificDataset 2023AhmadiSouthernCorpus
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset 2023DevVirahsawmyBoukieBananePDF
python main.py --getAndTransformDatasets --languages mor --debug --specificDataset 2023DevVirahsawmyBoukieBananeWeb
python main.py --getAndTransformDatasets --languages eng --debug --specificDataset 2023NLLBSeed
python main.py --getAndTransformDatasets --languages ukr --debug --specificDataset 2023SaichyshynaMulti30k
    
    
    
    # ============================================
    # Get and Transform Webdata
    # INPUT: Configuration files + URLs
    # OUTPUT: Raw (language/text) data
    # DESCRIPTION: 


# ============================================
# Cleaning of Text Data
# INPUT: Raw (language/text) data
# OUTPUT: Clean data (Each line 1 sentence or word)
# DESCRIPTION: 
python main.py --cleaningOfTextData --languages mor --debug
python main.py --cleaningOfTextData --languages mor kmr vie deu eng zho ukr --debug
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2001HaigKurdishNewspaper
python main.py --cleaningOfTextData --languages mor --debug --specificDataset 2012MorisienGramer
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2013EsmailiPewan
python main.py --cleaningOfTextData --languages deu --debug --specificDataset 2016ElliottMulti30k
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset #2016MatrasKurdishDialectDatabase
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2016UniMorphNorthernKurdish
python main.py --cleaningOfTextData --languages vie --debug --specificDataset 2017LuongNMT
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2018CraveApertiumNorthernKurdish
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset #2018GraveFasttextWordVectors
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset #2020AhmadiKurdishTokenization
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2020FatihkurtKurdishTwitter
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset #2020LeichtfußFreeDict
python main.py --cleaningOfTextData --languages zho --debug --specificDataset 2021BfsujasonMAC
python main.py --cleaningOfTextData --languages vie --debug --specificDataset 2021DoanPhoMT
python main.py --cleaningOfTextData --languages mor --debug --specificDataset 2021MorisienDictionaryEnglish
python main.py --cleaningOfTextData --languages mor --debug --specificDataset 2021MorisienEducationalBooksPupil
python main.py --cleaningOfTextData --languages mor --debug --specificDataset #2021MorisienEducationalBooksTeacher
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2022AhmadiInterdialect
python main.py --cleaningOfTextData --languages mor --debug --specificDataset 2022DabreMorisienMT
python main.py --cleaningOfTextData --languages vie --debug --specificDataset 2022NgoSynthetic
python main.py --cleaningOfTextData --languages kmr --debug --specificDataset 2023AhmadiSouthernCorpus
python main.py --cleaningOfTextData --languages mor --debug --specificDataset 2023DevVirahsawmyBoukieBananePDF
python main.py --cleaningOfTextData --languages mor --debug --specificDataset 2023DevVirahsawmyBoukieBananeWeb
python main.py --cleaningOfTextData --languages eng --debug --specificDataset 2023NLLBSeed
python main.py --cleaningOfTextData --languages ukr --debug --specificDataset 2023SaichyshynaMulti30k


# ============================================
# Language Identification
# INPUT: Clean data + Confidence thresholds
# OUTPUT: Language data (Each line with identified language & confidence)
# DESCRIPTION: 
python main.py --languageIdentification --languages mor --debug


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
    # OUTPUT: Silver aligned data (bi-text)
    # DESCRIPTION: 

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

    # Read the contents of the `config.ini` file:
    config.read(f'{args.configPath}')

    # Access values from the configuration file:
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
    data_monolingual_clean_path = config.get('General', 'data_monolingual_clean_path')
    data_monolingual_bronze_path = config.get('General', 'data_monolingual_bronze_path')
    data_monolingual_silver_path = config.get('General', 'data_monolingual_silver_path')
    data_monolingual_gold_path = config.get('General', 'data_monolingual_gold_path')
    data_monolingual_platinum_path = config.get('General', 'data_monolingual_platinum_path')
    data_multingual_silver_path = config.get('General', 'data_multingual_silver_path')
    data_multingual_gold_path = config.get('General', 'data_multingual_gold_path')
    data_multingual_platinum_path = config.get('General', 'data_multingual_platinum_path')
    data_model_download_path = config.get('General', 'data_model_download_path')
    data_model_monolingual_path = config.get('General', 'data_model_monolingual_path')
    data_model_multingual_path = config.get('General', 'data_model_multingual_path')
    language_identification_confidence_thresholds = config.get('General', 'language_identification_confidence_thresholds')


    # Read dataset information and filter according to parameter
    logging.debug(f'This is the path to the dataset config file: {config_data_datasets_path}')
    
    with open(config_data_datasets_path, 'r') as json_file:
        info_datasets_all = json.load(json_file)

    info_datasets_ready = {}
    info_datasets_todo = {}
    
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

    """
    Separate function for each step of the workflow
    """
    def get_and_transform_datasets():
        current_processing_step = "Get and Transform Datasets"
        logging.info(f'==== {current_processing_step} ====')
        down_ds.main(languages_selected,    # Languages selected via input arguments
                     info_datasets_ready,   # Only select datasets marked "ready"
                     data_raw_dataset_path) # Location to store downloaded data

    def get_and_transform_webdata():
        current_processing_step = "Get and Transform Webdata"
        logging.info(f'==== {current_processing_step} ====')
        pass

    def cleaning_of_text_data():
        current_processing_step = "Cleaning of Text Data"
        logging.info(f'==== {current_processing_step} ====')
        clean_ds.main(info_datasets_ready,          # Only select datasets marked "ready"
                      data_raw_dataset_path,        # Location of raw data to clean
                      data_transform_datasets_path, # (Temp) Location for transformed data
                      data_sort_datasets_path,      # (Temp) Location for sorted data
                      data_clean_datasets_path)     # Location for cleaned data          

    def language_identification():
        current_processing_step = "Language Identification"
        logging.info(f'==== {current_processing_step} ====')
        pass

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


    """
    Script execution based on input arguments
    """
    def mode_script():
        # Download public datasets
        if args.getAndTransformDatasets:
            get_and_transform_datasets()

        # Download webdata
        if args.getAndTransformWebdata:
            pass

        # Clean collected text data
        if args.cleaningOfTextData:
            cleaning_of_text_data()

        # Identify language of clean text data
        if args.languageIdentification:
            language_identification()

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
    parser.add_argument('--specificDataset', type=str , default='None', help='single dataset-key for easy testing.')
    parser.add_argument("--verbose",action="store_true", help="increase output verbosity.")
    parser.add_argument('--configPath', type=str, default='./../configs/general/paths.ini', help='path to config file.')
    parser.add_argument('--languages', type=str, nargs='+', default='mor', help='list of language ids.')
    parser.add_argument('--getAndTransformDatasets', action="store_true", help='')
    parser.add_argument('--getAndTransformWebdata', action="store_true", help='')
    parser.add_argument('--cleaningOfTextData', action="store_true", help='')
    parser.add_argument('--languageIdentification', action="store_true", help='')
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