"""
pip install wordcloud
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import sys

from wordcloud import WordCloud

# Function to generate a word cloud from a frequency dictionary
def generate_word_cloud(frequency_dict, language):
    if language == "Chinese":
        # Specify the font path for Chinese characters
        chinese_font_path = "./MaShanZheng-Regular.ttf"
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=chinese_font_path).generate_from_frequencies(frequency_dict)
    else:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequency_dict)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    #plt.title(f'Word Cloud - {language}')
    plt.savefig(f'./../../logs/{language}-wordcloud.png', bbox_inches='tight')
    #plt.show()
"""
# NOTE: For displaying Chinese characters:
1. First, download a Chinese font file (TTF format). You can find Chinese fonts on websites like Google Fonts or other font repositories.
2. Place the downloaded font file in the same directory as your Python script, or provide the full path to the font file.
3. Modify your script to include the font path when creating the WordCloud instance:
"""

# Generate word clouds for each language
def create_wordcloud_plots():
    pass
    #TODO
    
    


def create_line_plots(frequency_data, language="Multiple Languages"):

    # Sort the combined dictionary by frequency in descending order
    sorted_mfe_combined = dict(sorted(frequency_data.items(), key=lambda item: item[1], reverse=True))

    # Find the maximum frequency value
    max_frequency = max(sorted_mfe_combined.values())

    # Create dynamic x-axis ticks and labels
    x_ticks = []
    x_labels = []
    group_size = 100

    while group_size <= max_frequency:
        x_ticks.append(group_size)
        x_labels.append(f"{group_size - 99}-{group_size}")
        group_size *= 10  # Increase group size dynamically

    # Plot the scatter plot with dynamically adjusted group sizes
    plt.scatter(x_ticks, [sorted_mfe_combined.get(f"{i + 1}-{i + group_size}", 0) for i, group_size in enumerate(x_ticks)], alpha=0.5, label='Word Frequency')
    plt.xscale('log')  # Set x-axis to logarithmic scale
    plt.xlabel('Word Rank (Grouped)')
    plt.ylabel('Word Frequency')
    plt.title('Word Frequencies for Multiple Languages')
    plt.legend()
    plt.show()

    sys.exit()


    # Sort the combined dictionary by frequency in descending order
    sorted_frequency_data = dict(sorted(frequency_data.items(), key=lambda item: item[1], reverse=True))

    """
    NOTE: Simple version that can not handle strongly skewed data
    # Plot the line chart
    plt.plot(range(1, len(sorted_frequency_data) + 1), list(sorted_frequency_data.values()), marker='o', linestyle='-', color='b')

    #plt.xscale('log')  # Set x-axis to logarithmic scale
    #plt.yscale('log')  # Set y-axis to logarithmic scale
    plt.xlabel('Word Rank (log scale)')
    plt.ylabel('Word Frequency (log scale)')
    plt.title(f'Word Frequencies for {language}')
    plt.savefig(f'./../../logs/{language}-lineplot.png', bbox_inches='tight')
    plt.show()
    """

    """
    NOTE: First 100 values normally, then grouping them by 100-er
    # Create x-axis ticks and labels
    x_ticks = []
    x_labels = []
    group_size = 100
    for i in range(0, len(sorted_frequency_data), group_size):
        x_ticks.append(i + 0.5 * group_size)
        x_labels.append(f"{i + 1}-{i + group_size}")

    # Plot the scatter plot for the first 100 entries and group the rest
    plt.scatter(range(1, len(sorted_frequency_data) + 1), list(sorted_frequency_data.values()), alpha=0.5, label='Word Frequency')
    plt.xticks(x_ticks, x_labels, rotation='vertical')
    plt.xlabel('Word Rank (Grouped)')
    plt.ylabel('Word Frequency')
    plt.title('Word Frequencies for Multiple Languages')
    plt.legend()
    plt.show()
    """


    """
    NOTE: Introducing dynamically sized groups now

    """
    # Find the maximum frequency value
    max_frequency = max(sorted_frequency_data.values())

    # Create dynamic x-axis ticks and labels
    x_ticks = []
    x_labels = []
    group_size = 100

    """
    while group_size <= max_frequency:
        for i in range(0, len(sorted_frequency_data), group_size):
            x_ticks.append(i + 0.5 * group_size)
            x_labels.append(f"{i + 1}-{i + group_size}")
        group_size *= 100  # Increase group size dynamically

    # Plot the scatter plot with dynamically adjusted group sizes
    plt.scatter(range(1, len(sorted_frequency_data) + 1), list(sorted_frequency_data.values()), alpha=0.5, label='Word Frequency')
    plt.xticks(x_ticks, x_labels, rotation='vertical')
    plt.xlabel('Word Rank (Grouped)')
    plt.ylabel('Word Frequency')
    plt.title('Word Frequencies for Multiple Languages')
    plt.legend()
    plt.show()
    """
    while group_size <= max_frequency:
        x_ticks.append(group_size)
        x_labels.append(f"{group_size - 99}-{group_size}")
        group_size *= 10  # Increase group size dynamically

    # Plot the scatter plot with dynamically adjusted group sizes
    plt.scatter(x_ticks, [sorted_frequency_data.get(f"{i + 1}-{i + group_size}", 0) for i, group_size in enumerate(x_ticks)], alpha=0.5, label='Word Frequency')
    plt.xscale('log')  # Set x-axis to logarithmic scale
    plt.xlabel('Word Rank (Grouped)')
    plt.ylabel('Word Frequency')
    plt.title('Word Frequencies for Multiple Languages')
    plt.legend()
    plt.show()
    

    


# Combine frequency dictionaries
def combine_freq_dicts(dictionaries):    
    combined = {}
    for language_dict in dictionaries:
        for word, count in language_dict.items():
            combined[word] = combined.get(word, 0) + count
    return combined

# Read data from files
def read_data():
    path_to_data = './../../data/multilingual/plain/'

    # Morisien
    with open(f'{path_to_data}mfe/freqdict-eng.mfe', 'r') as f:
        eng_mfe = json.load(f)
    with open(f'{path_to_data}mfe/freqdict-fra.mfe', 'r') as f:
        fra_mfe = json.load(f)

    # Combine frequency dictionaries
    mfe = combine_freq_dicts([eng_mfe, fra_mfe])

    # Kurmanji
    with open(f'{path_to_data}kmr/freqdict-eng.kmr', 'r') as f:
        eng_kmr = json.load(f)
    
    kmr = combine_freq_dicts([eng_kmr])

    # Vietnamese
    with open(f'{path_to_data}vie/freqdict-eng.vie', 'r') as f:
        eng_vie = json.load(f)
    with open(f'{path_to_data}vie/freqdict-fra.vie', 'r') as f:
        fra_vie = json.load(f)
    with open(f'{path_to_data}vie/freqdict-jap.vie', 'r') as f:
        jap_vie = json.load(f)
    with open(f'{path_to_data}vie/freqdict-zho.vie', 'r') as f:
        zho_vie = json.load(f)
    
    vie = combine_freq_dicts([eng_vie, fra_vie, jap_vie, zho_vie])

    # German
    with open(f'{path_to_data}deu/freqdict-eng.deu', 'r') as f:
        eng_deu = json.load(f)
    with open(f'{path_to_data}deu/freqdict-fra.deu', 'r') as f:
        fra_deu = json.load(f)
    
    deu = combine_freq_dicts([eng_deu, fra_deu])

    # Chinese
    with open(f'{path_to_data}zho/freqdict-eng.zho', 'r') as f:
        eng_zho = json.load(f)
    with open(f'{path_to_data}zho/freqdict-vie.zho', 'r') as f:
        vie_zho = json.load(f)
    
    zho = combine_freq_dicts([eng_zho, vie_zho])

    # English
    with open(f'{path_to_data}eng/freqdict-deu.eng', 'r') as f:
        deu_eng = json.load(f)
    with open(f'{path_to_data}eng/freqdict-fra.eng', 'r') as f:
        fra_eng = json.load(f)
    with open(f'{path_to_data}eng/freqdict-kmr.eng', 'r') as f:
        kmr_eng = json.load(f)
    with open(f'{path_to_data}eng/freqdict-mfe.eng', 'r') as f:
        mfe_eng = json.load(f)
    with open(f'{path_to_data}eng/freqdict-ukr.eng', 'r') as f:
        ukr_eng = json.load(f)
    with open(f'{path_to_data}eng/freqdict-vie.eng', 'r') as f:
        vie_eng = json.load(f)
    with open(f'{path_to_data}eng/freqdict-zho.eng', 'r') as f:
        zho_eng = json.load(f)
    
    eng = combine_freq_dicts([deu_eng, fra_eng, kmr_eng, mfe_eng, ukr_eng, vie_eng, zho_eng])

    
    #create_wordcloud_plots()
    """
    generate_word_cloud(mfe, 'Morisien')
    generate_word_cloud(kmr, 'Kurmanjî')
    generate_word_cloud(vie, 'Vietnamese')
    generate_word_cloud(deu, 'German')
    generate_word_cloud(zho, 'Chinese')
    generate_word_cloud(eng, 'English')
    
    """
    create_line_plots(mfe, "Morisien")
    """
    create_line_plots(kmr, "Kurmanjî")
    create_line_plots(vie, "Vietnamese")
    create_line_plots(deu, "German")
    create_line_plots(zho, "Chinese")
    create_line_plots(eng, "English")
    """
    
    
    


read_data()



sys.exit()

# Function to aggregate the data
def aggregate_data(data):
    agg_data = {}
    for freq in data.values():
        agg_data[freq] = agg_data.get(freq, 0) + 1
    return agg_data

# Aggregate the data
eng_mfe_agg = aggregate_data(eng_mfe)
fra_mfe_agg = aggregate_data(fra_mfe)

# Plot the data
"""
# NOTE: This is insufficient for very skewed data (such as one item appearing 15000 times, and 5000 items appearing once)
plt.bar(eng_mfe_agg.keys(), eng_mfe_agg.values(), alpha=0.5, label='Eng-Mfe')
plt.bar(fra_mfe_agg.keys(), fra_mfe_agg.values(), alpha=0.5, label='Fra-Mfe')

