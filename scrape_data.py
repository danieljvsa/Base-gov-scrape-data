from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
import json




base_url = "http://www.base.gov.pt"

contract_data_list = [] 
contracts_failed = []
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
    number_contracts = soup.find('span', class_='defaultColor strong').get_text(strip=True)
    contract_list = soup.find('table') 
    urls = contract_list.find_all('a') 
    for links in urls:
        if(links.getText() == '+'):
          exception = url_errors(links.get('href'))
          #print(exception)
          if (exception == False):
            data_crawler(links.get('href'))
          else:
            contract_errors(links.get('href'))
    if (cruz and int(number_contracts) > 23): 
      next_page_partial = soup.find('div', class_='large-12 columns text-center pagination').find('p').find_all('a')[1]['href']
      next_page_url = base_url + next_page_partial
      print(next_page_url)
      url_crawler(next_page_url)
    else:
      contract_failed_file(contracts_failed)
      contract_data_file(contract_data_list)
      #finalFile = open("contratos_dados.txt", "w") 
      #finalFile.write(str(contract_data_list))
      #finalFile.close()  

def data_crawler(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  table = soup.find('table')
  row = table.find_all('tr')
  contract_data_raw = row[11].find_all('td')[0].get_text(strip=True)
  if(contract_data_raw == 'Data de celebração do contrato'):
    contract_data = row[11].find_all('td')[1].get_text(strip=True)
  else:
    contract_data = row[13].find_all('td')[1].get_text(strip=True)
  contract_type = row[1].find_all('td')[1].get_text(strip=True)
  contract_object_title = row[8].find_all('td')[0].get_text(strip=True)
  #print(contract_object_title)
  if(contract_object_title == "Objeto do Contrato"):
    contract_object = row[8].find_all('td')[1].get_text(strip=True)
    #print(contract_object_title)
  else:
    contract_object = row[10].find_all('td')[1].get_text(strip=True)
  contract_price_title = row[12].find_all('td')[0].get_text(strip=True)
  if(contract_price_title == "Preço contratual"):
    contract_price = row[12].find_all('td')[1].get_text(strip=True)
    #print(contract_object_title)
  else:
    contract_price = row[14].find_all('td')[1].get_text(strip=True)
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
  contract_dict['contract_data'] = contract_data
  contract_dict['contract_type'] = contract_type
  contract_dict['contract_object'] = contract_object
  contract_dict['contract_price'] = contract_price
  contract_dict['contracting_authority'] = contracting_authority
  contract_dict['hired_entity'] = hired_entity

  contract_data_list.append(contract_dict)
  return contract_data_list

def url_errors(url):
  tries = 0
  exception = True
  while(exception and tries < 15):
    try:
      html = requests.get(url, timeout = 60)
      if html.status_code == 500:
        tries = tries + 1 
        html.raise_for_status()
      exception = False
    except requests.exceptions.HTTPError:
      print('Error 500, Reconnecting...')
      print(tries)
      time.sleep(1)
      exception = True
    except requests.ConnectionError:
      print('Connection Error, Reconnecting...')
      time.sleep(30)
      exception = True
    except requests.RequestException:
      print('Handling RequstException, Reconnecing...')
      time.sleep(30)
      exception = True
    except requests.Timeout:
      print('TimeOut Error, Reconnecting...')
      time.sleep(30)
      exception = True
  return exception
def contract_errors(url):
  contracts_failed.append(url)
  return contracts_failed
def contract_data_file(contract_data_list):
  with open("contratos_dados.json", "w") as writeJSON:
    json.dump(contract_data_list, writeJSON, ensure_ascii=False, indent=4)
def contract_failed_file(contracts_failed):
  File = open("contratos_falhados.txt", "w") 
  File.write(str(contracts_failed))
  File.close()
dateStart = "2020-10-05"
dateLast = "2020-10-05"
days = 0

url, dateStart_Date, dateLast_Date, dateStart, dateLast = url_gap(dateStart, dateLast, days)
url_crawler(url)
