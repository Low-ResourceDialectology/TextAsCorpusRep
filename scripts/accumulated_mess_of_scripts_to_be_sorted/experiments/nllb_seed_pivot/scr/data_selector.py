# -*- coding: utf-8 -*-
# Python Script for working with text data from available datasets
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

# Path to project repository: /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep

"""Use
# =====================================================================
# Selecting subsets (lines) for translation tasks
python data_selector.py

"""

# Path to nllb-seed data (6193 text lines)
input_file = './../data/input/eng_Latn'


def read_data(input_file):
    # Read the file
    with open(input_file, "r") as f:
        text = f.read().splitlines()
        return text


def select_subset(starting_line, data, subset_size):
    new_subset = []

    for index in range(subset_size):
        line_number = starting_line + index
        selected_line = data[line_number]
        new_subset.append(selected_line)

    return new_subset


def create_split(split_name, split_number, subset_size, step_size, starting_points_for_lines):

    nllb_seed_data = read_data(input_file)

    starting_points_for_lines = starting_points_for_lines # Anchor: [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181]
    subset_size = subset_size # Anchor: 6
    current_subsets = []

    for starting_point in starting_points_for_lines:
        current_subset = select_subset(starting_point, nllb_seed_data, subset_size)

        current_subsets.append(current_subset)


    # For some reasons, consistency not being the least of them, the split is constructed bit-by-bit from the extracted subsets
    step_size = step_size # Anchor: 6
    final_split = []
    index_counter = 0 
    index_limit = len(current_subsets[0])

    while index_counter < index_limit:

        for subset in current_subsets:
            for line_index in range(index_counter, index_counter+step_size):
                final_split.append(subset[line_index])
                #print(f'line_index: {line_index}')

        index_counter = index_counter + step_size
        #print(f'index_counter: {index_counter}')


    output_file = './../data/output/'+split_name+'_'+str(int(split_number))+'.txt'

    with open(output_file, "w") as f:
        for text_line in final_split:
            f.writelines(text_line+'\n')
    

""" For the Anchor-Split creation

split_name = 'anchor'
split_number = 1
subset_size = 6
step_size = 6
starting_points_for_lines = [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181]

create_split(subset_size, step_size, starting_points_for_lines)
→
config = ['anchor', 1, 6, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181]]
create_split(config[0], config[1], config[2], config[3], config[4])
"""

configs = [
    ['anchor', 1, 6, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181]],
    ['tiny', 1, 12, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181]],
    ['tiny', 2, 6, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181, 
                       12, 1564, 2710, 3437, 3893, 4094, 5548, 6175]],
    ['tiny', 3, 6, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6181,
                        18, 1560, 2716, 3443, 3899, 4100, 5554, 6169]],
    ['small', 1, 18, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6175]],
    ['small-pascaline', 2, 18, 6, [18, 1570, 2716, 3443, 3899, 4100, 5554, 6157]],
    ['medium', 1, 30, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6163]],
    ['large', 1, 60, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6133]],
    ['large-megan', 2, 60, 6, [60, 1612, 2758, 3485, 3941, 4142, 5596, 6073]],
    ['huge', 1, 120, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6073]],
    ['huge-ni', 1, 120, 6, [0, 1552, 2698, 3425, 3881, 4082, 5536, 6073]],
    ['gigantic', 1, 360, 6, [0, 1552, 2698, 3360, 3721, 4082, 5536, 5833]],
    ['gigantic-tanh', 1, 360, 6, [0, 1552, 2698, 3360, 3721, 4082, 5536, 5833]]
]

for config in configs:
    create_split(config[0], config[1], config[2], config[3], config[4])


""" Information regarding the splits

- Anchor Text Lines: 1-6, 1553-1558, 2699-2704, 3426-3431, 3882-3887, 4083-4088, 5537-5542, 6182-6187

- Starting Points for line-subsets to select for splits:
    1, 1553, 2699, 3426, 3882, 4083, 5537, 6182

- Name      # lines     # words         # lines per subset
- Anchor    48 lines    1,015 words     6
- Tiny      96 lines    2,065 words     12
- Small     144 lines   3,096 words     18
- Medium    240 lines   5,026 words     30
- Large     480 lines   10,210 words    60
- Huge      960 lines   21,309 words    120
- Gigantic  2880 lines  64,052 words    360
- Entire    6,193 lines 136,528 words
- All       6,193 lines 136,528 words   


"""

