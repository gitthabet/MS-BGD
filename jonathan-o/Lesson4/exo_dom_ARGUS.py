# -*- coding: utf-8 -*-

"""

Created on Thu Oct 30 2014
    
@author: Ohayon

"""

import requests
import html5lib
import unicodedata as uni
from bs4 import BeautifulSoup
import json
import re
from pandas import Series, DataFrame

################################################################################################
# Some String manipulation functions

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')


################################################################################################
# Returns a soup object from a given url

def getSoupFromUrl(url):
    result = requests.get(url)
    
    if result.status_code == 200:
        return BeautifulSoup(result.text,"html5lib")
    
    else:
        print 'Request failed', url
        return None

#################################################################################################
#                                                                                               #
"""                                             ARGUS                                         """
#                                                                                               #
################################################################################################# 

##############################################################################################
# GetArgus 

def getArgus():
    soup = getSoupFromUrl('http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html')
    # find the info on cars
    balises_td = soup.find_all('td', class_="tdSD QuotMarque")
    List_of_car = [normalize(balise.select('a')[0].text) for balise in balises_td]
    balises_es = soup.find_all('td', class_="tdSD QuotNrj")
    Fuel_type = [normalize(balise.select('a')[0].text) for balise in balises_es]
    print Fuel_type
    Url_of_car = [normalize(balise.select('a')[0].get('href')) for balise in balises_td]
    
    Argus_data = []
    for i in range(0,len(List_of_car)):
        Argus_data.append([Fuel_type[i].upper() +' '+List_of_car[i] ,getValue(Url_of_car[i])])
    return Argus_data

##############################################################################################
# getValue

def getValue(part_URL):
    soup = getSoupFromUrl('http://www.lacentrale.fr/' + part_URL)
    balises_td = soup.find_all('span', class_="Result_Cote")
    return int(normalize(balises_td[0].text).replace(' ',''))

#createCSV for Argus
Argusdata = getArgus()
dataframeArgus = DataFrame(Argusdata,columns = ['Type','value'])
dataframeArgus.to_csv('Argus.csv')

