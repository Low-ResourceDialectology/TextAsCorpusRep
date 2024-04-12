
# Prepare the Data by moving/downloading into: /Flickr30k/data/

- Flickr30k-Original/images-and-descriptions.txt
from http://shannon.cs.illinois.edu/DenotationGraph/data/flickr30k.html
    → Use Regular Expressions to create json such that:
    {
        "1000092795.jpg":
        {
            "Two young guys with shaggy hair look at their hands while hanging out in the yard.",
            "Two young, White males are outside near many bushes.",
            "Two men in green shirts are standing in a yard.",
            "A man in a blue shirt standing in a garden.",
            "Two friends enjoy time spent together."
        },
        "10002456.jpg":
        {
            "Several men in hard hats are operating a giant pulley system.", ...
        }, ...
    }
    1. Remove first few lines
    2. " → \"
    3. \n    → ","
    4. jpg\n"," → jpg":["
    5. \n\n → "],\n
    6. ^ → "
    7. Remove , from last item
    8. Place } in last line
    9. Place { in first line}
    10. Rename to .json file
    11. \n""," → ":["
    12. Save
    - Images mapped to English


- Flickr30k-CNA/test & /train & /val
from https://zero.so.com/download.html
    → Flickr30k-CNA [Google Drive] [Baidu Drive] We provide the re-translated high-quality texts for Flickr30k.
    - Chinese


- Flickr30k-Images/Flickr30k-Multi30k/
from https://github.com/multi30k/dataset
    → git clone --recursive https://github.com/multi30k/dataset.git Flickr30k-Multi30k
    - English, German, French, Czech


- [!] Large download (4,4 GB)
- Flickr30k-Images/flickr30k-images.tar.gz
from https://zero.so.com/download.html
    → For Flickr30k-CNA, Please download the corresponding images from Flickr30k
        → http://shannon.cs.illinois.edu/DenotationGraph/data/index.html


- Flickr30k-Multi30k-uk/train.json & test_2016_flickr.json & test_2017_flickr.json & test_2017_mscoco.json & test_2018_flickr.json
from https://huggingface.co/datasets/turuta/Multi30k-uk/tree/main
    → Manual download or via python + huggingface's `from datasets import load_dataset`
    - Ukrainian



# Align across Languages

```
python3 language_aligner.py
```


