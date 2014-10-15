# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:04:09 2014

@author: Florian

"""
import requests
import pprint
from bs4 import BeautifulSoup


def GetReportFromYear(year):
    year=str(year)
    url= 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year    
    page= requests.get(url)
    prettypage= BeautifulSoup(page.text)
    report={}
    RowsToFind=['TOTAL DES PRODUITS DE FONCTIONNEMENT = A',
    'TOTAL DES CHARGES DE FONCTIONNEMENT = B',
    "TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
    "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
#    print prettypage
    for row in RowsToFind :
        ligne = prettypage.find(text=row).parent.parent
        cellules = ligne.contents
        #print cellules
        dataParHabitant= cellules[3].text
        dataParHabitant= int(dataParHabitant.replace(u'\xa0', u' ').replace(' ' ,''))

        dataParStrate = cellules[5].text
        dataParStrate= int(dataParStrate.replace(u'\xa0', u' ').replace(' ' ,''))

        #    
        
        print dataParHabitant
        print dataParStrate
        Result={}
        Result["EuroPrHab"]=dataParHabitant
        Result["MoyenneStrate"]=dataParStrate
        report[row]=Result
    return report
#    cellules = [prettypage.find_all(class_='montpetit G')
#    print cellules
    
    
#    print ligne
#    print page.text()    
#    print url
    

Reports={}
Reports["Report2013"]= GetReportFromYear('2013')
Reports["Report2012"]= GetReportFromYear('2012')
Reports["Report2011"]= GetReportFromYear('2011')
Reports["Report2010"]= GetReportFromYear('2010')
pprint.pprint(Reports)
#print BeautifulSoup(Reports).prettify