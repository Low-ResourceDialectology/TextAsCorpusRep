# -*- coding: utf-8 -*-
# Python Script for highlighting annotations
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Sources:
Colourising and Highlighting Strings in Terminal: https://gist.github.com/ChrisMorrisOrg/4450466

"""

""" User-Guide:
 0. Open a terminal and navigate to your desired directory:
cd PATH_TO_DIRECTORY/TextAsCorpusRep/experiments/annotation-potato
( cd /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/experiments/annotation-potato )

 1. Then activate this environment via
source venvPotato/bin/activate

 2. Start script for creating highlighted text visualisations
python main.py


"""
import json
import os
"""

"""
def highlight_pos_tags_sentence(input_path, output_path, output_name):
    #print(str(input_path))
    #print(str(output_path))
    #print(str(output_name))

    highlighting = True
    colourising = True

    # Colourise - colours text in shell. Returns plain if colour doesn't exist.
    def colourise(colour, text):
        if colour == "black":
            return "\033[1;30m" + str(text) + "\033[1;m"
        if colour == "red":
            return "\033[1;31m" + str(text) + "\033[1;m"
        if colour == "green":
            return "\033[1;32m" + str(text) + "\033[1;m"
        if colour == "yellow":
            return "\033[1;33m" + str(text) + "\033[1;m"
        if colour == "blue":
            return "\033[1;34m" + str(text) + "\033[1;m"
        if colour == "magenta":
            return "\033[1;35m" + str(text) + "\033[1;m"
        if colour == "cyan":
            return "\033[1;36m" + str(text) + "\033[1;m"
        if colour == "gray":
            return "\033[1;37m" + str(text) + "\033[1;m"
        return str(text)

    # Highlight - highlights text in shell. Returns plain if colour doesn't exist.
    def highlight(colour, text):
        if colour == "black":
            return "\033[1;40m" + str(text) + "\033[1;m"
        if colour == "red":
            return "\033[1;41m" + str(text) + "\033[1;m"
        if colour == "green":
            return "\033[1;42m" + str(text) + "\033[1;m"
        if colour == "yellow":
            return "\033[1;43m" + str(text) + "\033[1;m"
        if colour == "blue":
            return "\033[1;44m" + str(text) + "\033[1;m"
        if colour == "magenta":
            return "\033[1;45m" + str(text) + "\033[1;m"
        if colour == "cyan":
            return "\033[1;46m" + str(text) + "\033[1;m"
        if colour == "gray":
            return "\033[1;47m" + str(text) + "\033[1;m"
        return str(text)

    # Example usage:
    """
    print(colourise("black", "Black"))
    print(colourise("red", "Red"))
    print(colourise("green", "Green"))
    print(colourise("yellow", "Yellow"))
    print(colourise("blue", "Blue"))
    print(colourise("magenta", "Magenta"))
    print(colourise("cyan", "Cyan"))
    print(colourise("gray", "Gray"))
    print(highlight("black", "Highlight: black"))
    print(highlight("red", "Highlight: red"))
    print(highlight("green", "Highlight: green"))
    print(highlight("yellow", "Highlight: yellow"))
    print(highlight("blue", "Highlight: blue"))
    print(highlight("magenta", "Highlight: magenta"))
    print(highlight("cyan", "Highlight: cyan"))
    print(highlight("gray", "Highlight: gray"))
    """

    # Example usage of colourise() + highlight()
    """
    text = "Blue on red is difficult to read because the wavelengths are \
    refracted onto different areas of the eye."

    print(highlight("red", (colourise("blue", text))))
    """

    with open(input_path, 'r') as json_file:
        # To load a json file
        #json_data = json.load(json_file)
        #print("id:", str(json_data["id"]))
        #print("span_annotations[0]:", str(json_data["span_annotations"][0]))
        
        # To load a jsonl file
        json_list = list(json_file)
        
        json_data = []
        for json_str in json_list:
            json_data.append(json.loads(json_str))
            #print(f"result: {result}")
            #print(isinstance(result, dict))

        # For each annotated sentence (line in jsonl file)
        for annotation in json_data:
            # Check if current line is something else such as the consent
            if not annotation["id"].startswith('item_'):
                pass
            else:
                sentence_highlighted = ""
                sentence_colourized = ""
                #print(annotation["span_annotations"][0])

                # For each word of current annotated sentence
                for tag in annotation["span_annotations"]:
                    #print(tag)
                    text = tag["span"]
                    if tag["annotation"] == "Subject (proper noun?)":
                        if highlighting:
                            highlighted = highlight("red", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("red", text)
                            sentence_colourized=sentence_colourized+colourized+" "

                    elif tag["annotation"] == "Verb (run,read,is)":
                        if highlighting:
                            highlighted = highlight("green", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("green", text)
                            sentence_colourized=sentence_colourized+colourized+" "

                    elif tag["annotation"] == "Object (noun?)":
                        if highlighting:
                            highlighted = highlight("yellow", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("yellow", text)
                            sentence_colourized=sentence_colourized+colourized+" "

                    elif tag["annotation"] == "Adjective (green,tiny)":
                        if highlighting:
                            highlighted = highlight("blue", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("blue", text)
                            sentence_colourized=sentence_colourized+colourized+" "
                        
                    elif tag["annotation"] == "Adverb (quickly,very)":
                        if highlighting:
                            highlighted = highlight("orange", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("orange", text)
                            sentence_colourized=sentence_colourized+colourized+" "
                        
                    elif tag["annotation"] == "Preposition (on,beside,)":
                        if highlighting:
                            highlighted = highlight("magenta", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("magenta", text)
                            sentence_colourized=sentence_colourized+colourized+" "
                        
                    elif tag["annotation"] == "Conjunction (and,but,or)":
                        if highlighting:
                            highlighted = highlight("cyan", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("cyan", text)
                            sentence_colourized=sentence_colourized+colourized+" "
                        
                    elif tag["annotation"] == "Determiner (the,a,this)":
                        if highlighting:
                            highlighted = highlight("gray", text)
                            sentence_highlighted=sentence_highlighted+highlighted+" "
                        if colourising:
                            colourized = colourise("gray", text)
                            sentence_colourized=sentence_colourized+colourized+" "
                        
                    else:
                        if highlighting:
                            sentence_highlighted=sentence_highlighted+text+" "
                        if colourising:
                            sentence_colourized=sentence_colourized+text+" "
                else:
                    if highlighting:
                        print(sentence_highlighted)
                        with open(output_path+output_name+'-'+annotation["id"]+'-highlighted.txt', 'w') as f:     
                            f.write(sentence_highlighted)

                    if colourising:
                        print(sentence_colourized)
                        with open(output_path+output_name+'-'+annotation["id"]+'-colourised.txt', 'w') as f:     
                            f.write(sentence_colourized)

            

        