plt.xlabel('Frequency')
plt.ylabel('Count')
plt.title('Word Frequencies for Multiple Languages')
plt.legend()
plt.show()
"""

"""
# NOTE: Close, but no cigar!
# Plot the data with a logarithmic y-axis
plt.bar(eng_mfe_agg.keys(), eng_mfe_agg.values(), alpha=0.5, label='Eng-Mfe')
plt.bar(fra_mfe_agg.keys(), fra_mfe_agg.values(), alpha=0.5, label='Fra-Mfe')

plt.xlabel('Frequency')
plt.ylabel('Count (log scale)')
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.title('Word Frequencies for Multiple Languages')
plt.legend()
plt.show()
"""

"""
# NOTE: Everything grouped into bins (first 10 items not distingishable)
# Define bins for x-axis
bins = [1] + [10 * 10**i for i in range(4)]  # Bins: [1, 10, 100, 1000, 10000, 100000]

# Plot the data with a logarithmic y-axis and adjusted x-axis bins
plt.hist(eng_mfe_agg.keys(), bins=bins, alpha=0.5, label='Eng-Mfe', log=True, edgecolor='black')
plt.hist(fra_mfe_agg.keys(), bins=bins, alpha=0.5, label='Fra-Mfe', log=True, edgecolor='black')

