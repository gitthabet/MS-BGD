# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 14:19:06 2014

@author: Florian
"""

import requests
import json
from bs4 import BeautifulSoup
from pandas import DataFrame
import re

'''
 contenir les infos suivantes : 
 version ( il y en a 3), 
 année, 
 kilométrage, 
 prix, 
 téléphone du propriétaire,
 est ce que la voiture est vendue par un professionnel ou un particulier***
'''

Main()

#Main loop
def Main():
    Regions=['Ile-de-France','Aquitaine','Provence-Alpes-cote d\'azur']
    Regions = NormalizeRegions(Regions)
    Search_model = NormalizeQuery('Renault CAPTUR')
    Results=[]
    page = getPageResult(Regions[0],Search_model)
#    for region in Regions:
#        page = getPageResult(region,Search_model)
#        getDataCurrentPage(page)
#    getVersionsEtArgus()
    Results = Results +  ParcoursPages(page)
   
    print Results 
#    print page
    print Regions
    print Search_model
    return Results
    
#Method to navigate across the different pages of a research
def ParcoursPages(page):
    DatasPages = []    
    DatasPages = DatasPages + getDataCurrentPage(page)
    next_page = getNextPage(page)
    if next_page:
        DatasPages=DatasPages+ParcoursPages(next_page)
    return DatasPages
    
    
#get the car versions and the corresponding Argus Prices  
def getVersionsEtArgus():
    url="http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html"
    page = getPageFromUrl(url)
    links = page.select(".tdSD.QuotMarque a")
    prices={}
    for link in links:
        url_Tmp="http://www.lacentrale.fr/"+link.get("href")
        name = link.text
        print name
        print url_Tmp
        newPage=getPageFromUrl(url_Tmp)
        result = newPage.select(".Result_Cote.arial")
        prices[name]=result[0].text
        
    print prices
    return prices
    
#Go on the next page on a search result
def getNextPage(page):
    next_page_href = page.find("a",text="Page suivante")
    if next_page_href != None :
        next_page_url=next_page_href.get("href")
        next_page =getPageFromUrl(next_page_url)
    else: 
        return False
#     next_page
    return next_page

#Returns the coordinates of the town
def getTownCoordinates(town):
    token ="AIzaSyAxu2GEhusJPMwMBsQs6scZJlhmX39WGy0"
    url='https://maps.googleapis.com/maps/api/geocode/json?address='+town+'&region=fr&key='+token
    results = requests.get(url)
    json = results.json()
    coordinates = json['results'][0]['geometry']['location']
    x,y = coordinates['lat'], coordinates['lng']
    return x,y
    
    
#Return the data from the page cars
def getDataCurrentPage(page):
    cars = getCars(page)
#    print cars
    dataPage = []
    resultP =  getDataForCar(cars[0])
    dataPage.append(resultP)
    return dataPage
#
#    for car in cars:
#            getDataForCar(car)
    
#Retrieve the informations for a car from its page
def getDataForCar(car):
    page = getPageFromUrl(car)
    Text_Description = page.select(".AdviewContent .content")[0].text
    phone = getPhoneInText(Text_Description)
    basics_Infos = page.select(".lbcParams.criterias table")
    year =  basics_Infos[0].find("th",text="Année-modèle :").next_sibling.next_sibling.text.strip()
    kms =  basics_Infos[0].find("th",text="Kilométrage :").next_sibling.next_sibling.text.strip()
    price = page.select(".price span")[0].text.strip()
    town =  page.select(".lbcParams.withborder table")[0].find("th",text="Ville :").next_sibling.next_sibling.text.strip()
    lat,lng = getTownCoordinates(town)
    seller = page.select(".upload_by .ad_pro")
    if len(seller)>0:
        seller="Pro"
    else:
        seller="Particulier"
#    print seller
#    print town
##    print basics_Infos
#    print year,kms
#    print price
    data = {}
    data['tel'] = phone
    data['kms'] = kms
    data['price'] = price.strip()
    data['owner_type'] = seller
    data['year'] = year
    data['version'] = 6
    data['lat'] =  lat
    data['lng'] = lng
#    print data
#    print page
    return data
    
    
#Giving the description text, retrieves the phone number of the seller
def getPhoneInText(text):
#    print text
    regex= re.compile("\b0\d{9}|\b0\d((-|.)\d{2}){4}")
    phone = regex.findall(text)
    print phone
    return phone
    
    
#Give the list of links in the page    
def getCars(page):
    results = page.find('div',class_="list-lbc")
    results = results.find_all('a')
    cars=[]
    for result in results:
        cars.append(result.get("href"))
    return cars
    
#
def NormalizeRegions(rawList):
    pattern = re.compile(r"\s|\'|-")    
    cleanedList=[]
    for rawString in rawList:
        cleanString = rawString.lower().strip()
        cleanString=pattern.sub("_",cleanString)
        cleanedList.append(cleanString)
    return cleanedList

def NormalizeQuery(query):
    return query.replace(' ','+')
    
def getPageResult(region,model):
    url = 'http://www.leboncoin.fr/voitures/offres/'+region+'/?f=a&th=1&q='+model    
    return getPageFromUrl(url)

def getPageFromUrl(url):
    page= requests.get(url)
    prettypage= BeautifulSoup(page.text)
    return prettypage
