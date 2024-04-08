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


flikr_data = {}
output_file = './flikr30k/flikr30k-aligned'

def read_flikr_files(input_file, language):
    csv_rows_list = []

    with open(input_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in csv_reader:
            csv_rows_list.append(row)

    for row in csv_rows_list:
        translator_id = row[0]
        instance_id = row[1]
        if len(instance_id) <= 6: 
            annotation = row[3]
            if not annotation == '':
                if not instance_id in flikr_data:
                    flikr_data[instance_id] = {}
                    flikr_data[instance_id][language] = {}
                    flikr_data[instance_id][language][translator_id] = annotation.replace('\n','').strip()
                else:
                    if not language in flikr_data[instance_id].keys():
                        flikr_data[instance_id][language] = {}
                        flikr_data[instance_id][language][translator_id] = annotation.replace('\n','').strip()
                    else:
                        flikr_data[instance_id][language][translator_id] = annotation.replace('\n','').strip()


# Input files based on "annotated_instances.csv" files from language folders
data_file = './flikr30k/kob/annotated_instances.csv'
language = "kob"
read_flikr_files(data_file, language)

data_file = './flikr30k/mfe/annotated_instances.csv'
language = "mfe"
read_flikr_files(data_file, language)

data_file = './flikr30k/vie/annotated_instances.csv'
language = "vie"
read_flikr_files(data_file, language)

data_file = './flikr30k/zho/annotated_instances.csv'
language = "zho"
read_flikr_files(data_file, language)

# Trying to sort based on key value (id of the image)
#flikr_data_sorted = sorted(flikr_data) 
#sorted_dict = dict(sorted(flikr_data.items()))
#sorted_dict = dict(sorted(flikr_data.items(), key=zero_pad_numbers))
#sorted_dict = dict(sorted(flikr_data.items()))
#sorted_dict = {k: flikr_data[k] for k in sorted(flikr_data)}
"""
sorted_dict = dict(sorted(flikr_data.items(), key=lambda item: len(item[0])))
"""

# Some information about the data
number_of_images = len(flikr_data.keys())
print(f'Number of annotated images: {number_of_images}')


# Sort in descending order based on number of annotations for the image
sorted_flikr_data = sorted(flikr_data.items(), key=lambda x:len(x[1]), reverse=True)

sorted_dict = dict(sorted_flikr_data)

# Serializing json and write to file
json_object = json.dumps(sorted_dict, indent=4, ensure_ascii=False)
with open(f'{output_file}.json', "w", encoding="utf-8") as outfile:
    outfile.write(json_object)

