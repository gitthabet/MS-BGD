# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 21:37:04 2014

@author: louarradi
"""

import requests
from bs4 import BeautifulSoup

# Returns a soup object from a given url
def DataFrom(url):
    
    data = requests.get(url)
    if data.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(data.text)
    else:
    
        return None

def get_data_request(annee):
    
    Donnee_Paris = DataFrom('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(annee))
    
    Liste_Repere=['TOTAL DES PRODUITS DE FONCTIONNEMENT = A',
    'TOTAL DES CHARGES DE FONCTIONNEMENT = B',
    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
    

    for txt in  Liste_Repere :
        print txt
        Donnee = Donnee_Paris.find(text=txt)
        
        for line in Donnee.find_parents("tr"):
            l = line.find_all("td", class_="montantpetit G")
            print "Euros par habitant   : ", int(l[1].text.replace(u'\xa0', u' ').replace(' ' ,''))
            print "Moyenne de la strate : ", int(l[2].text.replace(u'\xa0', u' ').replace(' ' ,''))
    
    
def main():

    for annee in range (2010, 2014):
        get_data_request(annee)
if __name__ == '__main__':
  main()





