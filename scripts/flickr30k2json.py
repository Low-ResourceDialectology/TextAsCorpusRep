import re
import json
import io
import csv

#from sys import maxint
maxint = 2147483647

# optional '-' to support negative numbers
_num_re = re.compile(r'-?\d+')
# number of chars in the largest possible int
_maxint_digits = len(str(maxint))
# format for zero padding positive integers
_zero_pad_int_fmt = '{0:0' + str(_maxint_digits) + 'd}'
# / is 0 - 1, so that negative numbers will come before positive
_zero_pad_neg_int_fmt = '/{0:0' + str(_maxint_digits) + 'd}'


def _zero_pad(match):
    n = int(match.group(0))
    # if n is negative, we'll use the negative format and flip the number using
    # maxint so that -2 comes before -1, ...
    return _zero_pad_int_fmt.format(n) \
        if n > -1 else _zero_pad_neg_int_fmt.format(n + maxint)

def zero_pad_numbers(s):
    return _num_re.sub(_zero_pad, s)


flickr_data = {}
output_file = './../data/Multi30k_data/Flickr30k-MTACR/flickr30k-aligned'

def read_flickr_files(flickr_data, input_file, language):
    csv_rows_list = []

    with open(input_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            csv_rows_list.append(row)

    for row in csv_rows_list:
        translator_id = row[0]
        #translator_id = row['user']
        instance_id = row[1]
        #instance_id = row['instance_id']
        if len(instance_id) <= 6: 
            #annotation = row[3]
            # if row['textbox_input:::Description']:
            #     annotation = row['textbox_input:::Description']
            # if row['textbox_input:::Sự miêu tả']:
            #     annotation = row['textbox_input:::Sự miêu tả']
            # if row['textbox_input:::Şirove']:
            #     annotation = row['textbox_input:::Şirove']
            # if row['textbox_input:::描述']:
            #     annotation = row['textbox_input:::描述']
            if language == 'kob':
                annotation = row[16]
            elif language == 'mfe':
                annotation = row[20]
            elif language == 'vie':
                annotation = row[3]
            elif language == 'zho':
                annotation = row[3]
            else:
                annotation = ''
            if not annotation == '':
                if not instance_id in flickr_data:
                    flickr_data[instance_id] = {}
                    flickr_data[instance_id][language] = {}
                    flickr_data[instance_id][language][translator_id] = annotation.replace('\n','').strip()
                else:
                    if not language in flickr_data[instance_id].keys():
                        flickr_data[instance_id][language] = {}
                        flickr_data[instance_id][language][translator_id] = annotation.replace('\n','').strip()
                    else:
                        flickr_data[instance_id][language][translator_id] = annotation.replace('\n','').strip()
    return flickr_data


# Input files based on "annotated_instances.csv" files from language folders
data_file = './../data/flickr30k/kob/annotated_instances.csv'
language = "kob"
flickr_data = read_flickr_files(flickr_data, data_file, language)

data_file = './../data/flickr30k/mfe/annotated_instances.csv'
language = "mfe"
flickr_data = read_flickr_files(flickr_data, data_file, language)

data_file = './../data/flickr30k/vie/annotated_instances.csv'
language = "vie"
flickr_data = read_flickr_files(flickr_data, data_file, language)

data_file = './../data/flickr30k/zho/annotated_instances.csv'
language = "zho"
flickr_data = read_flickr_files(flickr_data, data_file, language)

# Trying to sort based on key value (id of the image)
#flickr_data_sorted = sorted(flickr_data) 
#sorted_dict = dict(sorted(flickr_data.items()))
#sorted_dict = dict(sorted(flickr_data.items(), key=zero_pad_numbers))
#sorted_dict = dict(sorted(flickr_data.items()))
#sorted_dict = {k: flickr_data[k] for k in sorted(flickr_data)}
"""
sorted_dict = dict(sorted(flickr_data.items(), key=lambda item: len(item[0])))
"""

# Some information about the data
number_of_images = len(flickr_data.keys())
print(f'Number of annotated images: {number_of_images}')


# Sort in descending order based on number of annotations for the image
sorted_flickr_data = sorted(flickr_data.items(), key=lambda x:len(x[1]), reverse=True)

sorted_dict = dict(sorted_flickr_data)

# Serializing json and write to file
json_object = json.dumps(sorted_dict, indent=4, ensure_ascii=False)
with open(f'{output_file}.json', "w", encoding="utf-8") as outfile:
    outfile.write(json_object)

