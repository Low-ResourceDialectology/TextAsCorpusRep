# -*- coding: utf-8 -*-
# Python Script for plotting highlighted annotations of sentences
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

""" Sources:

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
import ast
import matplotlib.pyplot as plt
import numpy as np
import os
"""

"""
def plot_highlighted_pos_tags_sentence(example, input_path, output_path, output_name):


    """ # Sentences (long ones) cut off on the side
    def plot_highlighted_sentences_single_plot(sentences, pos_colors, output_path, output_name):
        # Plot multiple sentences in the same plot with each sentence on a new line
        plt.figure(figsize=(8, 6))

        line_height = 0.1  # Height between lines
        x_position = 0.1  # Initial x position
        y_position = 1.0  # Initial y position

        for sentence in sentences:
            #print(sentence)
            #print(type(sentence))
            if sentence and isinstance(sentence[0], tuple):
                words, tags = zip(*sentence)
                total_word_length = sum(len(word) for word, _ in sentence)
                avg_word_length = total_word_length / len(sentence)
                word_gap = max(0.05, 0.015 - 0.005 * avg_word_length)  # Adjust word gap based on average word length

                for word, tag in sentence:
                    plt.text(x_position, y_position, word, ha='left', va='center', color=pos_colors.get(tag, 'white'), fontsize=16, weight="bold")
                    x_position += len(word) * 0.01 + word_gap  # Adjust x position based on word length and word gap

                y_position -= line_height
                x_position = 0.1  # Reset x position for the next sentence
            else:
                print("Sentence is empty or has an incorrect structure.")

        plt.xlim(0, 1)
        plt.ylim(-1, 1)
        plt.axis('off')
        plt.savefig(output_path+output_name+'.png', bbox_inches='tight')
        plt.show()
    """
    
    def plot_highlighted_sentences_single_plot(sentences, pos_colors, output_path, output_name):
        # Calculate the total number of lines needed for all sentences
        num_lines = sum(len(sentence) for sentence in sentences)
        
        # Set a maximum number of lines to occupy in the plot
        max_lines = 30  # Adjust this value as needed
        
        # Calculate the required figure height based on the number of lines
        fig_height = min(num_lines, max_lines) * 0.4  # Adjust the multiplication factor as needed
        
        # Calculate the figure width based on the maximum length of a sentence
        max_sentence_length = max(sum(len(word) for word, _ in sentence) for sentence in sentences)
        fig_width = max_sentence_length * 0.03  # Adjust the multiplication factor as needed

        # Plot sentences within the determined figure size
        plt.figure(figsize=(fig_width, fig_height))

        line_height = 0.5  # Height between lines
        x_position = 0.1  # Initial x position
        y_position = 0.1  # Initial y position

        for sentence in sentences:
            if sentence and isinstance(sentence[0], tuple):
                words, tags = zip(*sentence)
                total_word_length = sum(len(word) for word, _ in sentence)
                word_count = len(sentence)

                # Set background color for the entire sentence
                plt.axhspan(y_position - line_height, y_position, facecolor='lightgray', alpha=0.3)

                for word, tag in sentence:
                    # Calculate word gap dynamically based on individual word lengths
                    word_gap = max(0.01, 0.1 - 0.002 * len(word))  # Adjust the multiplication factor as needed

                    plt.text(x_position, y_position, word, ha='left', va='center', color=pos_colors.get(tag, 'black'), fontsize=16, weight="bold")
                    x_position += len(word) * 0.01 + word_gap  # Adjust x position based on word length and word gap
                """
                avg_word_length = total_word_length / len(sentence)
                word_gap = max(0.05, 0.015 - 0.005 * avg_word_length)  # Adjust word gap based on average word length
                
                for word, tag in sentence:
                    plt.text(x_position, y_position, word, ha='left', va='center', color=pos_colors.get(tag, 'black'), fontsize=16, weight="bold")
                    x_position += len(word) * 0.01 + word_gap  # Adjust x position based on word length and word gap
                """

                y_position -= line_height
                x_position = 0.1  # Reset x position for the next sentence
            else:
                print("Sentence is empty or has an incorrect structure.")

        plt.xlim(0, 1)
        plt.ylim(-fig_height, 1)  # Update the y-axis limit based on the figure height
        plt.axis('off')
        plt.savefig(output_path + output_name + '.png', bbox_inches='tight')
        plt.show()




    if example:
        # Define colors for different POS tags
        pos_colors = {
            "DET": "lightblue",
            "NOUN": "lightgreen",
            "VERB": "lightsalmon",
            "ADJ": "lightpink",
            "ADV": "lightyellow",
            "ADP": "lightcoral",
            "PRON": "lightgrey"
        }

        # Sample data: sentences with their POS tags
        sentences = [
            [("The", "DET"), ("cat", "NOUN"), ("is", "VERB"), ("on", "ADP"), ("the", "DET"), ("mat", "NOUN")],
            [("A", "DET"), ("quick", "ADJ"), ("brown", "ADJ"), ("fox", "NOUN"), ("jumped", "VERB"), ("over", "ADP"), ("the", "DET"), ("lazy", "ADJ"), ("dog", "NOUN")],
            [("The", "DET"), ("sun", "NOUN"), ("is", "VERB"), ("shining", "VERB"), ("brightly", "ADV")],
            [("She", "PRON"), ("played", "VERB"), ("the", "DET"), ("piano", "NOUN"), ("beautifully", "ADV")]
        ]

        plot_highlighted_sentences_single_plot(sentences, pos_colors, output_path, output_name)

    else:
        # Define colors for different POS tags
        pos_colors = {
            "DET": "gray",
            "NOUN": "red",
            "VERB": "green",
            "ADJ": "blue",
            "ADV": "orange",
            "ADP": "lightcoral",
            "PRON": "lightgrey",
            "OBJ": "yellow",
            "IN": "magenta",
            "CC": "cyan"
        }

        sentences = []

        # Read from file a list of lists that contain tuples
        with open(input_path, 'r') as f:
            sentences = f.readlines()
            # Debugging-Shenanigans!
            #print(sentences)
            #print("")
            #print(sentences[0])
            #print(sentences[0][0])
            #print(list(sentences[0])[0])
            # Convert strings to list of tuples
            list_of_tuples = [ast.literal_eval(entry) for entry in sentences]

            #sentences = list(str(sentences).replace('"', ''))
            #print(list_of_tuples)
            #print("")
            #print(list_of_tuples[0])
            #print(list_of_tuples[0][0])
        
        plot_highlighted_sentences_single_plot(list_of_tuples, pos_colors, output_path, output_name)
    


    """
    # Sentences on top of each other with highlighted pos-tags in colors
    # Sample data: sentences with their POS tags
    sentences = [
        [("The", "DET"), ("cat", "NOUN"), ("is", "VERB"), ("on", "ADP"), ("the", "DET"), ("mat", "NOUN")],
        [("A", "DET"), ("quick", "ADJ"), ("brown", "ADJ"), ("fox", "NOUN"), ("jumped", "VERB"), ("over", "ADP"), ("the", "DET"), ("lazy", "ADJ"), ("dog", "NOUN")],
        [("The", "DET"), ("sun", "NOUN"), ("is", "VERB"), ("shining", "VERB"), ("brightly", "ADV")],
        [("She", "PRON"), ("played", "VERB"), ("the", "DET"), ("piano", "NOUN"), ("beautifully", "ADV")]
    ]

    # Define colors for different POS tags
    pos_colors = {
        "DET": "lightblue",
        "NOUN": "lightgreen",
        "VERB": "lightsalmon",
        "ADJ": "lightpink",
        "ADV": "lightyellow",
        "ADP": "lightcoral",
        "PRON": "lightgrey"
    }

    # Plot multiple sentences in the same plot with each sentence on a new line
    plt.figure(figsize=(8, 6))

    line_height = 0.1  # Height between lines
    sentence_gap = 0.2  # Gap between sentences
    x_position = 0.1  # Initial x position
    y_position = 1.0  # Initial y position

    for sentence in sentences:
        words, tags = zip(*sentence)
        for word, tag in sentence:
            plt.text(x_position, y_position, word, ha='left', va='center', color=pos_colors.get(tag, 'white'), fontsize=16, weight="bold")
            x_position += len(word) * 0.025  # Adjust x position based on word length
        y_position -= sentence_gap
        x_position = 0.1  # Reset x position for the next sentence

    plt.xlim(0, 1)
    plt.ylim(-1, 1)
    plt.axis('off')
    plt.show()
    """

    """
    # One plot containing all sentences- but each word is in a new line
    # Sample data: sentences with their POS tags
    sentences = [
        [("The", "DET"), ("cat", "NOUN"), ("is", "VERB"), ("on", "ADP"), ("the", "DET"), ("mat", "NOUN")],
        [("A", "DET"), ("quick", "ADJ"), ("brown", "ADJ"), ("fox", "NOUN"), ("jumped", "VERB"), ("over", "ADP"), ("the", "DET"), ("lazy", "ADJ"), ("dog", "NOUN")],
        [("The", "DET"), ("sun", "NOUN"), ("is", "VERB"), ("shining", "VERB"), ("brightly", "ADV")],
        [("She", "PRON"), ("played", "VERB"), ("the", "DET"), ("piano", "NOUN"), ("beautifully", "ADV")]
    ]

    # Define colors for different POS tags
    pos_colors = {
        "DET": "lightblue",
        "NOUN": "lightgreen",
        "VERB": "lightsalmon",
        "ADJ": "lightpink",
        "ADV": "lightyellow",
        "ADP": "lightcoral",
        "PRON": "lightgrey"
    }

    # Plot multiple sentences in the same plot vertically
    plt.figure(figsize=(8, 6))

    line_height = 0.1  # Height between lines
    sentence_gap = 0.1  # Gap between sentences
    y_position = 1.0  # Initial y position

    for sentence in sentences:
        words, tags = zip(*sentence)
        for word, tag in sentence:
            plt.text(0.5, y_position, word, ha='center', va='center', color=pos_colors.get(tag, 'white'), fontsize=12)
            y_position -= line_height
        y_position -= sentence_gap

    plt.xlim(0, 1)
    plt.ylim(-1, 1)
    plt.axis('off')
    plt.show()
    """

    """
    # One figure holding a grid of the sentence-plots
    # Sample data: sentences with their POS tags
    sentences = [
        [("The", "DET"), ("cat", "NOUN"), ("is", "VERB"), ("on", "ADP"), ("the", "DET"), ("mat", "NOUN")],
        [("A", "DET"), ("quick", "ADJ"), ("brown", "ADJ"), ("fox", "NOUN"), ("jumped", "VERB"), ("over", "ADP"), ("the", "DET"), ("lazy", "ADJ"), ("dog", "NOUN")],
        [("The", "DET"), ("sun", "NOUN"), ("is", "VERB"), ("shining", "VERB"), ("brightly", "ADV")],
        [("She", "PRON"), ("played", "VERB"), ("the", "DET"), ("piano", "NOUN"), ("beautifully", "ADV")]
    ]

    # Define colors for different POS tags
    pos_colors = {
        "DET": "lightblue",
        "NOUN": "lightgreen",
        "VERB": "lightsalmon",
        "ADJ": "lightpink",
        "ADV": "lightyellow",
        "ADP": "lightcoral",
        "PRON": "lightgrey"
    }

    # Plot multiple sentences in a grid
    num_sentences = len(sentences)
    cols = 3  # Number of columns in the grid
    rows = -(-num_sentences // cols)  # Calculate number of rows needed

    plt.figure(figsize=(12, 4 * rows))

    for i, sentence in enumerate(sentences):
        plt.subplot(rows, cols, i + 1)
        plt.subplots_adjust(hspace=0.5)  # Adjust vertical spacing between subplots
        words, tags = zip(*sentence)
        for j, (word, tag) in enumerate(sentence):
            plt.text(j + 0.5, 0.5, word, ha='center', va='center', color=pos_colors.get(tag, 'white'), fontsize=12)
        plt.xticks(np.arange(0.5, len(words) + 0.5), words)
        plt.yticks([])
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.title(' '.join(words), fontsize=12)

    plt.tight_layout()
    plt.show()
    """

    """
    # Single Sentence per plot
    # Sample data: sentences with their POS tags
    sentences = [
        [("The", "DET"), ("cat", "NOUN"), ("is", "VERB"), ("on", "ADP"), ("the", "DET"), ("mat", "NOUN")],
        [("A", "DET"), ("quick", "ADJ"), ("brown", "ADJ"), ("fox", "NOUN"), ("jumped", "VERB"), ("over", "ADP"), ("the", "DET"), ("lazy", "ADJ"), ("dog", "NOUN")]
    ]

    # Define colors for different POS tags
    pos_colors = {
        "DET": "lightblue",
        "NOUN": "lightgreen",
        "VERB": "lightsalmon",
        "ADJ": "lightpink",
        "ADP": "lightyellow"
    }

    # Create a plot for each sentence
    def plot_sentence(sentence):
        plt.figure(figsize=(8, 2))
        words, tags = zip(*sentence)
        for i, (word, tag) in enumerate(sentence):
            plt.text(i + 0.5, 0.5, word, ha='center', va='center', color=pos_colors.get(tag, 'white'), fontsize=12)
        plt.xticks(np.arange(0.5, len(words) + 0.5), words)
        plt.yticks([])
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.title(' '.join(words), fontsize=14)
        plt.show()

    # Plot each sentence
    for sentence in sentences:
        plot_sentence(sentence)
    """

