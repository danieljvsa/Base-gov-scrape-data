from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import json
import csv
from lxml import html



base_url = "http://www.base.gov.pt"



def url_gap(dateStart, dateLast, days):
    dateStart = datetime.strptime(dateStart, "%Y-%m-%d")
    dateStart_Date = dateStart + timedelta(days = days)     

    dateLast = datetime.strptime(dateLast, "%Y-%m-%d")
    dateLast_Date = dateLast + timedelta(days = days)   

    dateStart = dateStart_Date.strftime('%Y-%m-%d')
    dateLast = dateLast_Date.strftime('%Y-%m-%d')

    url = ("http://www.base.gov.pt/Base/pt/ResultadosPesquisa?type=contratos&query=texto%3D%26tipo%3D0%26tipocontrato%3D0%26cpv%3D%26numeroanuncio%3D%26aqinfo%3D%26adjudicante%3D%26adjudicataria%3D%26desdeprecocontrato_false%3D%26desdeprecocontrato%3D%26ateprecocontrato_false%3D%26ateprecocontrato%3D%26desdedatacontrato%3D"
    + dateStart + "%26atedatacontrato%3D" + dateLast 
    + "%26desdedatapublicacao%3D%26atedatapublicacao%3D%26desdeprazoexecucao%3D%26ateprazoexecucao%3D%26desdedatafecho%3D%26atedatafecho%3D%26desdeprecoefectivo_false%3D%26desdeprecoefectivo%3D%26ateprecoefectivo_false%3D%26ateprecoefectivo%3D%26pais%3D0%26distrito%3D0%26concelho%3D0"
    )
    
    return url, dateStart_Date, dateLast_Date, dateStart, dateLast
contract_urls =[]
def url_crawler(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    cruz = soup.find('span', class_="plusSign")
    contract_list = soup.find('table') 
    urls = contract_list.find_all('a') 
    for links in urls:
        if(links.getText() == '+'):
            contract_urls.append(links.get('href'))
    if(cruz):             
        next_page_partial = soup.find('div', class_='large-12 columns text-center pagination').find('p').find_all('a')[1]['href']
        next_page_url = base_url + next_page_partial
        print(next_page_url)
        url_crawler(next_page_url)
    else:
      file = open("contratos.txt", "w")
      file.write(str(contract_urls))
      file.close() 
      return contract_urls    
dateStart = "2020-10-05"
dateLast = "2020-10-06"
days = 0

url, dateStart_Date, dateLast_Date, dateStart, dateLast = url_gap(dateStart, dateLast, days)
contract_urls = url_crawler(url)
for items in contract_urls:
    print(str(contract_urls))