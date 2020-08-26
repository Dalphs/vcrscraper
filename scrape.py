import requests 
from bs4 import BeautifulSoup

import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="companies"
)
mycursor = db.cursor()

def getData(name):
    URL = "https://datacvr.virk.dk/data/visninger?soeg=" + parseName(name) + "&oprettet=null&ophoert=null&branche=&type=virksomhed&language=da"
    r = requests.get(URL)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(r.content, "html.parser")

    table = soup.find('div', attrs = {'class':'name'})


    quotes=[]  # a list to store quotes
    table = soup.find('div', attrs = {'id':'soegeresultat'})
    for row in table.find_all('div', attrs = {'class':'virk'}):
        if len(row) > 0:
            quote = {}
            quote["name"] = row.div.h2.a.text
            part = row.find("div", attrs = {"class" : "cvr"})
            quote["cvr"] = part.p.next_sibling.next_sibling.text
            quotes.append(quote)
    insert(quotes)
            
def parseName(name):
    return name.replace(' ', '%20')

def insert(quote):
    sql = "INSERT INTO info (name, cvr) VALUES (%s, %s)"
    for data in quote:
        val = (data["name"], data["cvr"])
        mycursor.execute(sql, val)
    db.commit()

getData("enteraction")
db.close()