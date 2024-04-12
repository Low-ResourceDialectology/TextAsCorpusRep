import json
import gzip
import re
import sys
import os 

"""
!!! Might take a long time to finish 
    due to less optimal look-up for Ukrainian data 
    at the bottom of this script !!!
"""

flikr_data = {}
# input files are the previously collected flickr30k & multi30k files in /data/Multi30k_data/data/
output_file = './data/Multi30k-Aligned/multi30k-aligned'
output_dir = './data/Multi30k-Aligned'
# Check whether directory already exists
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
    print("Folder %s created!" % output_dir)
else:
    print("Folder %s already exists" % output_dir)

"""
Helper function for reading file formats
"""
# Read from compressed file
def read_gzip_file(file_path):
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        return f.readlines()

# Read from text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

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


"""
Start with the English original annotation for the images
"""
def read_flikr_original(input_file):
    flickr_data = {}
    with open(input_file, 'r') as json_file:
        data = json.load(json_file)

    for key in data.keys():
        if not key == "Image Not Found":
            flickr_data[key] = {}
            flickr_data[key]["eng"] = {}
            flickr_data[key]["eng"]["Original-01"] = data[key][0]
            flickr_data[key]["eng"]["Original-02"] = data[key][1]
            flickr_data[key]["eng"]["Original-03"] = data[key][2]
            flickr_data[key]["eng"]["Original-04"] = data[key][3]
            flickr_data[key]["eng"]["Original-05"] = data[key][4]
    return flickr_data

flikr_data = read_flikr_original('./data/Flickr30k-Original/images-and-descriptions.json')


"""
Add German, French, Czech annotations
"""
def read_flikr_multi(data, split):
    flickr_data = data
    
    if split == "train":
        image_filenames = read_text_file('./data/Flickr30k-Multi30k/data/task1/image_splits/train.txt')
        text_cs = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/train.cs.gz')
        text_de = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/train.de.gz')
        text_en = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/train.en.gz')
        text_fr = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/train.fr.gz')
    elif split == "val":
        image_filenames = read_text_file('./data/Flickr30k-Multi30k/data/task1/image_splits/val.txt')
        text_cs = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/val.cs.gz')
        text_de = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/val.de.gz')
        text_en = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/val.en.gz')
        text_fr = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/val.fr.gz')
    elif split == "test":
        image_filenames = read_text_file('./data/Flickr30k-Multi30k/data/task1/image_splits/test_2016_flickr.txt')
        text_cs = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/test_2016_flickr.cs.gz')
        text_de = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/test_2016_flickr.de.gz')
        text_en = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/test_2016_flickr.en.gz')
        text_fr = read_gzip_file('./data/Flickr30k-Multi30k/data/task1/raw/test_2016_flickr.fr.gz')

    for index in range(len(image_filenames)):
        img_id = image_filenames[index].replace('\n','')
        annotation_cs = text_cs[index].replace('\n','')
        annotation_de = text_de[index].replace('\n','')
        annotation_en = text_en[index].replace('\n','')
        annotation_fr = text_fr[index].replace('\n','')

        if img_id in flickr_data.keys():
            flickr_data[img_id]["ces"] = {}
            flickr_data[img_id]["ces"]["MULTI"] = annotation_cs
            flickr_data[img_id]["deu"] = {}
            flickr_data[img_id]["deu"]["MULTI"] = annotation_de
            flickr_data[img_id]["eng"]["MULTI"] = annotation_en
            flickr_data[img_id]["fra"] = {}
            flickr_data[img_id]["fra"]["MULTI"] = annotation_fr
        else:
            print(f'Image ID not found in original flickr30k data: {img_id}')
    return flickr_data

flikr_data = read_flikr_multi(flikr_data, "train")
flikr_data = read_flikr_multi(flikr_data, "val")
flikr_data = read_flikr_multi(flikr_data, "test")


"""
Add Chinese annotations
"""
def read_flikr_cn(data, input_file):
    flickr_data = data
    with open(input_file, 'r') as text_file:
        text_lines = text_file.readlines()

    for line in text_lines:
        img_id = line.split('#')[0]+'.jpg'
        ann_id = line.split('\t')[0][-1]
        ann_id_int = int(ann_id) + 1
        ann_id_str = "CNA-0"+str(ann_id_int)
        text = line.split('\t')[1].replace('\n','')

        if img_id in flickr_data.keys():
            if not "zho" in flickr_data[img_id]:
                flickr_data[img_id]["zho"] = {}
                flickr_data[img_id]["zho"][ann_id_str] = text
            else:
                flickr_data[img_id]["zho"][ann_id_str] = text
    return flickr_data

