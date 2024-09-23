# NOTE: Just added a new script to merge the initially collected flikr30k entries with our mtacr-collected entries,
#       just to realize, that I must have done that in the past already... Whoops!
#       Also renamed some of the files, which might result in some older scripts requiring some changes... Whoopsie!
#       → Original flikr30k entries and our mtacr-collected data are together in /data/alignments_mtacr_flikr30k.json

import json

data_path = "./../data"

# Load the first JSON file
with open(f'{data_path}/alignments_flikr30k.json', 'r', encoding='utf-8') as file1:
    data1 = json.load(file1)

# Load the second JSON file
with open(f'{data_path}/data_mtacr_flikr30k_adjusted.json', 'r', encoding='utf-8') as file2:
    data2 = json.load(file2)

# Merge the two JSON dictionaries
merged_data = data2.copy()  # Start with data2's contents

for key, value in data1.items():
    if key in merged_data:
        # If the key (filename) exists in both, combine their annotations
        merged_data[key].update(value)
    else:
        # Otherwise, add the new key-value pair from data1
        merged_data[key] = value

# Save the merged data to a new file
with open(f'{data_path}/alignments_mtacr_flikr30k.json', 'w', encoding='utf-8') as output_file:
    json.dump(merged_data, output_file, ensure_ascii=False, indent=4)

print("JSON files have been merged and saved to a new file")
