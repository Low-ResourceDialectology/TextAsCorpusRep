# -*- coding: utf-8 -*-
# Python Script for downloading text data from available datasets
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################
"""
Prior Step: Prepare Configuration Files
This Step: Get and Transform Datasets
Next Step: Cleaning of Text Data
"""

import logging
import os
import requests
import sys

from datasets import list_datasets
from datasets import load_dataset

# Enable importing the other scripts by adding their location to the python-path
sys.path.append(r"./../../")

import utils.utilities_general as util_ge

""" INPUT (examples):
    languages = ["mfe", "kmr", "vie"]
    output_path = "./../../data/datasets/"
    datasets =  { 
                    "2022DabreMorisienMT":
                    {
                        "language":"mfe", 
                        "id":"prajdabre/KreolMorisienMT",
                        "source":"huggingface"
                    }
                }
"""
def main(languages, datasets, output_path, specific_datasets):
# TODO: Move main to bottom of script.
    """
    Automated downloading of data from github repositories
    """
    def download_from_github(dataset_ids, dataset_path, dataset_key):

        # Create directory if it does not already exist
        current_savepath = f'{dataset_path}{dataset_key}/'
        util_ge.create_directory(current_savepath)
        
        for dataset_id in dataset_ids:

            # Name and extension of file to download
            current_filename = util_ge.get_filename_without_extension(dataset_id)
            #print(current_filename)
            current_extension = util_ge.get_fileextension(dataset_id).lower()
            #print(current_extension)

            if dataset_id == "https://raw.githubusercontent.com/unimorph/kmr/master/kmr":
                current_filename = "kmr"
                current_extension = 'txt'

            if os.path.exists(f'{current_savepath}{current_filename}'):
                logging.info(f"GitHub-File already exists at {current_savepath}{current_filename}. Skipping download.")
                continue

            write_mode = 'wb' if current_extension in ('gz','zip','jpg','png','exe','pdf') else 'w'
            
            # Server response handling
            response = requests.get(dataset_id)
            if response.status_code == 200:

                # Write downloaded data to file (either binary content or text)
                with open(f'{current_savepath}{current_filename}.{current_extension}', write_mode) as file:
                    file.write(response.content if write_mode == 'wb' else response.text)
                logging.info(f"File downloaded successfully and saved at: {current_savepath}")
            else:
                logging.info(f"Failed to download file. Status code: {response.status_code}")

                #with open(current_savepath, 'wb') as file:
                    #file.write(response.content)

            # Write downloaded text data to file
            #with open(f'{dataset_path}{dataset_key}/text-{current_filename}', 'w') as output_f:
            #	output_f.write(r.text)
            
            # Write downloaded text data to file
            #with open(f'{dataset_path}{dataset_key}/content-{current_filename}', 'wb') as output_f:
            #	output_f.write(r.content)


    """
    Automated downloading of data from huggingface
        - dataset_id = Combination of User_Name/Dataset_Name
            e.g. "prajdabre/KreolMorisienMT"
        - dataset_path = Local path to download to
            e.g. "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/raw/datasets/"
        - dataset_key = Identifier for local dataset location
            e.g. "2022DabreMorisienMT"
    """
    def download_from_hugginface(dataset_id, dataset_path, dataset_key):
        
        if os.path.exists(f'{dataset_path}{dataset_key}'):
            logging.info(f"Huggingface-Dataset {dataset_path}{dataset_key} already exists. Skipping download.")
        else:
            logging.info(f"Downloading and caching dataset {dataset_path}{dataset_key} ...")
            dataset = load_dataset(dataset_id, cache_dir=f'{dataset_path}{dataset_key}/cache')
            #dataset = load_dataset('squad', split='train', cache_dir="PATH/TO/MY/CACHE/DIR")

            # Save the downloaded dataset to cache
            dataset.save_to_disk(f'{dataset_path}{dataset_key}/local')
        
            # To later load from local location
            # from datasets import load_from_disk
            # my_current_dataset = load_from_disk(f'{dataset_path}{dataset_key}')

    """
    Automated downloading of data from websites
    """
    def download_from_website(dataset_id, dataset_path, dataset_key):
        pass
    # f'{dataset_path}/{dataset_key}'


    """
    Input:
    languages = ["mfe", "kmr", "vie"]
    output_path = "./../../data/datasets/"
    datasets =  { 
                    "2022DabreMorisienMT":
                    {
                        "language":"mfe", 
                        "id":"prajdabre/KreolMorisienMT",
                        "source":"huggingface"
                    }
                }
    """
    def manage_downloading_process(languages, output_path, datasets, specific_datasets):
        #logging.info(languages)
        for dataset_key in datasets.keys():
            
            # Only download datasets for the defined language OR when specific dataset(s) are given
            if datasets[dataset_key]["Language"] in languages or specific_datasets != 'None':
            
                # Download dataset from Huggingface
                if datasets[dataset_key]["Platform"] == "huggingface":
                    logging.info(f'====   Downloading from Huggingface: {dataset_key}')
                    download_from_hugginface(datasets[dataset_key]["Platform ID"], output_path, dataset_key)
                    
                # Download dataset from GitHub
                if datasets[dataset_key]["Platform"] == "github":
                    logging.info(f'====   Downloading from GitHub: {dataset_key}')
                    download_from_github(datasets[dataset_key]["Platform ID"], output_path, dataset_key)
                
                # Download dataset from Websites
                if datasets[dataset_key]["Platform"] == "website":
                    logging.info(f'====   Downloading from Website: {dataset_key}')
                    download_from_website(datasets[dataset_key]["Platform ID"], output_path, dataset_key)
                
                # Download dataset from Homepage or Requests
                if datasets[dataset_key]["Platform"] == "homepage":
                    logging.info(f'====   The dataset {dataset_key} needs to be requested from the creators.')
                    logging.info(f'++++     Access Information: {datasets[dataset_key]["Access"]}')
        
    manage_downloading_process(languages, output_path, datasets, specific_datasets)


    """
    Display number and names of datasets from hugginhface.
    """
    def show_huggingface_datasets():
        
        datasets_list = list_datasets()
        number_of_datasets = len(datasets_list)
        logging.info(f'Number of datasets: {number_of_datasets}')
        # → 86.987 datasets

        printable_list = ', '.join(dataset for dataset in datasets_list)
        logging.info(f'List of datasets: {printable_list}')
        # → Large output!

    #show_huggingface_datasets() 

if __name__ == "__main__":
    main()
