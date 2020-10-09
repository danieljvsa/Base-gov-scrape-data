import requests
from bs4 import BeautifulSoup
import bs4 as bs
import time
import csv
import urllib.request
import pandas as pd
import json

url = 'http://www.base.gov.pt/Base/pt/Pesquisa/Contrato?a=5992585'
headers= {'User-Agent': 'Mozilla/5.0'}
response = urllib.request.urlopen(url).read()


soup = bs.BeautifulSoup(response, 'lxml')

stat_table = soup.select_one('#pesquisaInci > div > div > ss3:nth-child(2) > div > table:nth-child(3)')

table_rows = stat_table.find_all('tr')
new_table = pd.DataFrame(columns=range(0,2), index = [0])


def tableDataText(table):       
    rows = []
    trs = table_rows
    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
    return rows

list_table = tableDataText(stat_table)
with open('contrato.json', 'w', encoding='utf-8') as json_file:
    json.dump(list_table, json_file, sort_keys=True, ensure_ascii=False, indent=4)
      
            
        