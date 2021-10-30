import re
from bs4 import BeautifulSoup
import requests
data=requests.get('https://divar.ir/s/tehran')
data_soup=BeautifulSoup(data.text,'html.parser')
val=data_soup.find_all('div',attrs={"class":"kt-post-card__body"})
info=data_soup.find_all('div',attrs={"class":"kt-post-card__description"})
rows=str()
d=0
c=0
for row in val:
    rows=row.text
    if rows.find("توافقی") != -1:
        print(rows)