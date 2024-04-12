import re
import json
import io
import csv

flickr_data = {}
aligned_file = './../data/flickr30k-aligned'
info_file = './../data/flickr30k/filenames/flickr30k_1_500'
output_file = './../data/flickr30k-adjusted'

def read_aligned_json(file_path):
    with open(f'{file_path}.json', 'r') as json_file:
        aligned_data = json.load(json_file)
        return aligned_data

flickr_data = read_aligned_json(aligned_file)


def read_flickr_potato_info(input_file):
    info_data = {}
    
    with open(f'{input_file}.json', 'r') as input_file:
        info_text = input_file.readlines()
    
    for line in info_text:
        id = line.split('{"id":"')[1].split('","text":"<img')[0]
        img_file = line.split('/flickr30k_1_500\/')[1].split('.jpg')[0]+'.jpg'
        info_data[id] = img_file
    return info_data

img_file_info = read_flickr_potato_info(info_file)

# Output dictionary for mapped data
adjusted_flickr_data = {}

# Map all potato-task-ids to their corresponding image filenames
for key in flickr_data.keys():
    if key in img_file_info.keys():
        filename_key = img_file_info[key]
        adjusted_flickr_data[filename_key] = flickr_data[key]
    else:
        print(f'Unexpected missing of key in info-file for: {key}')


# Serializing json and write to file
json_object = json.dumps(adjusted_flickr_data, indent=4, ensure_ascii=False)
with open(f'{output_file}.json', "w", encoding="utf-8") as outfile:
    outfile.write(json_object)