import re
import json
import io

# Input and output file paths
input_all = './nllb/T00-eng-entire.json'
output_all = './nllb/nllb-aligned.json'


def read_nllb_json(input_file):

    with open(input_file, 'r') as in_file:
        data = json.load(in_file)
    return data

nllb_all = read_nllb_json(input_all)
#print(type(nllb_all))
#print(nllb_all.keys())


def expand_nllb_json(current_data, new_file, language, translator_id):
    with open(new_file, 'r') as in_file:
        new_data = json.load(in_file)

    for key in new_data.keys():
        eng_text = new_data[key]["eng"]
        if "new" in new_data[key]:
            new_text = new_data[key]["new"]
            #print(key)
            for index in current_data.keys():
                #cur_text = current_data[index]["eng"]
                #if key == cur_text:
                # Find the corresponding English sentence from the new file inside the current_data to know its id
                if eng_text == current_data[index]["eng"]:
                    # Add the language and item combination if not exists for current translator id
                    if not language in current_data[index].keys():
                        current_data[index][language] = {}
                    if not translator_id in current_data[index][language].keys():
                        # Add the translated text from the current translator
                        current_data[index][language][translator_id] = new_text
    return current_data

nllb_all = expand_nllb_json(nllb_all, './nllb/T01-mfe-small-clean.json', "mfe", "T01")
nllb_all = expand_nllb_json(nllb_all, './nllb/T02-mfe-large_100.json', "mfe", "T02")

nllb_all = expand_nllb_json(nllb_all, './nllb/T03-vie-entire_1470.json', "vie", "T03")
nllb_all = expand_nllb_json(nllb_all, './nllb/T03-vie-large_480.json', "vie", "T03")
nllb_all = expand_nllb_json(nllb_all, './nllb/T04-vie-huge_622-clean.json', "vie", "T04")
nllb_all = expand_nllb_json(nllb_all, './nllb/T05-vie-entire_1765.json', "vie", "T05")
nllb_all = expand_nllb_json(nllb_all, './nllb/T05-vie-large_480.json', "vie", "T05")

nllb_all = expand_nllb_json(nllb_all, './nllb/T06-kob-small_144.json', "kob", "T06")
nllb_all = expand_nllb_json(nllb_all, './nllb/T07-kob-anchor-clean.json', "kob", "T07")
nllb_all = expand_nllb_json(nllb_all, './nllb/T07-kob-small-clean.json', "kob", "T07")

#file_list = ['./nllb/T08-zho-tiny_90-clean.json', './nllb/T09-zho-tiny_90-clean.json']
#for new_file in file_list:
#    nllb_all = expand_nllb_json(nllb_all, new_file)


def expand_nllb_json_zho(current_data, new_file, language, translator_id):

    #print("What?")
    #print(current_data["1"])
    #print("The?")

    with open(new_file, 'r') as in_file:
        new_data = json.load(in_file)

    for key in new_data.keys():
        eng_text = key
        new_text = new_data[key]["new"]
        #print(key)
        for index in current_data.keys():
            #cur_text = current_data[index]["eng"]
            #if key == cur_text:
            # Find the corresponding English sentence from the new file inside the current_data to know its id
            if eng_text == current_data[index]["eng"]:
                # Add the language and item combination if not exists for current translator id
                if not language in current_data[index].keys():
                    current_data[index][language] = {}
                if not translator_id in current_data[index][language].keys():
                    # Add the translated text from the current translator
                    current_data[index][language][translator_id] = new_text
    return current_data

nllb_all = expand_nllb_json_zho(nllb_all, './nllb/T08-zho-tiny_90-clean.json', "zho", "T08")
nllb_all = expand_nllb_json_zho(nllb_all, './nllb/T09-zho-tiny_90-clean.json', "zho", "T09")
nllb_all = expand_nllb_json_zho(nllb_all, './nllb/T10-zho-tiny-clean.json', "zho", "T10")


def save_nllb_json(data, output_file):
    
    # Serializing json and write to file
    json_object = json.dumps(data, indent=4, ensure_ascii=False)
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)

save_nllb_json(nllb_all, output_all)
