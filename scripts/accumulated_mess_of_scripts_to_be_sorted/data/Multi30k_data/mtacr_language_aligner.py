from datetime import datetime
import json
import gzip
import re
import sys

flikr_data = {}
# Previously aligned data related to Flickr30k (Python Script: multi30k_language_aligner.py)
input_file = './data/Multi30k-Aligned/multi30k-aligned'
mtacr_input_file = './../data/Multi30k_data/data/Flickr30k-MTACR/flickr30k-adjusted'
output_file = './multi30k-mtacr'

current_datetime = str(datetime.now().strftime("%Y_%m_%d"))
log_file = f'./../../logs/multi30k-mtacr-{current_datetime}'
log_data = {}

"""
Helper function for reading file formats
"""
# Read from json file
def read_aligned_json(file_path):
    with open(f'{file_path}.json', 'r') as json_file:
        aligned_data = json.load(json_file)
        return aligned_data

# Count items in json file
def count_elements(dictionary):
    count = 0
    for value in dictionary.values():
        if isinstance(value, dict):
            count += count_elements(value)  # Recursively count elements in nested dictionary
        else:
            count += 1  # Increment count for non-dictionary elements
    return count


flikr_data = read_aligned_json(input_file)
input_elements = count_elements(flikr_data)
print("Total annotations of input (flickr) data:", input_elements)
log_data["Number of Input Entries"] = input_elements

missing_key = "Filenames part of MTACR-Data but missing in the aggregated Multi30k-Data"
log_data[missing_key] = {}

def read_flikr_mtacr(data, input_file):
    flickr_data = data
    mtacr_data = read_aligned_json(input_file)

    for key in mtacr_data.keys():
        if not key in flickr_data.keys():
            print(f'Unexpected image filename missing in keys for: {key}')
            log_data[missing_key][key] = "Missing"
        else:
            for language_key in mtacr_data[key].keys():
                for anno_key in mtacr_data[key][language_key].keys():
                    if language_key in flickr_data[key].keys():
                        flickr_data[key][language_key][anno_key] = mtacr_data[key][language_key][anno_key]
                    else:
                        flickr_data[key][language_key] = {}
                        flickr_data[key][language_key][anno_key] = mtacr_data[key][language_key][anno_key]

    return flickr_data

flikr_data = read_flikr_mtacr(flikr_data, mtacr_input_file)
input_elements = count_elements(flikr_data)
print("Total annotations of output (flickr+mtacr)  data:", input_elements)
log_data["Number of Output Entries"] = input_elements

"""
Unexpected image filename missing in keys for: 667626.jpg
Unexpected image filename missing in keys for: 16396205.jpg
Unexpected image filename missing in keys for: 21514026.jpg
Unexpected image filename missing in keys for: 15950702.jpg
Unexpected image filename missing in keys for: 16396183.jpg
Unexpected image filename missing in keys for: 16396193.jpg
"""

# Serializing json and write to file
json_object = json.dumps(flikr_data, indent=4, ensure_ascii=False)
with open(f'{output_file}_mtacr.json', "w", encoding="utf-8") as outfile:
    outfile.write(json_object)

json_object_log = json.dumps(log_data, indent=4, ensure_ascii=False)
with open(f'{log_file}.json', "w", encoding="utf-8") as outfile:
    outfile.write(json_object_log)
