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

def url_crawler(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    cruz = soup.find('span', class_="plusSign")
    contract_list = soup.find('table') 
    urls = contract_list.find_all('a') 
    for links in urls:
        if(links.getText() == '+'):
            data_crawler(links.get('href'))
    if(cruz):             
        next_page_partial = soup.find('div', class_='large-12 columns text-center pagination').find('p').find_all('a')[1]['href']
        next_page_url = base_url + next_page_partial
        print(next_page_url)
        url_crawler(next_page_url)
    else:
      finalFile = open("contratos_dados.txt", "w") 
      finalFile.write(str(contract_data_list))
      finalFile.close()  
contract_data_list = [] 
def data_crawler(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  table = soup.find('table')
  row = table.find_all('tr')
  contract_data_raw = row[11].find_all('td')[1].get_text()
  if(contract_data_raw == '-' or contract_data_raw == 'O procedimento destina-se à satisfação de necessidades de várias Entidades'):
    contract_data = row[13].find_all('td')[1].get_text()
  else:
    contract_data = contract_data_raw
  contract_type = row[1].find_all('td')[1].get_text()
  contract_object_title = row[10].find_all('td')[0].get_text(strip=True)
  #print(contract_object_title)
  if(contract_object_title == "CPV"):
    contract_object = row[8].find_all('td')[1].get_text()
    #print(contract_object_title)
  else:
    contract_object = row[10].find_all('td')[1].get_text()
  contract_price_title = row[12].find_all('td')[0].get_text(strip=True)
  if(contract_price_title == "Preço contratual"):
    contract_price = row[12].find_all('td')[1].get_text()
    #print(contract_object_title)
  else:
    contract_price = row[14].find_all('td')[1].get_text()
  contracting_authority_title = row[6].find_all('td')[0].get_text(strip=True)
  if(contracting_authority_title == "Entidade adjudicante - Nome, NIF"):
    contracting_authority = row[6].find_all('td')[1].get_text(strip=True)
    #print(contract_object_title)
  else:
    contracting_authority = row[8].find_all('td')[1].get_text(strip=True)
  hired_entity_title = row[7].find_all('td')[0].get_text(strip=True)
  #print(hired_entity_title)
  if(hired_entity_title == "Entidade adjudicatária - Nome, NIF"):
    hired_entity = row[7].find_all('td')[1].get_text(strip=True)
    #print(contract_object_title)
  else:
    hired_entity = row[9].find_all('td')[1].get_text(strip=True)

  contract_dict = {} 
  contract_dict['Data de Celebração'] = contract_data
  contract_dict['Tipo de Contrato'] = contract_type
  contract_dict['Objeto do Contrato'] = contract_object
  contract_dict['Preço Contratual'] = contract_price
  contract_dict['Entidade adjudicante'] = contracting_authority
  contract_dict['Entidade adjudicatária'] = hired_entity

  contract_data_list.append(contract_dict)
  return contract_data_list



dateStart = "2020-10-05"
dateLast = "2020-10-06"
days = 0

url, dateStart_Date, dateLast_Date, dateStart, dateLast = url_gap(dateStart, dateLast, days)
url_crawler(url)
