from bs4 import BeautifulSoup
import requests
import mysql.connector
db=mysql.connector.connect(
    user='root',password='your pass',host='127.0.0.1',database='your db'
)
cursor=db.cursor()
d=requests.get('https://www.digikala.com/search/category-cars/')
d_soup=BeautifulSoup(d.text,'html.parser')
info=d_soup.find_all('div',attrs={"class":"c-product-box__title"})
cars=str()
a=input("enter your car:")
i=0

for car in info:
    cars=car.text
    if cars.find(a)!=-1 and i<20:
        cursor.execute('INSERT IGNORE INTO your_table VALUES(\'%s\')'%(cars))
        db.commit()
        i+=1

print('done')
