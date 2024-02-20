from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
This method collects links until reaching the maximum number of links
By default it sets the max number on 1; whoch mean it will crawl only the given url
"""
def collect_links(url, max_links_num):
    all_links = [url]
    visited_links = set()

    while len(all_links) < max_links_num:
        cur_url = all_links.pop(0)
        visited_links.add(cur_url)
        links_on_page = get_links(cur_url)
        for link in links_on_page:
            if link not in visited_links:
                all_links.append(link)

    return all_links[:max_links_num]

"""
This method will be called from @collect_links to get all links on the target page
"""
def get_links(url):
    driver.get(url)
    links = driver.find_elements(By.TAG_NAME, "a")
    links_list = []
    for link in links:
        link_href = link.get_attribute("href")
        if link_href:
            links_list.append(link_href)
    return links_list

"""
This method write all extracted texts from the links, which was found
"""
def write_extracted_text(urls):
    with open("output.txt", "w", encoding="utf-8") as file:
        for url in urls:
            driver.get(url)
            title = driver.title
            content = driver.find_element(By.TAG_NAME, "body").text
            file.write(f"URL: {url}\n\n")
            file.write(f"Title: {title}\n\n")
            file.write(f"{content}\n\n")
            file.write("================================================================"+ "\n\n")


"""
This is the main method, alle crwaling method are called from here 
"""
def do_crawl(url, max_links_num=1):
    urls = collect_links(url, max_links_num)
    write_extracted_text(urls)
    driver.quit()

"""
This is a config-method for driver options
Crawling must be done without UI; so it will work more efficiently
"""
def setUp_driver():
    driver_options = Options()
    driver_options.add_argument("--headless")
    return driver_options


""" 
To run the application give your target url and the maximum number of links
for example:
do_crawl("https://www.exmaple.com", 20)
"""
driver = webdriver.Chrome(options=setUp_driver())
driver.implicitly_wait(10)
do_crawl("https://stackoverflow.com/questions/28090960/read-file-as-a-list-of-tuples")

