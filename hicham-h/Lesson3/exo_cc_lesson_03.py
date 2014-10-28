# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import sys
import csv
import numpy as np

#Fonction de téléchargement
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text,'html.parser')
    else:
        return None

#Origines et destinations
origins = ['Caen','Paris','Marseille','Lyon','Lille']
destinations = origins

#Initialisation
result = np.zeros((5,5))
i=0
j=0

for origin in origins:
    j = 0
    for destination in destinations:
        if destination != origin:
#           Recuperation des donnees
            encoded_object = get_page("http://maps.googleapis.com/maps/api/directions/json?origin="+origin+"&destination="+destination)
            if encoded_object == None:
                sys.exit("Request failed")
            else:
#               Lecture de la reponse
                json_data = json.loads(str(encoded_object))
                routes = json_data['routes']
                for route in routes:
                    legs = route['legs']
                    for leg in legs:
                        distance = leg['distance']
#                       distance en km
                        result[i][j] = distance['value']/1000
#       Incrementation de l'indice de colonne
        j += 1
#   Incrementation de l'indice de colonne
    i += 1

#Affichage du resultat
print "Liste des villes: ", origins
print "Distance entre villes:"
print result
