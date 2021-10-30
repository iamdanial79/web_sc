#web_scraping and use ml to guss car price
from os import replace
import re
from typing import final
from numpy.core.shape_base import block
import requests
import mysql.connector
from bs4 import BeautifulSoup
from sklearn import preprocessing
from sklearn import tree
a=list()
km_list=list()
year_list=list()
locate_list=list()
price_list=list()
final_list=list()
p_a=[]
data=list()
d_soup=[]
le=preprocessing.LabelEncoder()
for i in range(0,11):
    data.append(requests.get('https://bama.ir/car/all-brands/all-models/all-trims?hasprice=true&page=%i'))%(i)
    d_soup.append(BeautifulSoup(data.text,'html.parser'))
car_name=[]
km_car=[]
year_car=[]
locate_car=[]
price_car=[]
for soup in d_soup:
    car_name.append((soup.find_all('span',attrs={"class":"ad-title-span"})))
    km_car.append((soup.find_all('p',attrs={"class":"price hidden-xs"})))
    year_car.append((soup.find_all('span',attrs={"itemprop":"releaseDate"})))
    locate_car.append((soup.find_all('span',attrs={"class":"provice-mobile"})))
    price_car.append((soup.find_all('span',attrs={"itemprop":"price"})))
cars=str()
kms=str()
years=str()
locates=str()
prices=str()
e=0
e1=0
for row in car_name:
    cars=row.text
    cars=cars.replace('\n','')
    cars=cars.replace('\r','')
    e+=1
    if e%2==0:
        a.append(cars)



for row in km_car:
    kms=row.text
    valid=re.search(r'.*\d',kms)
    if valid==None:
        kms=0
        kms=float(kms)
        km_list.append(kms)
    else:
        kms=kms.split()
        kms=kms[1]
        kms=kms.replace(',','')
        kms=float(kms)
        km_list.append(kms)
    




for row in year_car:
    years=row.text
    years=years[:-1]
    e1+=1
    if e1%2==0:
        years=float(years)
        year_list.append(years)
    
for row in price_car:
    prices=row.text
    prices=prices.replace(',','')
    if prices.find('حواله')!=-1:
        prices=0
        prices=float(prices)
        price_list.append(prices)
    else:
        prices=float(prices)
        price_list.append(prices)

db=mysql.connector.connect(
    user='root',password='your pass',host='127.0.0.1',database='your db'
)
cursor=db.cursor()    

a1=[]
le.fit(a)
a=le.transform(a)
for r in a:
    a1.append(float(r))
x=[]
y=[]
for n in range(0,33):
    final_list.append((a1[n],km_list[n],year_list[n],price_list[n]))
    cursor.execute('INSERT IGNORE INTO your_table VALUES(\'%s\',\'%s\,\'%s,%i)'%(a[n],km_list[n],year_list[n],price_list[n]))
    db.commit()
for line in final_list:
    x.append(line[0:3])
    y.append(line[3])
print(x[0])
print(y[0])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y,sample_weight=None,check_input=True,X_idx_sorted="deprecated")
print("now we want to peredict the price")
model=input('enter the car:')
model=le.transform(model)
kilometer=input('enter the km:')
years_of_car=input('enter the ys of car:')
p_a.append((model,kilometer,years_of_car))
answer=clf.predict(p_a)
print(answer)