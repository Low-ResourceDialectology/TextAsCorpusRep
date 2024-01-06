
###########################################
# From clean.py                           #
# About working with HuggingFace datasets #
###########################################

# # Monolingual
# # Read data from json file (jsonl is just a "long json")
# # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
# input_lines = [json.loads(line)
#     for line in open(download_path+'data/cr/cr_train.jsonl', 'r', encoding='utf-8')]

# # The input is on the format:   {"input": "morisien_text_here", "target": ""}
# # Extracting the Morisien texts and store them in data
# data = [input_lines[index]['input']
#     for index in range(len(input_lines))]

# # Removing the first (empty) element from the list of text lines
# data.pop(0)

# #print(data[3]) # Debugging to check content

# # Write the Morisien text into a new file
# with open(transform_path+'mor.mor', 'w') as file:
#     for line in data:
#         file.write(line)
#         file.write('\n')

# # Bilingual - English
# # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
# #input_lines_dev = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
# #input_lines_test = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
# input_lines_train = [json.loads(line)
#         for line in open(download_path+'data/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
# #input_lines = input_lines_dev + input_lines_test + input_lines_train
# input_lines = input_lines_train

# # The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
# # Extracting the English and Morisien texts and store them in data
# data_eng_mor = [input_lines[index]['input']
#         for index in range(len(input_lines))]
# data_mor_eng = [input_lines[index]['target']
#         for index in range(len(input_lines))]

# # Write the English text (aligned with Morisien) into a new file
# with open(transform_path+'mor.eng', 'w') as file:
#     for line in data_eng_mor:
#         file.write(line)
#         file.write('\n')
# # Write the Morisien text (aligned with English) into a new file
# with open(transform_path+'eng.mor', 'w') as file:
#     for line in data_mor_eng:
#         file.write(line)
#         file.write('\n')

# # Bilingual - Fench 
# # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
# #input_lines_dev = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
# #input_lines_test = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
# input_lines_train = [json.loads(line)
#         for line in open(download_path+'data/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
# #input_lines = input_lines_dev + input_lines_test + input_lines_train
# input_lines = input_lines_train

# # The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
# # Extracting the English and Morisien texts and store them in data
# data_fra_mor = [input_lines[index]['input']
#         for index in range(len(input_lines))]
# data_mor_fra = [input_lines[index]['target']
#         for index in range(len(input_lines))]

# # Write the French text (aligned with Morisien) into a new file
# with open(transform_path+'mor.fra', 'w') as file:
#     for line in data_fra_mor:
#         file.write(line)
#         file.write('\n')
# # Write the Morisien text (aligned with French) into a new file
# with open(transform_path+'fra.mor', 'w') as file:
#     for line in data_mor_fra:
#         file.write(line)
#         file.write('\n')

# """
# Backup due to loading with huggingface instead of downloading files directly now
# # Monolingual
# # Read data from json file (jsonl is just a "long json")
# # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
# input_lines = [json.loads(line)
#     for line in open(download_path+'data/cr/cr_train.jsonl', 'r', encoding='utf-8')]

# # The input is on the format:   {"input": "morisien_text_here", "target": ""}
# # Extracting the Morisien texts and store them in data
# data = [input_lines[index]['input']
#     for index in range(len(input_lines))]

# # Removing the first (empty) element from the list of text lines
# data.pop(0)

# #print(data[3]) # Debugging to check content

# # Write the Morisien text into a new file
# with open(transform_path+'mor.mor', 'w') as file:
#     for line in data:
#         file.write(line)
#         file.write('\n')

# # Bilingual - English
# # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
# #input_lines_dev = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_dev.jsonl', 'r', encoding='utf-8')]
# #input_lines_test = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/en-cr/en-cr_test.jsonl', 'r', encoding='utf-8')]
# input_lines_train = [json.loads(line)
#         for line in open(download_path+'data/en-cr/en-cr_train.jsonl', 'r', encoding='utf-8')]
# #input_lines = input_lines_dev + input_lines_test + input_lines_train
# input_lines = input_lines_train

# # The input is on the format:   {"input": "english_text_here", "target": "morisien_text_here"}
# # Extracting the English and Morisien texts and store them in data
# data_eng_mor = [input_lines[index]['input']
#         for index in range(len(input_lines))]
# data_mor_eng = [input_lines[index]['target']
#         for index in range(len(input_lines))]

# # Write the English text (aligned with Morisien) into a new file
# with open(transform_path+'mor.eng', 'w') as file:
#     for line in data_eng_mor:
#         file.write(line)
#         file.write('\n')
# # Write the Morisien text (aligned with English) into a new file
# with open(transform_path+'eng.mor', 'w') as file:
#     for line in data_mor_eng:
#         file.write(line)
#         file.write('\n')

