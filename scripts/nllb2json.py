import re
import json
import io

# Input and output file paths
input_t00 = './../data/nllb/T00-eng-entire.txt'
output_t00 = './../data/nllb/T00-eng-entire.json'


def nllb2json(input_file, output_file):

    with open(input_file, 'r') as in_file:
        input_lines = in_file.readlines()

    index = 0
    nllb_data = {}
    for text_line in input_lines:
        index = index + 1 
        cur_index = str(index).zfill(4)
        cur_text = text_line
        
        nllb_data[cur_index] = {}
        nllb_data[cur_index]["eng"] = {}
        nllb_data[cur_index]["eng"]["NLLB"] = cur_text.replace('\n','')

    # Serializing json and write to file
    json_object = json.dumps(nllb_data, indent=4, ensure_ascii=False)
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)

nllb2json(input_t00, output_t00)



def txt2json(file_name, eng_file):

    with open(f'{file_name}.txt', 'r') as in_file:
        input_lines = in_file.readlines()
    
    with open(f'{eng_file}.txt', 'r') as in_file:
        eng_lines = in_file.readlines()
    
    nllb_data = {}
    for text_line in eng_lines:
        index = text_line[:4] 
        cur_text = text_line[6:]
        
        nllb_data[index] = {}
        nllb_data[index]["eng"] = {}
        nllb_data[index]["eng"]["NLLB"] = cur_text.replace('\n','')

    for new_line in input_lines:
        index = new_line[:4]
        #print(f'index:{index}')
        cur_text = new_line[6:]
        
        nllb_data[index]["new"] = cur_text.replace('\n','').strip()
        

    # Serializing json and write to file
    json_object = json.dumps(nllb_data, indent=4, ensure_ascii=False)
    with open(f'{file_name}.json', "w", encoding="utf-8") as outfile:
        outfile.write(json_object)


input_files_anchor = ['./../data/nllb/T07-kob-anchor-clean']
for input_file in input_files_anchor:
    txt2json(input_file, './../data/nllb/mtacr-translator-splits/anchor_1')

input_files_small_custom = ['./../data/nllb/T07-kob-small-clean']
for input_file in input_files_small_custom:
    txt2json(input_file, './../data/nllb/mtacr-translator-splits/small-pascaline_2')

input_files_small = ['./../data/nllb/T01-mfe-small-clean', './../data/nllb/T06-kob-small_144']
for input_file in input_files_small:
    txt2json(input_file, './../data/nllb/mtacr-translator-splits/small_1')


input_files_large = ['./../data/nllb/T02-mfe-large_100', './../data/nllb/T03-vie-large_480', './../data/nllb/T05-vie-large_480']
for input_file in input_files_large:
    txt2json(input_file, './../data/nllb/mtacr-translator-splits/large_1')

txt2json('./../data/nllb/T04-vie-huge_622-clean', './../data/nllb/mtacr-translator-splits/T04-vie-14k_words')

input_files_entire = ['./../data/nllb/T05-vie-entire_1765']
for input_file in input_files_large:
    txt2json(input_file, './../data/nllb/mtacr-translator-splits/large_1')

txt2json('./../data/nllb/T03-vie-entire_1470', './../data/nllb/mtacr-translator-splits/entire-lara')
txt2json('./../data/nllb/T05-vie-entire_1765', './../data/nllb/mtacr-translator-splits/T05-vie-entire_part_2')
