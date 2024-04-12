
# Aligning the data collected via the NLLB-Task and the Flikr30k-Task
- Get the data from the potato-task setup
- in /data/ create directories "flickr30k" and "nllb" for all the files


## 0. Rename all files for easy processing and to annonymize translator identities

## 1. Transform the data from the translators into simple .txt files 
```
cd MTACR/TextAsCorpusRep/scripts/
python3 nllb2txt.py
```

## 2. Transform all .txt data from the translators to .json files with the same structure 
```
python3 nllb2json.py
```

## 3. Combine data from all translators (and languages) into a single .json file 
```
python3 expand_nllb_json.py
```

## 4. Parse and combine data from all flikr30k annotation tasks (and languages) into a single .json file 
```
python3 flikr30k2json.py
```

## 5. Map the potato-task ids back to the original image filenames from flickr30k
```
python3 flikr30k2filenames.py
```

---

## 6. Get some statistics about the collected data 
```
python3 master_texter.py
```

