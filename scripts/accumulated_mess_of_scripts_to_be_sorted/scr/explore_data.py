# Moved to datasets_04_analyze.py

# -*- coding: utf-8 -*-
# Python Script for exploring collected text data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

import os
import json
import shutil

# Explore Text Data #
#####################

"""
Main Script
"""
def main():
    print("This is the explore_data script.")


    # Path to directory containing preprocessed data and output for explored data 
    #datasets_path = "./../data/data_datasets/"
    preprocessed_path = './../data/data_preprocessed/'
    explored_path = "./../data/data_explored/"

    # Dictionary holding the dataset entries to later be saved as json file
    dataset_json = {}
    dataset_counter = 0

    # Iterate over files in that directory
    for filename in os.listdir(preprocessed_path):
        filepath = os.path.join(preprocessed_path, filename)
        # Checking if it is a file
        if os.path.isfile(filepath):
            current_dataset = {
                "Name": "",
                "Source": "",
                "Target": "None",
                "Size": ""
                }

            #print(filepath) # Debugging

            # Split and get the name of the dataset from the name of the text file
            split_name = filepath.split("-")

            # Get the start of the file path
            #current_dataset["Name"] = split_name[0] # = "./../data/data_preprocessed/2021DoanPhoMT"

            # Take the last split to get the dataset name 
            current_dataset["Name"] = split_name[0].split("/")[4]
            
            # Split and get the end of the name of the text file
            #dataset_language = split_name[1] # = "kur.txt" or "eng_vie.txt" 
            
            # Split and get the language(s) identifier from the name of the text file
            dataset_language = split_name[1].split(".")[0]
            
            # If the length is 3, then this dataset is monolingual and there is only one language
            if len(dataset_language) == 3:
                #print("Length is 3 for: "+str(dataset_language)) # Debugging

                current_dataset["Source"] = dataset_language

            # If the length is not 3, then it is a multilingual dataset with a source- and a target-language
            else:
                #print("Length is not 3 for: "+str(dataset_language)) # Debugging

                dataset_languages = dataset_language.split("_")
                current_dataset["Source"] = dataset_languages[0]
                current_dataset["Target"] = dataset_languages[1]

            # Read the dataset textfile and count the number of lines
            with open(filepath, 'r') as fp:
                num_lines = sum(1 for line in fp)
                #print('Total lines:', num_lines) # Debugging
                current_dataset["Size"] = num_lines

            # Add the current dataset with the counter as key
            dataset_json[dataset_counter] = current_dataset

            # Serializing dictionary object into json 
            json_object = json.dumps(dataset_json, indent = 4)  

            # Increase the dataset_counter for the next file
            dataset_counter = dataset_counter + 1

    # TODO: Create directory prior to execution in order to create the json-file
    # Writing to sample.json
    with open(explored_path+'datasets_basic.json', "w") as outfile:
        outfile.write(json_object)



    # Alternative structure for forced layout #
    ###########################################
    """"
    # Dictionary holding the dataset entries to later be saved as json file
    dataset_json = {
        "nodes": 
        [
            {
                "id": "Chinese",
                "group": "1"
            },
            {
                "id": "English",
                "group": "2"
            },
            {
                "id": "French",
                "group": "3"
            },
            {
                "id": "German",
                "group": "4"
            },
            {
                "id": "Kobani",
                "group": "5"
            },
            {
                "id": "Kurmanji",
                "group": "6"
            },
            {
                "id": "Morisien",
                "group": "7"
            },
            {
                "id": "Russian",
                "group": "8"
            },
            {
                "id": "Ukrainian",
                "group": "9"
            },
            {
                "id": "Vietnamese",
                "group": "10"
            }
        ],
        "links":
        [

        ]
    }
    dataset_counter = 0

    # Iterate over files in that directory
    for filename in os.listdir(preprocessed_path):
        filepath = os.path.join(preprocessed_path, filename)
        # Checking if it is a file
        if os.path.isfile(filepath):
            current_dataset_node = {
                "id": "",
                "group": ""
                }
            current_dataset_link = {
                "source": "",
                "target": "",
                "value":""
                }
            current_dataset_link_two = {
                "source": "",
                "target": "",
                "value":""
                }

            #print(filepath) # Debugging

            # Split and get the name of the dataset from the name of the text file
            split_name = filepath.split("-")
            current_dataset_node["id"] = split_name[0]
            
            # Split and get the end of the name of the text file
            #dataset_language = split_name[1] # = "kur.txt" or "eng_vie.txt" 
            
            # Split and get the language(s) identifier from the name of the text file
            dataset_language = split_name[1].split(".")[0]
            
             # Read the dataset textfile and count the number of lines
            with open(filepath, 'r') as fp:
                num_lines = sum(1 for line in fp)
                #print('Total lines:', num_lines) # Debugging

            # If the length is 3, then this dataset is monolingual and there is only one language
            if len(dataset_language) == 3:
                #print("Length is 3 for: "+str(dataset_language)) # Debugging

                current_dataset_link["source"] = split_name[0]
                current_dataset_link["target"] = dataset_language
                current_dataset_link["value"] = num_lines

            # If the length is not 3, then it is a multilingual dataset with a source- and a target-language
            else:
                #print("Length is not 3 for: "+str(dataset_language)) # Debugging

                dataset_languages = dataset_language.split("_")

                current_dataset_link["source"] = split_name[0]
                current_dataset_link["target"] = dataset_languages[0]
                current_dataset_link["value"] = num_lines

                current_dataset_link_two["source"] = split_name[0]
                current_dataset_link_two["target"] = dataset_languages[1]
                current_dataset_link_two["value"] = num_lines

            dataset_json["nodes"]

            # Serializing dictionary object into json 
            json_object = json.dumps(dataset_json, indent = 4)  


    # Writing to sample.json
    with open(explored_path+'datasets_forced_layout.json', "w") as outfile:
        outfile.write(json_object)

    """


if __name__ == "__main__":
    main()
