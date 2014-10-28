# -*- coding: utf-8 -*-

token = 'AIzaSyD0Je91FF7XuGcaTwNqH4apLq86DaM7fWc'
#key=token

import html5lib
import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd


# Donne l'objet soup correspondant à l'url spécifiée
def getSoupFromUrl(url) :
	webPage = requests.get(url)
	if webPage.status_code != 200 :
		print "Failure of the request on web page : " + url

	return BeautifulSoup(webPage.text, 'html5lib')

# Retourne la distance entre deux villes (avec autoroute)
def getDistanceBetweenTowns(departureTown, arrivalTown) :

	# Construction de la bonne url
	url = 'https://maps.googleapis.com/maps/api/directions/json?key='+token+'&origin=' + departureTown + '&destination=' + arrivalTown
	soup = getSoupFromUrl(url)

	# Conversion en Json puis extraction de la distance (en m)
	jsonObject = json.loads( soup.text )
	distance = jsonObject['routes'][0]['legs'][0]['distance']['value']

	return distance


# Création de la matrice en mode DataFrame
def createMatrixData(listOfTowns) :

	# Création d'une matrice vierge avec les bons indices et bonnes colonnes
	nbTowns = len(listOfTowns)
	emptyData = np.zeros( (nbTowns, nbTowns) )
	matrixData = pd.DataFrame(emptyData, index=listOfTowns, columns=listOfTowns)

	# Remplissage de la matrice 
	for departureTown in listOfTowns : 
		for arrivalTown in listOfTowns : 
			matrixData[departureTown][arrivalTown] = getDistanceBetweenTowns(departureTown, arrivalTown)
	
	return matrixData

distance = getDistanceBetweenTowns('Paris', 'Paris')
matrixData = createMatrixData( ['Caen', 'Paris', 'Marseille', 'Lyon', 'Lille'] )
print matrixData

