"""Using the Google directions API"""
# -*- coding: iso-8859-15 -*-
from google.directions import GoogleDirections
gd = GoogleDirections('AIzaSyC7d9cBib4H734ta4lHc0JEQ7LMIdm3njQ')
villes = ['Caen', 'Paris', 'Marseille', 'Lyon', 'Lille']
for v1 in villes:
    for v2 in villes:
        if v2 not in [v1]:
    		res = gd.query(v1, v2)
    		print v1+' to '+v2 + '=' +str(res.distance)

# res.distance

#[x for x in my_list if not x.startswith('#')]
#[for a in villes if not a in ['Paris']: print a]

# for a in villes:
#     if a not in ['paris']:
#     	print a