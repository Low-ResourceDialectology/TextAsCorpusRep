# -*- coding: utf-8 -*-
# Python Script for preparing the work with text data from available datasets
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

"""
Python program to check if a path exists if path doesn’t exist we create a new path

"""

import json
import logging
import os

import utilities as util

#def main(languages, info_path, output_path):

"""
Create directories of the project.
"""
def create_dirs_for_lang(output_path):

    logging.info(f'  Creating new directories')
    logging.debug(f'output_path: {output_path}')

    # List of dirs to be created for each language
    list_of_dirs = ['00_prepare', '01_download', '02_transform', '03_analyze', '04_sort', '05_clean', '06_aggregate', '07_process', '08_evaluate']
    for dir in list_of_dirs:
    
        new_dir = output_path+dir
        #logging.debug(f'new_dir: {new_dir}')
    
        # Create directory if not existing
        util.create_directory(new_dir)

"""
Get information about datasets from provided json file.

Format of dataset_information.json
{
    "Datasets":
    {
        "2022DabreMorisienMT":
        {
            "language":"mor",
            "source":"huggingface",
            "id":"prajdabre/KreolMorisienMT",
            ...
        },
        "2022AhmadiInterdialect":
        {
            ...
        }
    }
}


"""
def read_dataset_information(info_path):

    # Empty dictionary to hold information
    dataset_info = {}

    # Read information from file
    with open(f'{info_path}dataset_information.json', 'r') as f:
        dataset_information = json.load(f)

    # For each dataset information's key, extract crucial information
    for dataset_key in dataset_information["Datasets"].keys():

            dataset_info[dataset_key] = {
                "language":dataset_information["Datasets"][dataset_key]["language"],
                "source":dataset_information["Datasets"][dataset_key]["source"],
                "id":dataset_information["Datasets"][dataset_key]["id"]
            }
    
    return dataset_info

"""
Get information about languages from provided json file.
"""
def read_language_information(info_path):
    language_info = {
        "mor":{
            "Name":"Morisien"
        },
        "vie":{
            "Name":"Vietnamese"
        },
        "kur":{
            "Name":"Northern Kurdich"
        },
        "Kob":{
            "Name":"Kobani"
        }
    }

    return language_info

    
    
"""
    create_dirs_for_lang(output_path)

    language_info = read_language_information(info_path)

    dataset_info = read_dataset_information(info_path)

    return language_info, dataset_info
"""

#if __name__ == "__main__":
#	main()
