# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys

#Fonction de téléchargement
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text)
    else:
        return None

#Fonction d'extraction du montant par habitant
def extract_data (page):
    lignes = page.find_all("tr")
    for ligne in lignes:
        td = ligne.find("td",text=re.compile("user(.*)", re.IGNORECASE))
        if td != None:
            print "Utilisateur: " + td.parent.select("td:nth-of-type(2)")[0].text
        td = None
        td = ligne.find("td",text=re.compile("karma(.*)", re.IGNORECASE))
        if td != None:
            print "karma: " + td.parent.select("td:nth-of-type(2)")[0].text
            break

for i in [1,2,3]:

#   On télécharge les données
    print ""
    print "DONNEES DE LA PAGE " + str(i)
    bs = get_page("https://news.ycombinator.com/news?p="+str(i))
    if bs == None:
        sys.exit("Request failed")

#   On extrait les liens vers les fiches utilisateurs
    users = None
    users = bs.find_all("a",attrs={"href":re.compile('user(.*)', re.IGNORECASE)})
    for user in users:
        user_page = get_page("https://news.ycombinator.com/"+user['href'])
        if user_page != None:
            extract_data(user_page)
        else: 
            print "La page " + user['href'] + " n'a pas pu être récupérée"

            