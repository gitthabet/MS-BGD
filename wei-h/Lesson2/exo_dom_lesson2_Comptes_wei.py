# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 20:40:58 2014

@author: Wei He
"""

import requests
from bs4 import BeautifulSoup

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

def getFonctionnementValues(year):
    soupComptes = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
    fonctionnements = soupComptes.find_all("td", {'class': 'libellepetit G'})
    print "\n********** Data in year", str(year), "**********\n"
    if fonctionnements:
        for fonctionnement in fonctionnements:
            tds  = fonctionnement.parent.find_all("td")
            if tds[3].text.find("TOTAL") != -1:
                print tds[3].text
                print "Euros par habitant   =", int(tds[1].text.replace(u'\xa0', u' ').replace(' ' ,''))
                print "Moyenne de la strate =", int(tds[2].text.replace(u'\xa0', u' ').replace(' ' ,'')), "\n"
    else:
        print "No data in year", str(year), "\n"
    
    return

for year in range(2009,2014):
    res = getFonctionnementValues(year)
