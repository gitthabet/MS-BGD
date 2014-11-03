# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 08:44:33 2014

@author: wei he
"""

################################
# Using google directions API
################################

import requests
from bs4 import BeautifulSoup

from google.directions import GoogleDirections
gd = GoogleDirections('AIzaSyDW_ZDyMTvaAj2um4b_YqyfiMVjLRu56Eg')

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

#city1 = "caen"
city1 = "lyon"
city2 = "paris"

#url = 'http://maps.googleapis.com/maps/api/directions/xml?origin='+city1+'&destination='+city2+'&sensor=false'

url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+city1+'&destination='+city2+'&waypoints=Joplin,MO|Oklahoma+City,OK&key=AIzaSyDW_ZDyMTvaAj2um4b_YqyfiMVjLRu56Eg'
city = ["caen","paris","marseille","lyon","lille"]

soupCities = getSoupFromUrl(url)
print soupCities.findall("distance")
