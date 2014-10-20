# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


def getAllMetricsForParis(annee):
    
    valeurs = []
    soupAlize = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(annee))
    # premier tableau    
    table = soupAlize.find_all("table", limit=3)	
    tableau = table[2]	
    # lignes						  
    bleu = tableau.find_all("tr", class_ = "bleu")		
    for l in range(3,25):
        ligne = bleu[l].find_all("td", class_ = "montantpetit G", limit = 3) 
        if len(ligne) != 0:
            # consider only Euros par hab and Moyenne strate
            for col in range(1,3):						  
                valeur = ligne[col].text						 
                val = int(valeur.replace(u'\xa0', u' ').replace(' ' ,''))
                valeurs.append(val)
    # remove R
    valeurs.pop(4)
    valeurs.pop(4)
    # organize values
    result = {}
    result['A'] = [valeurs[0],valeurs[1]]
    result['B'] = [valeurs[2],valeurs[3]]
    result['C'] = [valeurs[4],valeurs[5]]
    result['D'] = [valeurs[6],valeurs[7]]
         
    return result


def displayResults(result, annee):
    print "----------------------"
    print "TOTAL DES PRODUITS DE FONCTIONNEMENT: "  
    print "Euros par habitant :  " + str((result['A'])[0])
    print "Moyenne de la strate :" + str((result['A'])[1])
    print "TOTAL DES CHARGES DE FONCTIONNEMENT: "  
    print "Euros par habitant :  " + str((result['B'])[0])
    print "Moyenne de la strate :" + str((result['B'])[1])
    print "TOTAL DES RESSOURCES D'INVESTISSEMENT: "  
    print "Euros par habitant :  " + str((result['C'])[0])
    print "Moyenne de la strate :" + str((result['C'])[1])
    print "TOTAL DES EMPLOIS D'INVESTISSEMENT: "  
    print "Euros par habitant :  " + str((result['D'])[0])
    print "Moyenne de la strate :" + str((result['D'])[1])
    print "----------------------\n"
    return None
    
    
######### MAIN ####################    
for annee in range(2010,2014):
    Values = getAllMetricsForParis(annee)
    print "*** Resultat " + str(annee) +" ***"
    displayResults(Values, annee)