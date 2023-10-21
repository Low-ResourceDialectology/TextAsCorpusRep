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

from bs4 import BeautifulSoup

"""
tei_doc = './../data/German/Datasets/freedict-deu-eng-1.9-fd1.dictd/deu-eng/deu-eng.dict'
with open(tei_doc, 'r') as tei:
    soup = BeautifulSoup(tei, 'lxml')
"""

tei_doc = './../data/German/Datasets/freedict-deu-kur-0.2.2.dictd/deu-kur/deu-kur.dict'
with open(tei_doc, 'r') as tei:
    soup = BeautifulSoup(tei, 'lxml')

print(len(soup.contents))

print(soup.contents[0].name)




