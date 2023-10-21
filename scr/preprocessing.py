# Python Script for preprocessing of text data of target languages
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
###############################################################################

"""
User-Guide:
 1. Prior to first start create a virtual environment names venvTextAsCorpusRep via
python -m venv venvTextAsCorpusRep

 2. Then activate this environment via
source venvTextAsCorpusRep/bin/activate

 3. Install the required python packages via
python -m pip install -r requirements.txt 

 4. Provide the collected text data in 
 - TextAsCorpusRep/data/TARGETLANGUAGE/Additional/
 - TextAsCorpusRep/data/TARGETLANGUAGE/Datasets/
 - TextAsCorpusRep/data/TARGETLANGUAGE/Urls/
 to then be transformed into 
 - TextAsCorpusRep/data/TARGETLANGUAGE/Corpus/
"""

import os, os.path
import nltk 
#import nltk.data
from nltk.corpus import PlaintextCorpusReader

from nltk import word_tokenize
nltk.data.path.append("/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/nltk_data/")

""" # Works with data downloaded with nltk-downloader
from nltk.corpus import brown
nltk.data.path.append("/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/nltk_data/")
brown.words()
print(brown.words()[1])
"""

""" # Own data
corpus_root = '/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Kurmanji/Datasets/2023AhmadiSouthernCorpus/'
corpus = PlaintextCorpusReader(corpus_root, '.*', encoding='latin1')

print("Words")
for index in range(0,20):
    print(corpus.words()[index])

    # BREAKS because forsome reason the resource "punkt" is not found...
print("Sentences")
for index in range(0,20):
    print(corpus.sents()[index])
# corpus.paras()
"""

""" # Works
nltk.data.path.append("/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Kurmanji/Datasets/2023AhmadiSouthernCorpus/")
#kurmanji_corpus = nltk.data.load('NorthernKurdish-latn_train.txt', format='raw')
kurmanji_corpus = nltk.data.load('NorthernKurdish-latn_train.txt', format='text')
print("Sentences")
for index in range(0,20):
    print(kurmanji_corpus[index])
print(len(kurmanji_corpus))
"""

path_chinese = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Chinese/"
nltk.data.path.append(path_chinese)
path_english = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/English/"
nltk.data.path.append(path_english)
path_french = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/French/"
nltk.data.path.append(path_french)
path_german = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/German/"
nltk.data.path.append(path_german)
path_kobani = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Kobani/"
nltk.data.path.append(path_kobani)
path_kurmanji = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Kurmanji/"
nltk.data.path.append(path_kurmanji)
path_morisien = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Morisien/"
nltk.data.path.append(path_morisien)
path_ukrainian = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Ukrainian/"
nltk.data.path.append(path_ukrainian)
path_vietnamese = "/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/TextAsCorpusRep/data/Vietnamese/"
nltk.data.path.append(path_vietnamese)


# Morisien #
############
print("# ==== # Morisien # ==== #")
mor_corpus_01 = nltk.data.load('Input/2012_Police-Michel_Carpooran_Florigny_Gramer_Kreol_Morisien.txt', format='text')
mor_corpus_02 = nltk.data.load('Input/2012_Rajki_deChazal_Diksyoner_Kreol_Morisyen.txt', format='text')
mor_corpus = mor_corpus_01 + mor_corpus_02

print("Morisien Corpus is: "+str(type(mor_corpus))+" and the number is "+str(len(mor_corpus)))
for index in range(100,105):
    print(mor_corpus[index])

mor_tokens = word_tokenize(mor_corpus)
print("Morisien Tokens are: "+str(type(mor_tokens))+" and their number is "+str(len(mor_tokens)))
for index in range(100,105):
    print(mor_tokens[index])

mor_words = [w.lower() for w in mor_tokens]
print("Morisien Words are: "+str(type(mor_words))+" and their number is "+str(len(mor_words)))
for index in range(100,105):
    print(mor_words[index])

mor_vocab = sorted(set(mor_words))
print("Morisien Vocab is: "+str(type(mor_vocab))+" and their number is "+str(len(mor_vocab)))
for index in range(100,105):
    print(mor_vocab[index])

# Vietnamese #
##############
print("# ==== # Vietnamese # ==== #")
vie_corpus = nltk.data.load('Datasets/2022NgoSynthetic/en-vi/tst2012.vi', format='text')

print("Vietnamese Corpus is: "+str(type(vie_corpus))+" and the number is "+str(len(vie_corpus)))
for index in range(100,105):
    print(vie_corpus[index])

vie_tokens = word_tokenize(vie_corpus)
print("Vietnamese Tokens are: "+str(type(vie_tokens))+" and their number is "+str(len(vie_tokens)))
for index in range(100,105):
    print(vie_tokens[index])

vie_words = [w.lower() for w in vie_tokens]
print("Vietnamese Words are: "+str(type(vie_words))+" and their number is "+str(len(vie_words)))
for index in range(100,105):
    print(vie_words[index])

vie_vocab = sorted(set(vie_words))
print("Vietnamese Vocab is: "+str(type(vie_vocab))+" and their number is "+str(len(vie_vocab)))
for index in range(100,105):
    print(vie_vocab[index])

#path_kurmanji = 'Kurmanji/Corpus/NorthernKurdish-latn_train.txt'
#path_kurmanji = 'NorthernKurdish-latn_train.txt'

#nltk.download()
# Change Download-Directory to: /media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/nltk_data

#print(nltk.data.path)
#nltk.data.path.append("/media/QereqolaXebate/CrazyProjects/DDLitLab-TextAsCorpusRep/data/")
#print(nltk.data.path)

#nltk.data.load(path_kurmanji, format='raw')






# NLTK Tutorial Book
# https://www.nltk.org/book/ch03.html