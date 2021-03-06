# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 14:44:34 2014

@author: Sarra


e http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
récupérer les données A,B,C et D sur les colonnes Euros par habitant et par strate.
"""
import requests
from bs4 import BeautifulSoup
import re

# Returns a soup object from a given url
def getSoupFromUrl(url):
    
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        result.encoding = 'utf-8'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getMetricsABCDforParis(year):
    
    soupParis = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
    
    liste = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A","TOTAL DES CHARGES DE FONCTIONNEMENT = B",
             "TOTAL DES RESSOURCES D'INVESTISSEMENT = C","TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]

    print "==============================================="
    print "Année : ", year
    print "-------------"

    for txt in liste :
        print txt
        a_string = soupParis.find(text=txt)
        for line in a_string.find_parents("tr"):
            l = line.find_all("td", class_="montantpetit G")
            print "Euros par habitant   : ", int(l[1].text.replace(u'\xa0', u' ').replace(' ' ,''))
            print "Moyenne de la strate : ", int(l[2].text.replace(u'\xa0', u' ').replace(' ' ,''))
    
    
def main():

    for year in range (2010, 2014):
        getMetricsABCDforParis(year)

if __name__ == '__main__':
  main()