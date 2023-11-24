# -*- coding: utf-8 -*-
# Python Script for preprocessing collected text data
# 
# Authors: Christian "Doofnase" Schuler, 
#          Deepesah "Tania" Saurty, 
#          Tramy Thi "Myy" Tran, 
#          Raman "Brudi" Ahmad, 
#          Anran "Echo" Wang
################################################################################

import fasttext
from huggingface_hub import hf_hub_download

# download model
## cache_dir: path to the folder where the downloaded model will be stored/cached.
model_path = hf_hub_download(repo_id="cis-lmu/glotlid", filename="model.bin", cache_dir=None)

# load the model
model = fasttext.load_model(model_path)

# predict language label (call this function as many times as needed)
prediction01 = model.predict("Li herêmên Bakur û Rêhilatê Sûriyeyê qedexeya derketina derve ji ber şewba vîrûsa koronayê ji 23'ê Adarê ve dewam dike.")
prediction02 = model.predict("Di encamê de kuştî û birîndarên çeteyan nehat zelalkirin.") #"Bonzour, mo apel Tania. Mo p gagn fin. Mo res gagn fin mem mwa.")
prediction03 = model.predict("Dewleta Tirk a dagirker di 15'ê Nîsanê de êrişa hewayî bir ser qada Zînî Wertê û kampa penaberan a Mexmûrê. Li Mexmûrê 3 jin şehîd bûn.") #xín chao, bạn. Bạn khỏe không??? Hôm này em là mùng.")
prediction04 = model.predict("Bonzour, mo apel Tania. Mo p gagn fin. Mo res gagn fin mem mwa. Xín chao, bạn. Bạn khỏe không??? Hôm này em là mùng. Dewleta Tirk a dagirker di 15'ê Nîsanê de êrişa hewayî bir ser qada Zînî Wertê û kampa penaberan a Mexmûrê. Li Mexmûrê 3 jin şehîd bûn.") #xín chao, bạn. Bạn khỏe không??? Hôm này em là mùng.")
prediction05 = model.predict("Bonzour, mo apel Tania. Mo p gagn fin. Mo res gagn fin mem mwa.")
prediction06 = model.predict("Xín chao, bạn. Bạn khỏe không??? Hôm này em là mùng.")

print("This is my prediction: "+str(prediction01))
print("This is my prediction: "+str(prediction02))
print("This is my prediction: "+str(prediction03))
print("This is my prediction: "+str(prediction04))
print("This is my prediction: "+str(prediction05))
print("This is my prediction: "+str(prediction06))