# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 15:39:29 2014

@author: Paco
"""

import requests as req
from bs4 import BeautifulSoup as bs


def main():
    for year in range(2009,2014):
        r = req.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
        soup = bs(r.text)
        count = 0    
        print "Annee: "+str(year)    
        for truc in soup.find_all('td', attrs={'class' : 'montantpetit G'}):
            if count==1:
                print "A (Total des produits de fonctionnement): "+truc.text
            if count==4:
                print "B (Total des charges de fonctionnement): "+truc.text
            if count==10:
                print "C (Total des ressources d'investissement): "+truc.text
            if count==13:
                print "D (Total des emplois d'investissement): "+truc.text
            count = count + 1    
            
if __name__ == '__main__':
    main()