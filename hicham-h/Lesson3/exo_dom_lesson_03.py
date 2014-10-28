# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import sys
import csv

#Fonction de téléchargement
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text,'html.parser')
    else:
        return None
        
#Recuperation de la page
bs = get_page("https://gist.github.com/paulmillr/2657075")
if bs == None:
    sys.exit("Request failed")
    
#On extrait le tableau qui nous intéresse
tableau = bs.find("table")

#On lit le tableau ligne par ligne
lignes = tableau.find_all("tr")
users = []
for ligne in lignes:
    user_href = ligne.find('td').find('a')
    if len(user_href) > 0:
        user = user_href.get('href').replace('https://github.com/','')
        encoded_object = get_page('https://api.github.com/users/'+user+'/repos')
        user_repos = json.loads(str(encoded_object))
        user_stars = 0
        for user_rep in user_repos:
            user_stars += user_rep['stargazers_count']
        users.append((user,user_stars/float(len(user_repos)) if len(user_repos)>0 else 0))

#Tri des resultats
users = sorted(users, key=lambda x:x[-1], reverse=True)

#Generation du fichier csv
myfile = open('resultats.csv', 'w')
wr = csv.writer(myfile, delimiter=';')
for user in users:
    wr.writerow(user)
