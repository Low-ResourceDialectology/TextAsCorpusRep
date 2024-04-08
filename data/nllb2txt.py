import re
import json
import io

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile

# http://etienned.github.io/posts/extract-text-from-word-docx-simply/

"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.iter(PARA):
        texts = [node.text
                 for node in paragraph.iter(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n'.join(paragraphs)


#input_t07 = './nllb/T07-kob-small_100.docx'
#output_t07 = './nllb/T07-kob-small_100-clean.txt'
input_t07 = './nllb/T07-kob-anchor.docx'
output_t07 = './nllb/T07-kob-anchor-clean.txt'
input_t07 = './nllb/T07-kob-small.docx'
output_t07 = './nllb/T07-kob-small-clean.txt'

text_from_docx_file = get_docx_text(input_t07)
# Open output file for writing
with open(output_t07, 'w') as output_file:
    output_file.write(text_from_docx_file)



def pdf2txt(input_file, output_file):
    # Open input file for reading
    with open(input_file, 'r') as input_file:
        lines = input_file.readlines()

    # Initialize variables
    current_sentence = ""
    output_text = ""

    # Iterate through the lines
    for line in lines:
        line = line.replace('','')
        # Check if the line starts with a 4-digit number followed by a colon and a space
        if re.match(r'^\d{4}:\s', line):
            # If the current sentence is not empty, add it to the output text
            if current_sentence:
                output_text += current_sentence.strip() + '\n'
            # Start a new sentence with the current line
            current_sentence = line.strip().replace('\n','')+' '
        else:
            # Append the current line to the current sentence
            current_sentence += line.replace('\n','')+' '

    # Add the last sentence to the output text
    if current_sentence:
        output_text += current_sentence.strip() + '\n'

    # Open output file for writing
    with open(output_file, 'w') as output_file:
        output_file.write(output_text)

# Input and output file paths
input_t01 = './nllb/T01-mfe-small.txt'
output_t01 = './nllb/T01-mfe-small-clean.txt'

input_t04 = './nllb/T04-vie-huge_622.txt'
output_t04 = './nllb/T04-vie-huge_622-clean.txt'

pdf2txt(input_t01, output_t01)
pdf2txt(input_t04, output_t04)



def json2txt(input_file, output_file, annotator_id):

    with open(input_file, 'r', encoding="unicode_escape") as in_file:
        input_lines = in_file.readlines()

    nllb_data = {}
    for text_line in input_lines:
        #print(text_line)
        cur_id = text_line.split('"id": "')[1].split('", "displayed_text')[0]
        if not cur_id.endswith(".html"):
            #print(cur_id)
            #print("===")
            cur_disp_text = text_line.split('"displayed_text": "')[1].split('", "label_annotations')[0]
            cur_disp_text_a = cur_disp_text.split('A. ')[1].split('<br>B. ')[0]
            cur_disp_text_b = cur_disp_text.split('<br>B. ')[1].split('<br>C. ')[0]
            cur_disp_text_c = cur_disp_text.split('<br>C. ')[1].split('", "label_annotations"')[0]

            cur_labels = text_line.split('"label_annotations": {"textbox_input": {"')[1].split('"}}, "span_annotations')[0]
            #print(cur_labels)
            #print(cur_labels.split('A:":')[1])
            cur_labels_a = cur_labels.split('": "')[1].split('", "对于B:')[0]#.encode().decode('unicode-escape')
            cur_labels_b = cur_labels.split('"对于B:": "')[1].split('", "对于C:"')[0]#.encode().decode('unicode-escape')
            cur_labels_c = cur_labels.split('"对于C:": "')[1].split('"}}, "span_annotations"')[0]#.encode().decode('unicode-escape')

            nllb_data[cur_disp_text_a] = {}
            #nllb_data[cur_disp_text_a]["zho"] = {}
            #nllb_data[cur_disp_text_a]["zho"][annotator_id] = cur_labels_a
            nllb_data[cur_disp_text_a]["new"] = cur_labels_a
            nllb_data[cur_disp_text_b] = {}
            #nllb_data[cur_disp_text_b]["zho"] = {}
            #nllb_data[cur_disp_text_b]["zho"][annotator_id] = cur_labels_b
            nllb_data[cur_disp_text_b]["new"] = cur_labels_b
            nllb_data[cur_disp_text_c] = {}
            #nllb_data[cur_disp_text_c]["zho"] = {}
            #nllb_data[cur_disp_text_c]["zho"][annotator_id] = cur_labels_c
            nllb_data[cur_disp_text_c]["new"]= cur_labels_c


    # Serializing json and write to file
    json_object = json.dumps(nllb_data, indent=4, ensure_ascii=False)
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
    #sorted_text_lines = sorted(text_lines.items(), key=lambda x:x[1])
    #converted_dict = dict(sorted_text_lines)

    #print(converted_dict)

    #with open(output_file, 'w') as text_file:
    #    for line in text_lines:
    #        text_file.write(line)

# Input and output file paths
input_t08 = './nllb/T08-zho-tiny_90.jsonl'
output_t08 = './nllb/T08-zho-tiny_90-clean.json'

input_t09 = './nllb/T09-zho-tiny_90.jsonl'
output_t09 = './nllb/T09-zho-tiny_90-clean.json'

input_t10 = './nllb/T10-zho-tiny.jsonl'
output_t10 = './nllb/T10-zho-tiny-clean.json'

json2txt(input_t08, output_t08, "T08")
json2txt(input_t09, output_t09, "T09")
json2txt(input_t10, output_t10, "T10")

