# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import sys

#Fonction d'extraction du montant par habitant
def extract_data (tableau, data):
    lignes = tableau.find_all("tr")
    ligne_trouvee = False
    for ligne in lignes:
        if ligne_trouvee is False:
#           On cherche la ligne "Total"            
            td = ligne.find("td",text=re.compile("TOTAL(.*)"+data+"($)", re.IGNORECASE))
            if td != None:
#               Ligne "Total" trouvée               
                ligne_trouvee = True
                print td.text + " -> " + td.parent.select("td:nth-of-type(2)")[0].text + "€/hab"
            else:
                continue
        else:
#           On cherche le détail du total            
            if ligne.find("td",class_="libellepetit G"):
                break
            else:
                td = ligne.find('td',attrs={'class':re.compile('libellepetit(.*)', re.IGNORECASE)})
                if td != None:
                    print td.text + " -> " + td.parent.select("td:nth-of-type(2)")[0].text + "€/hab"

#Téléchargement des données
response = requests.get("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013")
if response.status_code == 200:
   bs = BeautifulSoup(response.text)
else:
   sys.exit("Request failed")

#On extrait le tableau qui nous intéresse
tableau = None
tables = bs.find_all("table")
for table in tables:
    td = table.find("td",text=re.compile("ANALYSE(.*)FONDAMENTAUX", re.IGNORECASE))
    if td != None:
        tableau = table
        break

#On extrait les données du tableau
if tableau != None:
    extract_data(tableau, "A")
    extract_data(tableau, "B")
    extract_data(tableau, "C")    
    extract_data(tableau, "D")  
else:
    print "Tableau non trouvé"

            