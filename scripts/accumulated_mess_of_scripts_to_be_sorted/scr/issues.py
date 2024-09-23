# Collection of issues encountered
# Also place for scripts and functions that might be useful later, 
# but would just clutter the other scripts right now.


# Kurmanji

# 2022AhmadiInterdialect 
###############################################################################
input_lines = []

# Okay... Reading xml files that are as basic as this one and which also contain duplicated ids is a pain in the butt!
"""
tree = etree.parse(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.kmr.eng.xml')
for graph in tree.xpath('//p'):
    print(graph.xpath('@id')[0])

root = tree.getroot()

topic = root.find(".//*[@id='1:2']").text
print(topic)
"""

"""
# Reading the data inside the xml
# file to a variable under the name 
# data
with open(path_kurmanji+'Datasets/2022AhmadiInterdialect/InterdialectCorpus/KMR-ENG/KMR-ENG.kmr.eng.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag 
# `unique`
b_unique = Bs_data.find_all('unique')
 
print(b_unique)
 
print(value)
"""

