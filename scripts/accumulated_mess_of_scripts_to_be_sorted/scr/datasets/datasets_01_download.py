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

"""

import logging
import os
import requests

from datasets import list_datasets
from datasets import load_dataset

import utilities as util

# → dataset = load_dataset('squad', split='train')

def main(languages, output_path, datasets):

    """

    """
    def download_from_github(dataset_ids, dataset_path, dataset_key):

        # Create directory if it does not already exist
        current_savepath = f'{dataset_path}{dataset_key}/'
        util.create_directory(current_savepath)
        
        for dataset_id in dataset_ids:

            # Name and extension of file to download
            current_filename = util.get_filename(dataset_id)
            current_extension = util.get_fileending(dataset_id).lower()

            if os.path.exists(f'{current_savepath}{current_filename}'):
                print(f"GitHub-File already exists at {current_savepath}{current_filename}. Skipping download.")
                continue

            write_mode = 'wb' if current_extension in ('.jpg', '.png', '.exe') else 'w'
            
            # Server response handling
            response = requests.get(dataset_id)
            if response.status_code == 200:

                # Write downloaded data to file (either binary content or text)
                with open(f'{current_savepath}{current_filename}', write_mode) as file:
                    file.write(response.content if write_mode == 'wb' else response.text)
                print(f"File downloaded successfully and saved at: {current_savepath}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")

                #with open(current_savepath, 'wb') as file:
                    #file.write(response.content)

            # Write downloaded text data to file
            #with open(f'{dataset_path}{dataset_key}/text-{current_filename}', 'w') as output_f:
            #	output_f.write(r.text)
            
            # Write downloaded text data to file
            #with open(f'{dataset_path}{dataset_key}/content-{current_filename}', 'wb') as output_f:
            #	output_f.write(r.content)


    """

    """
    def download_from_hugginface(dataset_id, dataset_path, dataset_key):
        
        if os.path.exists(f'{dataset_path}/{dataset_key}'):
            print(f"Huggingface-Dataset {dataset_path}/{dataset_key} already exists. Skipping download.")
        else:
            print(f"Downloading and caching dataset {dataset_path}/{dataset_key} ...")
            dataset = load_dataset(dataset_id, cache_dir=f'{dataset_path}/{dataset_key}')

            # Save the downloaded dataset to cache
            dataset.save_to_disk(f'{dataset_path}/{dataset_key}')
        #dataset = load_dataset('squad', split='train', cache_dir="PATH/TO/MY/CACHE/DIR")

    """

    """
    def download_from_website(dataset_id, dataset_path, dataset_key):
        pass
    # f'{dataset_path}/{dataset_key}'


    """
    Input:
    languages = ["mor", "kur", "vie"]
    output_path = "./../../data/datasets/"
    datasets =  { 
                    "2022DabreMorisienMT":
                    {
                        "language":"mor", 
                        "id":"prajdabre/KreolMorisienMT",
                        "source":"huggingface"
                    }
                }
    """
    def manage_downloading_process(languages, output_path, datasets):
        print(languages)
        for dataset_key in datasets.keys():
            
            # Only download datasets for the defined language
            if datasets[dataset_key]["language"] in languages:
            
                # Download dataset from Huggingface
                if datasets[dataset_key]["source"] == "huggingface":
                    download_from_hugginface(datasets[dataset_key]["id"], output_path, dataset_key)
                
                # Download dataset from GitHub
                if datasets[dataset_key]["source"] == "github":
                    download_from_github(datasets[dataset_key]["id"], output_path, dataset_key)
                
                # Download dataset from Websites
                if datasets[dataset_key]["source"] == "website":
                    download_from_website(datasets[dataset_key]["id"], output_path, dataset_key)
        
    manage_downloading_process(languages, output_path, datasets)


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