flikr_data = read_flikr_cn(flikr_data, './data/Flickr30k-CNA/test/flickr30k_cn_test.txt')

def get_annotator_id(data, item_id):
    if not "CN-01" in data[item_id]["zho"].keys():
        ann_id = "CN-01"
    elif not "CN-02" in data[item_id]["zho"].keys():
        ann_id = "CN-02"
    elif not "CN-03" in data[item_id]["zho"].keys():
        ann_id = "CN-03"
    elif not "CN-04" in data[item_id]["zho"].keys():
        ann_id = "CN-04"
    elif not "CN-05" in data[item_id]["zho"].keys():
        ann_id = "CN-05"
    else:
        print(f'Unexpected number of items for current image id:{item_id}')
        ann_id = "CN-06"
    return ann_id


def read_flikr_cna(data, input_file):
    flickr_data = data
    with open(input_file, 'r') as text_file:
        text_lines = text_file.readlines()

    for line in text_lines:
        img_id = line.split('\t')[0]+'.jpg'
        text = line.split('\t')[1].replace('\n','')

        if img_id in flickr_data.keys():
            if not "zho" in flickr_data[img_id]:
                flickr_data[img_id]["zho"] = {}
                flickr_data[img_id]["zho"]["CN-01"] = text
            else:
                ann_id_str = get_annotator_id(flickr_data, img_id)
                flickr_data[img_id]["zho"][ann_id_str] = text
    return flickr_data

flikr_data = read_flikr_cna(flikr_data, './data/Flickr30k-CNA/train/flickr30k_cna_train.txt')
flikr_data = read_flikr_cna(flikr_data, './data/Flickr30k-CNA/val/flickr30k_cna_val.txt')


"""
Add Ukrainian annotations
"""
def read_flikr_multi_uk(data, input_file):
    flickr_data = data

    text_en = []
    text_uk = []

    text_data = read_text_file(input_file)
    for line in text_data:
        eng_text = line.split('"en":"')[1].split('","uk":"')[0].replace('\n','')
        text_en.append(eng_text)
        ukr_text = line.split('","uk":"')[1].split('"}')[0].replace('\n','')
        text_uk.append(ukr_text)

    #print(f'Number of sentences: {len(text_en)}')
    num_missing_MULTI = len(text_en)

    for index in range(len(text_en)):
        eng_text = text_en[index]
        ukr_text = text_uk[index]
        for key in flickr_data.keys():
            if not "MULTI" in flickr_data[key]["eng"].keys():
                continue
                #print(f'No English Annotation found for: {key}') 
            else:
                if eng_text == flickr_data[key]["eng"]["MULTI"]:
                    flickr_data[key]["ukr"] = {}
                    flickr_data[key]["ukr"]["MULTI-uk"] = ukr_text
                    num_missing_MULTI = num_missing_MULTI - 1
                    break
    print(f'Number of images without a MULTI-annotation: {num_missing_MULTI}')
    return flickr_data

flikr_data = read_flikr_multi_uk(flikr_data, './data/Flickr30k-Multi30k-uk/test_2016_flickr.json')
# → Number of images without a MULTI-annotation: 5
# → Number of sentences: 1000

flikr_data = read_flikr_multi_uk(flikr_data, './data/Flickr30k-Multi30k-uk/test_2017_flickr.json')
# → Number of images without a MULTI-annotation: 1000
# → Number of sentences: 1000

flikr_data = read_flikr_multi_uk(flikr_data, './data/Flickr30k-Multi30k-uk/test_2017_mscoco.json')
# → Number of images without a MULTI-annotation: 461
# → Number of sentences: 461

flikr_data = read_flikr_multi_uk(flikr_data, './data/Flickr30k-Multi30k-uk/test_2018_flickr.json')
# → Number of images without a MULTI-annotation: 1071
# → Number of sentences: 1071

# ! Takes a long time
#flikr_data = read_flikr_multi_uk(flikr_data, './data/Flickr30k-Multi30k-uk/train.json')
# → Number of images without a MULTI-annotation: 139
# → Number of sentences: 29000


# Serializing json and write to file
# json_object = json.dumps(flikr_data, indent=4, ensure_ascii=False)
# with open(f'{output_file}_ukr.json', "w", encoding="utf-8") as outfile:
#     outfile.write(json_object)
# sys.exit()


# Serializing json and write to file
json_object = json.dumps(flikr_data, indent=4, ensure_ascii=False)
with open(f'{output_file}.json', "w", encoding="utf-8") as outfile:
    outfile.write(json_object)