# # Bilingual - Fench 
# # Using list comprehension to solve this issue of invalid JSON files https://bobbyhadz.com/blog/python-jsondecodeerror-extra-data
# #input_lines_dev = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_dev.jsonl', 'r', encoding='utf-8')]
# #input_lines_test = [json.loads(line)
# #		for line in open(datasets_path+'2022DabreMorisienMT/data/fr-cr/fr-cr_test.jsonl', 'r', encoding='utf-8')]
# input_lines_train = [json.loads(line)
#         for line in open(download_path+'data/fr-cr/fr-cr_train.jsonl', 'r', encoding='utf-8')]
# #input_lines = input_lines_dev + input_lines_test + input_lines_train
# input_lines = input_lines_train

# # The input is on the format:   {"input": "french_text_here", "target": "morisien_text_here"}
# # Extracting the English and Morisien texts and store them in data
# data_fra_mor = [input_lines[index]['input']
#         for index in range(len(input_lines))]
# data_mor_fra = [input_lines[index]['target']
#         for index in range(len(input_lines))]

# # Write the French text (aligned with Morisien) into a new file
# with open(transform_path+'mor.fra', 'w') as file:
#     for line in data_fra_mor:
#         file.write(line)
#         file.write('\n')
# # Write the Morisien text (aligned with French) into a new file
# with open(transform_path+'fra.mor', 'w') as file:
#     for line in data_mor_fra:
#         file.write(line)
#         file.write('\n')
# """


##############################################################
# From clean.py                                              #
# Old code for sorting datasets from exploratory experiments #
# Prior to December 2023                                     #
##############################################################

# ===========================================
# MONOLINGUAL
# ===========================================
def sort_dataset(transform_path, sort_path):

    # Create directory if not existing
    util_ge.create_directory(sort_path)

    # For each file in the directory
    for filename in os.listdir(transform_path):
        # Combine the directory path with the filename
        text_file = os.path.join(transform_path, filename)
        
        # Checking if it is a file
        if os.path.isfile(text_file):
                    
            logging.debug(f'  Sorting: {text_file}')

            # Get file information
            f_basename = util_ge.get_basename(text_file)
            #logging.debug(f'    f_basename: {f_basename}')
            f_ending = util_ge.get_fileextension(text_file)
            #logging.debug(f'    f_ending: {f_ending}')
            #f_size = util_ge.get_filesize_b(text_file)
            #logging.debug(f'    f_size: {f_size}')

            #
            # Monolingual vs. Bilingual → Monolingual
            #
            if f_basename == f_ending:
                
                sort_path_mono = sort_path + 'Monolingual/'
                util_ge.create_directory(sort_path_mono)

                text_words = []
                text_sents = []

                text_data = util_ge.read_text_file(text_file)

                for line in text_data:

                    # Check if only a single word
                    if len(line.split(' ')) == 1:
                        text_words.append(line)
                    
                    # Otherwise multiple words
                    else:
                        text_sents.append(line)
                
                # Once all lines have been checked, write text (words & sents) to file

                # In case the data contained single words
                if len(text_words) > 0:

                    output_file_words = sort_path_mono + 'Words/'
                    util_ge.create_directory(output_file_words)
                    util_ge.write_text_file(output_file_words+f'{f_basename}.{f_ending}', text_words)

                # In case the data contained sentences
                if len(text_sents) > 0:

                    output_file_sents = sort_path_mono + 'Sentences/'
                    util_ge.create_directory(output_file_sents)
                    util_ge.write_text_file(output_file_sents+f'{f_basename}.{f_ending}', text_sents)
                # util_ge..write_text_file(output_file, text_words)
                # or
                # write_text_file_lines(output_file, text_words)
            
            #
            # Monolingual vs. Bilingual → Bilingual
            #
            elif f_basename != f_ending:

                logging.debug(f'  Sorting bilingual data for: {f_basename} and {f_ending}')
                sort_path_bili = sort_path + 'Bilingual/'
                util_ge.create_directory(sort_path_bili)

                text_words = []
                text_sents = []

                text_data = util_ge.read_text_file(text_file)

                for line in text_data:

                    # Check if only a single word
                    if len(line.split(' ')) == 1:
                        text_words.append(line)
                    
                    # Otherwise multiple words
                    else:
                        text_sents.append(line)
                
                # Once all lines have been checked, write text (words & sents) to file

                # In case the data contained single words
                if len(text_words) > 0:

                    output_file_words = sort_path_bili + 'Words/'
                    util_ge.create_directory(output_file_words)
                    util_ge.write_text_file(output_file_words+f'{f_basename}.{f_ending}', text_words)

                # In case the data contained sentences
                if len(text_sents) > 0:

                    output_file_sents = sort_path_bili + 'Sentences/'
                    util_ge.create_directory(output_file_sents)
                    util_ge.write_text_file(output_file_sents+f'{f_basename}.{f_ending}', text_sents)
                # util_ge..write_text_file(output_file, text_words)
                # or
                # write_text_file_lines(output_file, text_words)
            else:
                logging.debug(f'  Filename not properly formated: {text_file}')


