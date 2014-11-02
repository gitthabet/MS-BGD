# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 08:51:47 2014

@author: taigeo
"""

import requests
from bs4 import BeautifulSoup
import json


def getDistance(ville1,ville2):
   
    
    url='https://maps.googleapis.com/maps/api/directions/json?origin='+ville1+'&destination='+ville2+'&key=AIzaSyBv0WT6o0l9ywxmlOmVw2s4acoj_t57Up4'
    req2=requests.get(url)
    soup=BeautifulSoup(req2.text)
    print soup
    



getDistance('Caen','Paris')

