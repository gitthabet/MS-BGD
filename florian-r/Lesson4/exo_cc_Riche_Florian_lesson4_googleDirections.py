import requests
import pprint
from bs4 import BeautifulSoup

import numpy as np

from pandas import DataFrame
import json

cities = ["Caen","Paris","Marseille","Lyon","Lille"]
print cities

Matrix_distance = DataFrame(np.zeros((len(cities),len(cities))),index=cities,columns=cities)
key = 'AIzaSyAxu2GEhusJPMwMBsQs6scZJlhmX39WGy0'
for depart in cities:
    for arrivee in cities:
        url="https://maps.googleapis.com/maps/api/directions/json?origin="+depart+",FR&destination="+arrivee+",FR&key="+key
                
        results = requests.get(url)
        json = results.json()
        steps = json['routes'][0]['legs']
        distance =0
        for step in steps: 
            distance = distance + step['distance']['value']
        Matrix_distance[depart][arrivee] = distance
        
print Matrix_distance