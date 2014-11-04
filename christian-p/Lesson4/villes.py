# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 08:42:29 2014

@author: christian
"""

import numpy as np


villes = ['caen','paris','marseille','lyon','lille']

Matrix = [[]] 

from google.directions import GoogleDirections
gd = GoogleDirections('AIzaSyD8De9F85qtHsOl9vP27KHWbmZnnMW6CJ4')
res = gd.query('berlin','paris')

i = 0

for ville1 in villes:
    for ville2 in villes:
        Matrix.append([])
        if ville1 != ville2:
            res = gd.query(ville1, ville2)
            Matrix[i].append(res.distance)
            print "Distance ", ville1, ville2, "= ", res.distance
    i+=1
    
print Matrix