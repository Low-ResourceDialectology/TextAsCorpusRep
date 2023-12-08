# -*- coding: utf-8 -*-
# Python Script for transforming annotated sentences from potato for plotting
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

import json
import os

"""

"""
def transform_annotations_for_plotting(input_path, output_path, output_name):

    # Read jsonl-file
    with open(input_path, 'r') as json_file:

        # To load a jsonl file
        json_list = list(json_file)
        
        json_data = []
        for json_str in json_list:
            json_data.append(json.loads(json_str))

        annotation_data = []

        # For each annotated sentence (line in jsonl file)
        for annotation_line in json_data:            

            annotation_line_data = []

            # Check if current line is something else such as the consent
            if not annotation_line["id"].startswith('item_'):
                pass
            else:
                # For each annotated word in current line
                for annotated_tag in annotation_line["span_annotations"]:
                    current_pos_tag = "NO-TAG"

                    if annotated_tag["annotation"] == "Subject (proper noun?)":
                        current_pos_tag = "NOUN"
                    elif annotated_tag["annotation"] == "Verb (run,read,is)":
                        current_pos_tag = "VERB"
                    elif annotated_tag["annotation"] == "Object (noun?)":
                        current_pos_tag = "OBJ"
                    elif annotated_tag["annotation"] == "Adjective (green,tiny)":
                        current_pos_tag = "ADJ"
                    elif annotated_tag["annotation"] == "Adverb (quickly,very)":
                        current_pos_tag = "ADV"
                    elif annotated_tag["annotation"] == "Preposition (on,beside,)":
                        current_pos_tag = "IN"
                    elif annotated_tag["annotation"] == "Conjunction (and,but,or)":
                        current_pos_tag = "CC"
                    elif annotated_tag["annotation"] == "Determiner (the,a,this)":
                        current_pos_tag = "DET"
                    elif annotated_tag["annotation"] == "Adposition (in,to,during)":
                        current_pos_tag = "ADP"
                    elif annotated_tag["annotation"] == "Pronoun (he,she,it)":
                        current_pos_tag = "PRON"
                    else:
                        current_pos_tag = "UKNOWN-TAG"
                    
                    """ # A more complete version
                    current_annotation = {
                        "id":annotation_line["id"],
                        "span":annotation_line["span"],
                        "annotation":annotation_line["annotation"],
                        "pos":(annotation_line["span"], current_pos_tag)
                    }
                    """
                    current_annotation = (annotated_tag["span"], current_pos_tag)
                    
                    # Add current word to data of current line
                    annotation_line_data.append(current_annotation)

            # Add current line to data
            annotation_data.append(annotation_line_data)
        
        # Write transformed annotation data to file
        with open(output_path+output_name+'.txt', 'w') as f:
            for annotated_sentence in annotation_data:
                f.write(str(annotated_sentence)+'\n')



    # Transform the tagged data

    # Save data to new jsonl-file


    """ # Structure used in the plottin script
    sentences = [
        [("The", "DET"), ("cat", "NOUN"), ("is", "VERB"), ("on", "ADP"), ("the", "DET"), ("mat", "NOUN")],
    ]
    """

    """ # Colors used in Plotting
    pos_colors = {
            "DET": "lightblue",
            "NOUN": "lightgreen",
            "VERB": "lightsalmon",
            "ADJ": "lightpink",
            "ADV": "lightyellow",
            "ADP": "lightcoral",
            "PRON": "lightgrey"
        }
    """

    """ # POS-Tag used in Plotting
    sentences = [
            [
                ("The", "DET"), 
                ("cat", "NOUN"), 
                ("is", "VERB"), 
                ("on", "ADP"), 
                ("the", "DET"), 
                ("mat", "NOUN")
            ],
        ]
    """