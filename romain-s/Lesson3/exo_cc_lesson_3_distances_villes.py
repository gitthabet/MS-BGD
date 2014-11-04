# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 08:44:07 2014

@author: Romain
"""

import requests
import pandas as pd

# list of cities and API key
villes=['Caen','Paris','Marseille','Lyon','Lille']
api_key = 'AIzaSyAF1DGjNqXDpsik9pSAARs35PVnxJkL744'

# initilisation of result matrix
distmatrix = pd.DataFrame(0,index=villes,columns=villes)
distmatrix.loc['Caen','Lyon']

# loop
for origin in villes:
    for destination in villes:
        result = requests.get('https://maps.googleapis.com/maps/api/directions/json?origin=' + origin + '&destination=' + destination +'&key=' + api_key).json()
        distmatrix.loc[origin, destination] = result['routes'][0]['legs'][0]['distance']['value']/1000.0

# result  
distmatrix