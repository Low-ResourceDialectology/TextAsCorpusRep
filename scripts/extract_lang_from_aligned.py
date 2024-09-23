import json
import os
from collections import defaultdict

# Language code mapping
lang_codes = {
    "ces": "Czech",
    "deu": "German",
    "eng": "English",
    "fra": "French",
    "mfe": "Mauritian",
    "ukr": "Ukrainian",
    "vie": "Vietnamese",
    "kob": "Kobani",
    "zho": "Chinese"
}

"""
    NLLB data
"""
def process_translations(input_file, output_dir, data_source):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Initialize dictionary to store aligned translations
    aligned_translations = defaultdict(lambda: defaultdict(list))

    # Process each entry in the JSON file
    for entry_id, entry_data in data.items():
        eng_sentence = entry_data['eng']['NLLB']
        for lang, lang_data in entry_data.items():
            if lang != 'eng':
                for translation in lang_data.values():
                    aligned_translations[('eng', lang)]['eng'].append(eng_sentence)
                    aligned_translations[('eng', lang)][lang].append(translation)
                    aligned_translations[(lang, 'eng')][lang].append(translation)
                    aligned_translations[(lang, 'eng')]['eng'].append(eng_sentence)

    # Write aligned translations to separate files
    for (src_lang, tgt_lang), translations in aligned_translations.items():
        src_dir = os.path.join(output_dir, lang_codes[src_lang], data_source)
        os.makedirs(src_dir, exist_ok=True)
        output_file = os.path.join(src_dir, f"{lang_codes[tgt_lang]}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in translations[src_lang]:
                f.write(line + '\n')

    print(f"Processing complete. Output files saved in {output_dir}")

# Input and output file paths for NLLB-data
# input_file = './../data/data_mtacr_nllb.json'
# output_dir = './../corpus'
# data_source = 'NLLB'
# process_translations(input_file, output_dir, data_source)

"""
    Flikr30k data
        → Seems like this would result in way to many (way too weak) alignments...
"""
# def process_annotations(input_file, output_dir, data_source):
#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)

#     # Read input JSON file
#     with open(input_file, 'r', encoding='utf-8') as f:
#         data = json.load(f)

#     # Initialize dictionaries to store annotations and alignment info
#     aligned_annotations = defaultdict(lambda: defaultdict(list))
#     alignment_info = defaultdict(dict)

#     # Process each entry in the JSON file
#     for entry_id, entry_data in data.items():
#         for annotator_key, lang_data in entry_data.items():
#             annotator_lang = annotator_key.split('_')[0]
#             annotator_source = annotator_key.split('_')[1]

#             for trans_id, translation in lang_data.items():
#                 aligned_annotations[lang][trans_id].append(translation)
#                 alignment_info[entry_id][f"{lang}_{trans_id}"] = translation

#     # Write alignment info to a JSON file
#     alignment_file = os.path.join(output_dir, "alignment_info_flikr30k.json")
#     with open(alignment_file, 'w', encoding='utf-8') as f:
#         json.dump(alignment_info, f, ensure_ascii=False, indent=2)

#     print(f"Processing complete. Output files saved in {output_dir}")

# # Input and output file paths for Flickr30k-data
# # input_file = './../data/flickr30k-aligned.json'
# # output_dir = './../corpus'
# # data_source = 'Flickr30k'
# # process_annotations(input_file, output_dir, data_source)

# input_file = './../data/Multi30k_data/multi30k-mtacr_mtacr.json'
# output_dir = './../corpus'
# data_source = 'Flickr30k'
# process_annotations(input_file, output_dir, data_source)

"""
    Flikr30k data (quantitative)
        → Seems like this would result in way to many (way too weak) alignments...
"""
def count_annotations(input_file, output_dir, data_source):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    number_images = 0
    number_eng = 0
    sents_eng = []
    number_ces = 0
    sents_ces = []
    number_deu = 0
    sents_deu = []
    number_fra = 0
    sents_fra = []
    number_ukr = 0
    sents_ukr = []
    number_zho = 0
    sents_zho = []
    number_zho_mtacr = 0
    sents_zho_mtacr = []
    number_kob_mtacr = 0
    sents_kob_mtacr = []
    number_mfe_mtacr = 0
    sents_mfe_mtacr = []
    number_vie_mtacr = 0
    sents_vie_mtacr = []

    # Initialize dictionaries to store annotations and alignment info
    #aligned_annotations = defaultdict(lambda: defaultdict(list))
    #alignment_info = defaultdict(dict)

    # Process each entry in the JSON file
    for entry_id, entry_data in data.items():
        number_images += 1
        for annotator_key, lang_data in entry_data.items():
            annotator_lang = annotator_key.split('_')[0]
            #annotator_source = annotator_key.split('_')[1]
            
            if annotator_lang == "eng":
                number_eng += 1
                sents_eng.append(lang_data)
            elif annotator_lang == "ces":
                number_ces += 1
                sents_ces.append(lang_data)
            elif annotator_lang == "deu":
                number_deu += 1
                sents_deu.append(lang_data)
            elif annotator_lang == "fra":
                number_fra += 1
                sents_fra.append(lang_data)
            elif annotator_lang == "ukr":
                number_ukr += 1
                sents_ukr.append(lang_data)
            elif annotator_lang == "zho":
                if '-' in annotator_key.split('_')[1]:
                    number_zho += 1
                    sents_zho.append(lang_data)
                else:
                    number_zho_mtacr += 1
                    sents_zho_mtacr.append(lang_data)
            elif annotator_lang == "kob":
                number_kob_mtacr += 1
                sents_kob_mtacr.append(lang_data)
            elif annotator_lang == "mfe":
                number_mfe_mtacr += 1
                sents_mfe_mtacr.append(lang_data)
            elif annotator_lang == "vie":
                number_vie_mtacr += 1
                sents_vie_mtacr.append(lang_data)
            else:
                print(f'Unrecognized language code: {annotator_lang}')

    # Write counts info to a TXT file
    count_file = os.path.join(output_dir, "annotation_counts.txt")
    # NOTE: Results in SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 0-1: truncated \UXXXXXXXX escape
    #count_file = f'{output_dir}/annotation_counts.txt'
    #with open(f'{output_dir}/annotation_counts.txt', 'w') as f:
    with open(count_file, 'w') as f:
        f.writelines(f'Images: {str(number_images)}\nEnglish: {str(number_eng)}\nCzech: {str(number_ces)}\nGerman: {str(number_deu)}\nFrench: {str(number_fra)}\nUkrainian: {str(number_ukr)}\nChinese: {str(number_zho)}\nChinese-MTACR: {str(number_zho_mtacr)}\nKobani-MTACR: {str(number_kob_mtacr)}\nMorisian-MTACR: {str(number_mfe_mtacr)}\nVietnamese-MTACR: {str(number_vie_mtacr)}')

    os.makedirs(f'{output_dir}/English/{data_source}', exist_ok=True)
    with open(f'{output_dir}/English/{data_source}/English.txt', 'w') as f:
        #f.writelines(sents_eng)
        for sent in sents_eng:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Czech/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Czech/{data_source}/Czech.txt', 'w') as f:
        #f.writelines(sents_ces)
        for sent in sents_ces:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/German/{data_source}', exist_ok=True)
    with open(f'{output_dir}/German/{data_source}/German.txt', 'w') as f:
        #f.writelines(sents_deu)
        for sent in sents_deu:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/French/{data_source}', exist_ok=True)
    with open(f'{output_dir}/French/{data_source}/French.txt', 'w') as f:
        #f.writelines(sents_fra)
        for sent in sents_fra:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Chinese/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Chinese/{data_source}/Chinese.txt', 'w') as f:
        #f.writelines(sents_zho)
        for sent in sents_zho:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Chinese/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Chinese/{data_source}MTACR/Chinese.txt', 'w') as f:
        #f.writelines(sents_zho_mtacr)
        for sent in sents_zho_mtacr:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Ukrainian/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Ukrainian/{data_source}/Ukrainian.txt', 'w') as f:
        #f.writelines(sents_ukr)
        for sent in sents_ukr:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Kobani/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Kobani/{data_source}MTACR/Kobani.txt', 'w') as f:
        #f.writelines(sents_kob_mtacr)
        for sent in sents_kob_mtacr:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Morisien/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Morisien/{data_source}MTACR/Morisien.txt', 'w') as f:
        #f.writelines(sents_mfe_mtacr)
        for sent in sents_mfe_mtacr:
            f.write(sent+'\n')

    os.makedirs(f'{output_dir}/Vietnamese/{data_source}', exist_ok=True)
    with open(f'{output_dir}/Vietnamese/{data_source}MTACR/Vietnamese.txt', 'w') as f:
        #f.writelines(sents_vie_mtacr)
        for sent in sents_vie_mtacr:
            f.write(sent+'\n')

# Input and output file paths for Flickr30k-data
# input_file = './../data/flickr30k-aligned.json'
# output_dir = './../corpus'
# data_source = 'Flickr30k'
# process_annotations(input_file, output_dir, data_source)

#input_file = './../data/Multi30k_data/multi30k-mtacr_mtacr.json'
input_file = './../data/alignments_mtacr_flikr30k.json'
output_dir = './../corpus'
data_source = 'Flikr30k'
count_annotations(input_file, output_dir, data_source)
