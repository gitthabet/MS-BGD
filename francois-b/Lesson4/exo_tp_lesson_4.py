# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 08:43:18 2014

@author: Paco
"""

import requests as req

'''
--------------------------------------------------------------
Documentation : 
https://developers.google.com/maps/documentation/directions/
--------------------------------------------------------------
'''

# token api google direction
token_api = ""

# original vector
city_vector = ['Caen','Paris','Marseille','Lyon','Lille']

# final matrix
distance_matrix = [[0 for x in xrange(5)] for x in xrange(5)] 

for i in range(0,len(city_vector)):
    for j in range(0,len(city_vector)):
   
        origin_city = city_vector[i]
        destination_city = city_vector[j]       

        r = req.get('https://maps.googleapis.com/maps/api/directions/json?origin='+origin_city+'&destination='+destination_city+'&key='+token_api)
        rep = r.json()
        
        # get global distance
        value =  rep['routes'][0]['legs'][0]['distance']['text']

        if origin_city is destination_city:
            value = '0'
            
        print origin_city + " " + destination_city + " " + value        
            
        # fill the matrix    
        distance_matrix[i][j]=value

print distance_matrix