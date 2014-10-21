# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
# -*- coding: utf-8 -*-
"""

import requests

from bs4 import BeautifulSoup


# Returns a soup object from a given url


def get_soup_formule(url):
    result = requests.get(url)
    if result.status_code==200:
        print 'Requete OK'
        return BeautifulSoup(result.text)
    else:
        print 'Requete KO'
        return None


def get_chiffres(annee):
    year=str(annee)
    url="http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="+year
    soupAnnee = get_soup_formule(url)
    balises=soupAnnee.find_all("td", class_="montantpetit G")
    
    AparHabitant=balises[1].text
    AparHabitant=int(AparHabitant.replace(u'\xa0', u' ').replace(' ' ,''))
    AparStrate=balises[2].text
    AparStrate=int(AparStrate.replace(u'\xa0', u' ').replace(' ' ,''))
    
    BparHabitant=balises[4].text
    BparHabitant=int(BparHabitant.replace(u'\xa0', u' ').replace(' ' ,''))
    BparStrate=balises[5].text
    BparStrate=int(BparStrate.replace(u'\xa0', u' ').replace(' ' ,''))
    
    CparHabitant=balises[10].text
    CparHabitant=int(CparHabitant.replace(u'\xa0', u' ').replace(' ' ,''))
    CparStrate=balises[11].text
    CparStrate=int(CparStrate.replace(u'\xa0', u' ').replace(' ' ,''))
    
    DparHabitant=balises[12].text
    DparHabitant=int(DparHabitant.replace(u'\xa0', u' ').replace(' ' ,''))
    DparStrate=balises[13].text
    DparStrate=int(DparStrate.replace(u'\xa0', u' ').replace(' ' ,''))   
    
    
    print "AparHabitant " , AparHabitant
    print "BparHabitant " , BparHabitant
    print "CparHabitant " , CparHabitant
    print "DparHabitant ", DparHabitant
    
    print "AparStrate ", AparStrate
    print "BparStrate ", BparStrate
    print "CparStrate ", CparStrate
    print "DparStrate ", DparStrate
    
    return None
    
for annee in (2010,2011,2012,2013)   :
    print '*******************'    
    print annee 
    print '*******************'
    get_chiffres(annee)
   
   
