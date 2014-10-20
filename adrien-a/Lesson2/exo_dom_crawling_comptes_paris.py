# -*- coding: utf-8 -*-

import html5lib
import requests
from bs4 import BeautifulSoup

# Donne l'objet soup correspondant à l'url spécifiée
def getSoupFromUrl(url) :
	webPage = requests.get(url)
	if webPage.status_code != 200 :
		print "Failure of the request on web page : " + url

	return BeautifulSoup(webPage.text, 'html5lib')


def getDataForASpecificYear(year) :

	# Récupération du html en rapport avec l'année souhaitée 
	soup = getSoupFromUrl( "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(year) )

	# Obtention des colonnes lignes A, B, C et D et colonnes euro et strate
	keys = ['aEuro', 'aStrate', 'bEuro', 'bStrate', 'cEuro', 'cStrate', 'dEuro', 'dStrate']
	returnObject = {'year': year}
	text = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", "TOTAL DES CHARGES DE FONCTIONNEMENT = B", "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
	selector = ["td:nth-of-type(2)", "td:nth-of-type(3)"]

	for i in range(0, len(keys)) :
		returnObject[keys[i]] = int(soup.find_all('td', text=text[i/2])[0].parent.select(selector[i%2])[0].string.replace(' ', ''))
	
	return returnObject


data = [getDataForASpecificYear(i) for i in range(2010,2014)]