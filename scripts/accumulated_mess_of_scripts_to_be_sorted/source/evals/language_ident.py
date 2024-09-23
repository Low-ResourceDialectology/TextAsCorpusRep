# -*- coding: utf-8 -*-
# Python Script for identifying the language of text data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import logging
import os
import sys

import fasttext
from huggingface_hub import hf_hub_download

# Enable importing the other scripts by adding their location to the python-path
sys.path.append(r"./../../")

import utils.utilities_general as util_ge # General Utilities
import utils.utilities_general as util_tp # Text Processing Utilities

""" Sources:
GlotLID: https://github.com/cisnlp/GlotLID
"""


""" INPUT parameter: 
    info_datasets_ready,          # Only select datasets marked "ready"
    data_raw_dataset_path,        # Location of raw data to clean
    data_transform_datasets_path, # (Temp) Location for transformed data
    data_sort_datasets_path,      # (Temp) Location for sorted data
    data_clean_datasets_path,     # Location for cleaned data
    execute_transforming,         # Flag if transforming step should be done (default=True)
    execute_sorting,              # Flag if sorting step should be done (default=True)
    execute_cleaning              # Flag if cleaning step should be done (default=True) 

    data_model_download_path,     # Base-Location to cache models
    data_model_langid_path,       # Location of current language identification model
    language_identification_confidence_thresholds) # List of confidence thresholds
"""
def main(input_path, output_path, current_dataset_key, data_model_download_glotlid_path):
    
    #input_path, 
    #output_path, 
    #current_dataset_key, 
    #language_identification_confidence_thresholds):
        
        #info_datasets_ready,          # Only select datasets marked "ready"
        #data_sort_webdata_path,       # Location of sorted data (from webdata)
        #data_clean_webdata_path,      # Location of cleaned data (from webdata)
        #data_clean_datasets_path,     # Location of cleaned data (from datasets)
        #data_monolingual_plain_path,  # Location for identified monolingual data
        #data_model_download_path,     # Base-Location to cache models
        #data_model_langid_path,       # Location of current language identification model
        #language_identification_confidence_thresholds): # List of confidence thresholds


    """
    This script uses the GlotLID implementation from HuggingFace, based on fasttext.
    For this, the model has to initially be downloaded.
    This model will be saved in a cache-directory for faster loading in future executions.
    """
    def get_model_GlotLID(repo_id_var="cis-lmu/glotlid", filename_var="model.bin", cache_dir_var="./../data/model/download/langid_glotLID/"):
        # ===========================================
        # Download Model
        # ===========================================
        ## cache_dir: path to the folder where the downloaded model will be stored/cached.
        model_path = hf_hub_download(repo_id=repo_id_var, filename=filename_var, cache_dir=cache_dir_var)

        # ===========================================
        # Load Model
        # ===========================================
        model_lid = fasttext.load_model(model_path)

        # ===========================================
        # Predict Language Label
        # ===========================================
        #model.predict("Hello, world!")

        return model_lid


    """
    Language Identification based on GlotLID
    INPUT:
    OUTPUT:
    """
    def identify_languages(input_path, output_path, model_path):

        model_cache_directory = model_path
        language_id_model = get_model_GlotLID(model_cache_directory)

        current_file_in = input_path
        text_lines_linebreak = util_ge.read_text_file(current_file_in)
        
        text_lines = []
        for line in text_lines_linebreak:
            text_lines.append(line.replace('\n', ''))

        text_lines_predictions = []
        for line in text_lines:
            prediction = language_id_model.predict(line)
            text_lines_predictions.append(prediction)
        
        text_lines_and_predictions = [] # List of lists, where each contained list holds 2 elements: sentence and predictions
        #text_lines_and_predictions = zip(text_lines[0:10], text_lines_predictions)
        for index in range(len(text_lines_predictions)):
            text_lines_and_predictions.append([text_lines[index], text_lines_predictions[index]])

        # NOTE: Currently the .info file is saved right next to the identified text data file
        output_file_path = util_ge.get_filename_without_extension(output_path)

        # Writing language identification predictions to "language_identifications".txt
        with open(f'{output_file_path}.info', "w") as outfile:
            for sentence_and_prediction in text_lines_and_predictions:
                outfile.write(str(sentence_and_prediction)+'\n')


    # ========================================================================= 
    # Execution
    #
    logging.debug(f'====== Identifying Languages of Webdata')
    logging.debug(f'++++++ inputPath: {input_path}')
    logging.debug(f'++++++ outputPath: {output_path}')
    logging.debug(f'++++++ current dataset: {current_dataset_key}')
    logging.debug(f'++++++ language model path: {data_model_download_glotlid_path}')
    
    # Create directories if not existing
    util_ge.create_directory(output_path)

    identify_languages(input_path, output_path, data_model_download_glotlid_path)


    # TODO
    #get_model_GlotLID(repo_id_var="cis-lmu/glotlid", filename_var="model.bin", cache_dir_var="./../data/model/download/langid_glotLID/")


if __name__ == "__main__":
    main()
