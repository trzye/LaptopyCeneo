# coding: utf-8

import requests
from tqdm import tqdm
import re
import sys
from bs4 import BeautifulSoup

def getCeneoSearch(product):
    return 'http://www.ceneo.pl/Laptopy_i_komputery;szukaj-' +  product.replace(' ', '+') + ';m2000;0112-0.htm'

file = open("notebooks.txt", "r")
notebooks = file.read()
soup = BeautifulSoup(notebooks, "lxml")
note_list = []

for notebook in soup.findAll("li"):
    text = notebook.text
    if(text.find('(')>-1):
        text = text[0:text.find("(")]
    if(text.find(',')>-1):
       note_list.extend(text.split(','))
    else:
       note_list.append(text)

notebook_list = []

for notebook in note_list:
    while(notebook.find('[') > -1):
        notebook = notebook[:notebook.find("[")] + notebook[notebook.find("]")+1:]
    if(notebook[0] == ' '):
        notebook = notebook[1:]
    notebook_list.append(notebook)

results = []

for notebook in tqdm(notebook_list):
    link = getCeneoSearch(notebook)
    request = requests.get(link)
    soup = BeautifulSoup(request.text, "lxml")
    all_results_page = soup.findAll("div", {"class" : "category-list-body js_category-list-body js_search-results"})[0]
    all_results = all_results_page.findAll("div", {"class" : "cat-prod-row js_category-list-item js_man-track-event"})
    if(len(all_results) > 0):
        price = all_results[0].findAll("span", {"class" : "price"})[0]
        value = price.findAll("span", {"class" : "value"})[0]
        penny = price.findAll("span", {"class" : "penny"})[0]
        result = {'model' : notebook, "gold" : value.text, "penny" : penny.text}
        results.append(result)

results.sort(key=lambda x: (x["gold"], x["penny"]))
for result in results:
    print(result["model"] + "\t" + result["gold"] + result["penny"])

    
