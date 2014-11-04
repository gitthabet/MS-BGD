import requests
from bs4 import BeuatifulSoup
import json
from googlemaps import GoogleMaps
from google.directions import GoogleDirections

# il fallait utiliser la Distance Matrix API


Villes = ["Caen","Paris","Lyon","Marseille","Lille"]

"""
for villeD in villes :
	for villeA in villes:
		ResultH = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin='+VilleD+"&destination="+VilleA"&key=AIzaSyDSpB6EGh2WJ4tOnpJpbs9TzgwfxcUoM3w')
		Item=[]
		if Result.ok:
			item = json.load(Result.content)

	for villeA in villes:
		ResultN = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin='+VilleD+"&destination="+VilleA"&key=AIzaSyDSpB6EGh2WJ4tOnpJpbs9TzgwfxcUoM3w&avoid=highways')
		Item=[]
		if Result.ok:
			item = json.load(Result.content)
"""

Result = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins=Caen|Paris|Lyon|Marseille|Lille&destinations=Caen|Paris|Lyon|Marseille|Lille&language=fr-FR&key=AIzaSyDSpB6EGh2WJ4tOnpJpbs9TzgwfxcUoM3w')	