# ===========================================
# Morisien 
# ===========================================
if '2022DabreMorisienMT' in dataset_list:

    transform_path = inputPath + '2022DabreMorisienMT/'
    sort_path = outputPath + '2022DabreMorisienMT/'
    logging.debug(f'  transform_path: {transform_path}')
    logging.debug(f'  sort_path: {sort_path}')
    sort_dataset(transform_path, sort_path)
    

# ===========================================
# Kurmanji 
# ===========================================
if '2022AhmadiInterdialect' in dataset_list:

    transform_path = inputPath + '2022AhmadiInterdialect/'
    sort_path = outputPath + '2022AhmadiInterdialect/'
    logging.debug(f'  transform_path: {transform_path}')
    logging.debug(f'  sort_path: {sort_path}')
    sort_dataset(transform_path, sort_path)
    

# ===========================================
# Vietnamese 
# ===========================================
if '2017LuongNMT' in dataset_list:

    transform_path = inputPath + '2017LuongNMT/'
    sort_path = outputPath + '2017LuongNMT/'
    logging.debug(f'  transform_path: {transform_path}')
    logging.debug(f'  sort_path: {sort_path}')
    sort_dataset(transform_path, sort_path)









###############################################################
# From clean.py                                               #
# Old code for cleaning datasets from exploratory experiments #
# Prior to December 2023                                      #
###############################################################

# ===========================================
# MONOLINGUAL
# ===========================================
def clean_monolingual(sort_path, clean_path):
    
    # Create directory if not existing
    util_ge.create_directory(clean_path)

    #
    # Check for monolingual data directories
    #
    if os.path.isdir(sort_path+'Monolingual'):
        
        #
        # Check for words data directories
        #
        if os.path.isdir(sort_path+'Monolingual/Words'):
            
            sort_path_mono_words = sort_path+'Monolingual/Words/'

            # For each file in the directory
            for filename in os.listdir(sort_path_mono_words):
                # Combine the directory path with the filename
                text_file = os.path.join(sort_path_mono_words, filename)
                
                # Checking if it is a file
                if os.path.isfile(text_file):
                            
                    #logging.debug(f'    Sorting: {text_file}')

                    f_basename = util_ge.get_basename(text_file)
                    f_ending = util_ge.get_fileending(text_file)

                    clean_path_mono_words = clean_path + 'Monolingual/Words/'
                    util_ge.create_directory(clean_path_mono_words)

                    text_words = []

                    text_data = util_ge.read_text_file(text_file)

                    for line in text_data:

                        # Only process non-empty lines
                        if util_ge.check_for_non_empty_string(line.replace("\n", "")):

                            # Remove punctuation at end of word
                            word = util_ge.remove_punctuation_end(line.replace("\n", ""))
                            text_words.append(word)

                        else:
                            pass
                    
                    util_ge.write_text_file_lines(clean_path_mono_words+f'{f_basename}.{f_ending}', text_words)

        #
        # Check for sentences data directories
        #
        if os.path.isdir(sort_path+'Monolingual/Sentences'):
            
            sort_path_mono_sents = sort_path+'Monolingual/Sentences/'

            # For each file in the directory
            for filename in os.listdir(sort_path_mono_sents):
                # Combine the directory path with the filename
                text_file = os.path.join(sort_path_mono_sents, filename)
                
                # Checking if it is a file
                if os.path.isfile(text_file):
                            
                    #logging.debug(f'    Sorting: {text_file}')

                    f_basename = util_ge.get_basename(text_file)
                    f_ending = util_ge.get_fileending(text_file)

                    clean_path_mono_sents = clean_path + 'Monolingual/Sentences/'
                    util_ge.create_directory(clean_path_mono_sents)

                    text_sents = []

                    text_data = util_ge.read_text_file(text_file)

                    for line in text_data:

                        # TODO: clean sentences
                        #sent = util_ge.remove_punctuation_end(line)
                        #text_sents.append(sent)
                        text_sents.append(line.replace("\n", ""))
                    
                    #print(f'Some lines from text_sents: {text_sents[0:3]}')
                    #print(f'target for cleaned sents: {clean_path_mono_sents}{f_basename}.{f_ending}')
                    
                    util_ge.write_text_file_lines(clean_path_mono_sents+f'{f_basename}.{f_ending}', text_sents)


