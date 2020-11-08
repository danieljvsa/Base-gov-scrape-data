# Base-gov-scrape-data
scrapedata from base.gov.pt

How to install Python(Windows):

Got to https://www.python.org/downloads/windows/ and download the Python 3.8.6

How to install PIP(Windows): 

python get-pip.py

How To Use this Program: 

python scrape_data.py dataStart dataLast

dataStart: first data to introduce,
dataLast: last data to introduce,
This turns to be the search period of time for crawler.

Libraries:


Datetime - pip install datetime,

Requests - pip install requsts,

=======
Datetime pip install datetime,
Requests - pip install requests,
>>>>>>> origin/main
BeautifulSoup (bs4) - pip install bs4,

lxml - pip install lxml;

Files Created:

contratos_dados.json - file with all contracts searched,
contratos_falhados - file with urls of contracts that failed to load.