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
import os 

# Path to nllb-seed data (6193 text lines)
input_path = './../data/mtacr-translator-splits/'

# For all text files in current directory
for filename in os.listdir(input_path):
    input_textfile = os.path.join(input_path, filename)

    indexed_text = []
    line_index = 1

    # Read the file
    with open(input_textfile, "r") as f:
        text = f.read().splitlines()
        
        for text_line in text:
            new_line = str(line_index).zfill(4)+': '+text_line

            indexed_text.append(new_line)
            line_index += 1

    with open(input_textfile, "w") as f:
        for text_line in indexed_text:
            f.writelines(text_line+'\n')