plt.xscale('log')  # Set x-axis to logarithmic scale
plt.xticks(bins)  # Set x-axis ticks to the defined bins
plt.xlabel('Frequency')
plt.ylabel('Count (log scale)')
plt.title('Word Frequencies for Multiple Languages')
plt.legend()
plt.show()
"""

"""
# NOTE: Maybe bar-plot simply does not work for this? All values from 1-10 are the same height?
# Define bins for x-axis
bins = [i for i in range(1, 11)] + [10 * 10**i for i in range(1, 6)]  # Bins: [1, 2, ..., 10, 100, 1000, 10000, 100000]

# Plot the data with a logarithmic y-axis and adjusted x-axis bins
plt.hist(eng_mfe_agg.keys(), bins=bins, alpha=0.5, label='Eng-Mfe', log=True, edgecolor='black')
plt.hist(fra_mfe_agg.keys(), bins=bins, alpha=0.5, label='Fra-Mfe', log=True, edgecolor='black')

plt.xscale('log')  # Set x-axis to logarithmic scale
plt.xticks(bins)  # Set x-axis ticks to the defined bins
plt.xlabel('Frequency')
plt.ylabel('Count (log scale)')
plt.title('Word Frequencies for Multiple Languages')
plt.legend()
plt.show()
"""

# TODO: Switch to Scatter Plot
# TODO: Switch roles of x- and y-values

# Create scatter plot
plt.scatter(eng_mfe_agg.values(), eng_mfe_agg.keys(), alpha=0.5, label='Eng-Mfe')
plt.scatter(fra_mfe_agg.values(), fra_mfe_agg.keys(), alpha=0.5, label='Fra-Mfe')

plt.xscale('log')  # Set x-axis to logarithmic scale
plt.xlabel('Frequency')
plt.ylabel('Count (log scale)')
plt.title('Word Frequencies for Multiple Languages')
plt.legend()
plt.show()




sys.exit()

# Data for group x and y
data_x = {
    '1': 33,
    '2': 30,
    '3': 14,
    '4': 18,
    '5': 5
}
data_y = {
    '1': 71,
    '2': 71,
    '3': 87,
    '4': 83,
    '5': 96
}

# Extract classes and percentages for group x and y
classes = list(data_x.keys())
percentages_x = list(data_x.values())
percentages_y = list(data_y.values())

# Create the plot
plt.figure(figsize=(8, 6))

# Plot bars for group x
plt.bar(np.arange(len(classes)) - 0.2, percentages_x, width=0.4, color='salmon', label='Group X - Not Morisien')

# Plot bars for group y
plt.bar(np.arange(len(classes)) + 0.2, percentages_y, width=0.4, color='skyblue', label='Group Y - Morisien')

# Calculate and display proportions
for i, class_name in enumerate(classes):
    prop_x = percentages_x[i] / (percentages_x[i] + percentages_y[i]) * 100
    prop_y = percentages_y[i] / (percentages_x[i] + percentages_y[i]) * 100
    plt.text(i - 0.2, percentages_x[i] + 2, f'{prop_x:.1f}%', ha='center', color='black')
    plt.text(i + 0.2, percentages_y[i] + 2, f'{prop_y:.1f}%', ha='center', color='black')


plt.xlabel('Rarity Classes (Number of Occurences in Collected Data)')
plt.ylabel('Number of Observations')
plt.title('Comparison of proportions between Group X and Group Y')

# Show legend
plt.legend()

# Show plot
plt.xticks(np.arange(len(classes)), classes)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()