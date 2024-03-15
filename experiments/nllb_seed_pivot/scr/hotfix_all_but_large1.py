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
input_file2 = './../data/output/large_01.txt.txt'

def read_data(input_file):
    # Read the file
    with open(input_file, "r") as f:
        text = f.read().splitlines()
        return text

nllb_seed_data = read_data(input_file)

large_data = read_data(input_file2)
large_data_clean = []

# Remove the translator helper indices
for text_line in large_data:
    new_line = text_line[6:]
    large_data_clean.append(new_line)


# Only keep the sentences that have not been included inside or large_data
final_split = []

for text_line in nllb_seed_data:
    if text_line not in large_data_clean:
        final_split.append(text_line)


output_file = './../data/output/entire-lara.txt'

with open(output_file, "w") as f:
    for text_line in final_split:
        f.writelines(text_line+'\n')

