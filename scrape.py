import requests 
from bs4 import BeautifulSoup
import math

import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="companies"
)
mycursor = db.cursor()

def searchCompany(name):
    URL = "https://datacvr.virk.dk/data/visninger?soeg=" + parseName(name) + "&openFilter=true&kommune=null&region=null&antal_ansatte=null&virksomhedsstatus=normal%2Caktiv&virksomhedsform=null&virksomhedsmarkering=null&personrolle=null&oprettet=null&ophoert=null&branche=&type=virksomhed&sortering=navnasc&language=da"
    r = requests.get(URL)
    # Create a BeautifulSoup object
    html = r.text.replace("<br />", "")
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find('div', attrs = {'class':'name'})

    sortingDiv = soup.find('div', attrs = {'class':'sorteringsvalg virksomhed'})
    extractData(soup, name)
    numberOfPages = sortingDiv.label.input.next_sibling
    numberOfPages = numberOfPages.replace("(", "")
    numberOfPages = numberOfPages.replace(") ", "")
    numberOfPages = int(numberOfPages)
    if(numberOfPages > 10):
        for x in range(2, math.ceil(numberOfPages / 10)):
            print(x)
            URL = "https://datacvr.virk.dk/data/visninger?page=" + str(x) + "&soeg=" + parseName(name) + "&openFilter=true&kommune=null&region=null&antal_ansatte=null&virksomhedsstatus=normal%2Caktiv&virksomhedsform=null&virksomhedsmarkering=null&personrolle=null&oprettet=null&ophoert=null&branche=&type=virksomhed&sortering=navnasc&language=da"
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, "html.parser")
            extractData(soup, name)


def extractData(site, name):
    quotes=[]  # a list to store quotes
    table = site.find('div', attrs = {'id':'soegeresultat'})
    for row in table.find_all('div', attrs = {'class':'virk'}):
        if len(row) > 0:
            str(row).replace("<br>", " ")
            quote = {}
            quote["name"] = row.div.h2.a.text
            part = row.find("div", attrs = {"class" : "cvr"})
            quote["cvr"] = part.p.next_sibling.next_sibling.text
            part = row.find("p", attrs = {"class" : "address"})
            quote["address"] = part.text
            quotes.append(quote)
            
    insert(quotes, name)
            
def parseName(name):
    return name.replace(' ', '%20')

def insert(quote, name):
    sql = "INSERT INTO info (name, cvr, address, searchquery) VALUES (%s, %s, %s, %s)"
    for data in quote:
        val = (data["name"], data["cvr"], data["address"], name)
        mycursor.execute(sql, val)
    db.commit()

searchCompany("falck")
db.close()