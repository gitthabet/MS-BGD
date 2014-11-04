# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 08:51:23 2014

@author: wei he
"""

import requests
from bs4 import BeautifulSoup
#import json
#import csv
#import numpy as np
import unicodedata as unic
import re
import urlparse

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

def unify(text):
    return unic.normalize('NFKD',text).encode('ascii','ignore')

def getTotalPages(link):
    firstRech = unify(getSoupFromUrl(link).select('span + span')[0].text)
    #pattern = re.compile("\d*\D+\d*\D+\d*\D+")
    pattern = re.compile('((\\d+))')
    totalAnnounces = int(pattern.findall(firstRech)[2][0])
    totalPages = (totalAnnounces/35) + 1
    return totalPages

def replace(text):
    return text.replace(' ','').replace('\n','').replace('\t','')

def getVersion(text):
    
    for version in versions:
        ver = re.compile(version)
        if re.search(ver, text.lower()):
            return version
    return ""

#def getCote2013():
    

def getVehicleDetail(allInfo, soupVeh, dep, catagory):
    fullTitle = soupVeh.find('h2').text.strip()
    version = getVersion(fullTitle)
    #price = soupVeh.find("span", {'class': 'price'}).text.replace(' ','').replace('€','')
    price = replace(soupVeh.find("span", {'class': 'price'}).text).replace('€','')
    year  = replace(soupVeh.find(text="Année-modèle :").find_next('td').text)
    km    = replace(soupVeh.find(text="Kilométrage :").find_next('td').text).replace('KM','')
    
    allInfo.append(dep+",")
    if catagory:
        allInfo.append("Professional"+",")
    else:
        allInfo.append("Personnal"+",")
    allInfo.append(version+",")
    allInfo.append(price+",")
    allInfo.append(year+",")
    allInfo.append(km+",")
    allInfo.append('\n')
    return allInfo
"""
version ( il y en a 3), ok
année, ok
kilométrage, ok
prix, ok
est ce que la voiture est vendue par un professionnel ou un particulier ok

Phone numbers, latitude, longtitude to find

"""
departments = ['ile_de_france','provence_alpes_cote_d_azur','aquitaine']
#departments = ['ile_de_france']
keyword = "Renault%20Captur"
versions = ['business', 'life', 'zen', 'intens', 'special', 'arizona', 'dci']

allInfo = []



resultVehs = open('resultVehs.csv', 'wb')
with resultVehs as csvfile:
    resultVehs.write('Department,Pro,Version,Price,Year,KM\n')
    for dep in departments:
        
        link = "http://www.leboncoin.fr/voitures/offres/" + dep + "?o=1&q="+ keyword
        totalPages = getTotalPages(link)
        
        for page in range (1, totalPages+1):
            link = "http://www.leboncoin.fr/voitures/offres/" + dep + "?o=" + str(page) + "&q="+ keyword
            
            #infoDiv = getSoupFromUrl(link).find_all("div", {'class': 'list-lbc'})
            infoDiv = getSoupFromUrl(link).find_all("div", {'class': 'lbc'})
            
            for line in infoDiv:
                infoA = line.find_parents("a")[0]
                linkVeh = urlparse.urljoin(link, infoA['href'])
                
                catagory = line.find('div', class_='category').text.strip()
                
                soupVeh = getSoupFromUrl(linkVeh)
                
                allInfo = getVehicleDetail(allInfo, soupVeh, dep, catagory)
    
    for eachLine in allInfo:
        resultVehs.write(eachLine)
    print "Csv file saved"