# ===========================================
# BILINGUAL
# ===========================================
def clean_bilingual(sort_path, clean_path):
    
    # Create directory if not existing
    util_ge.create_directory(clean_path)

    #
    # Check for bilingual data directories
    #
    if os.path.isdir(sort_path+'Bilingual'):
            
        #
        # Check for words data directories
        #
        if os.path.isdir(sort_path+'Bilingual/Words'):
            
            sort_path_bili_words = sort_path+'Bilingual/Words/'

            # For each file in the directory
            for filename in os.listdir(sort_path_bili_words):
                # Combine the directory path with the filename
                text_file = os.path.join(sort_path_bili_words, filename)
                
                # Checking if it is a file
                if os.path.isfile(text_file):
                            
                    #logging.debug(f'    Sorting: {text_file}')

                    f_basename = util_ge.get_basename(text_file)
                    f_ending = util_ge.get_fileending(text_file)

                    clean_path_bili_words = clean_path + 'Bilingual/Words/'
                    util_ge.create_directory(clean_path_bili_words)

                    text_words = []

                    text_data = util_ge.read_text_file(text_file)

                    for line in text_data:

                        # Only process non-empty lines
                        if util_ge.check_for_non_empty_string(line.replace("\n", "")):

                            # Remove punctuation at end of word
                            #print(type(line)) → <class 'str'>
                            word = util_ge.remove_punctuation_end(line.replace("\n", ""))
                            text_words.append(word)
                    
                    util_ge.write_text_file_lines(clean_path_bili_words+f'{f_basename}.{f_ending}', text_words)

        #
        # Check for sentences data directories
        #
        if os.path.isdir(sort_path+'Bilingual/Sentences'):
            
            sort_path_bili_sents = sort_path+'Bilingual/Sentences/'

            # For each file in the directory
            for filename in os.listdir(sort_path_bili_sents):
                # Combine the directory path with the filename
                text_file = os.path.join(sort_path_bili_sents, filename)
                
                # Checking if it is a file
                if os.path.isfile(text_file):
                            
                    #logging.debug(f'    Sorting: {text_file}')

                    f_basename = util_ge.get_basename(text_file)
                    f_ending = util_ge.get_fileending(text_file)

                    clean_path_bili_sents = clean_path + 'Bilingual/Sentences/'
                    util_ge.create_directory(clean_path_bili_sents)

                    text_sents = []

                    text_data = util_ge.read_text_file(text_file)

                    for line in text_data:

                        # TODO: clean sentences
                        #sent = util_ge.remove_punctuation_end(line)
                        #text_sents.append(sent)
                        text_sents.append(line.replace("\n", ""))
                    
                    #print(f'Some lines from text_sents: {text_sents[0:3]}')
                    #print(f'target for cleaned sents: {clean_path_bili_sents}{f_basename}.{f_ending}')
                    util_ge.write_text_file_lines(clean_path_bili_sents+f'{f_basename}.{f_ending}', text_sents)


# ===========================================
# Morisien 
# ===========================================
if '2022DabreMorisienMT' in dataset_list:

    sort_path = inputPath + '2022DabreMorisienMT/'
    clean_path = outputPath + '2022DabreMorisienMT/'
    logging.debug(f'  sort_path: {sort_path}')
    logging.debug(f'  clean_path: {clean_path}')
    clean_monolingual(sort_path, clean_path)
    clean_bilingual(sort_path, clean_path)


# ===========================================
# Kurmanji 
# ===========================================
if '2022AhmadiInterdialect' in dataset_list:

    sort_path = inputPath + '2022AhmadiInterdialect/'
    clean_path = outputPath + '2022AhmadiInterdialect/'
    logging.debug(f'  sort_path: {sort_path}')
    logging.debug(f'  clean_path: {clean_path}')
    clean_monolingual(sort_path, clean_path)
    clean_bilingual(sort_path, clean_path)

# ===========================================
# Vietnamese 
# ===========================================
if '2017LuongNMT' in dataset_list:

    sort_path = inputPath + '2017LuongNMT/'
    clean_path = outputPath + '2017LuongNMT/'
    logging.debug(f'  sort_path: {sort_path}')
    logging.debug(f'  clean_path: {clean_path}')
    clean_monolingual(sort_path, clean_path)
    clean_bilingual(sort_path, clean_path)
