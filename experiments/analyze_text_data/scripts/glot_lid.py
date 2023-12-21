# -*- coding: utf-8 -*-
# Python Script for all types of reoccuring functionalities
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

"""
GlotLID: https://github.com/cisnlp/GlotLID
"""

import fasttext
from huggingface_hub import hf_hub_download

def main(cache_directory):
    # ===========================================
    # Download Model
    # ===========================================
    ## cache_dir: path to the folder where the downloaded model will be stored/cached.
    model_path = hf_hub_download(repo_id="cis-lmu/glotlid", filename="model.bin", cache_dir=cache_directory)

    # ===========================================
    # Load Model
    # ===========================================
    model = fasttext.load_model(model_path)

    # ===========================================
    # Predict Language Label
    # ===========================================
    #model.predict("Hello, world!")

    return model

