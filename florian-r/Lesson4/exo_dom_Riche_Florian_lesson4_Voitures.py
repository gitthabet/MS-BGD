# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 14:19:06 2014

@author: Florian
"""

import requests
import json
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas
import re
import numpy as np

'''
 contenir les infos suivantes : 
 version ( il y en a 3), 
 année, 
 kilométrage, 
 prix, 
 téléphone du propriétaire,
 est ce que la voiture est vendue par un professionnel ou un particulier***
'''


#Main loop
def Main():
    Regions=['Ile-de-France','Aquitaine','Provence-Alpes-cote d\'azur']
    Regions = NormalizeRegions(Regions)
    model = 'Renault CAPTUR'
    Search_model = NormalizeQuery(model)
    Results=[]
    PricesArgus,ModelesVersions =  getVersionsEtArgus()
    
    for region in Regions:
        page = getPageResult(region,Search_model)
        Results = Results +  ParcoursPages(page,model,ModelesVersions)
   
    print Results 
#    print page
    print Regions
    print Search_model
    Results = DataFrame(Results)
    Results['Argus'] = Results['version'].map(lambda x:PricesArgus[x])
    return Results ,  PricesArgus,ModelesVersions
    
#Method to navigate across the different pages of a research
def ParcoursPages(page,CheckModel,ModelesVersions):
    DatasPages = []    
    DatasPages = DatasPages + getDataCurrentPage(page,CheckModel,ModelesVersions)
    next_page = getNextPage(page)
#    print "next page" 
    if next_page:
        DatasPages=DatasPages+ParcoursPages(next_page,CheckModel,ModelesVersions)
    return DatasPages
    
    
#get the car versions and the corresponding Argus Prices  
def getVersionsEtArgus():
    url="http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html"
    page = getPageFromUrl(url)
    links = page.select(".tdSD.QuotMarque a")
    prices={}
    prices[None] = np.NaN
    modeles=getCaracVersion(page)
    
    for link in links:
        url_Tmp="http://www.lacentrale.fr/"+link.get("href")
        name = link.text
#        print name
#        print url_Tmp
        newPage=getPageFromUrl(url_Tmp)
        result = newPage.select(".Result_Cote.arial")
        prices[name]=int(result[0].text.replace(u'€',u'').replace(' ',''))
    return prices,modeles

def getCaracVersion(page):
    modeles = page.select(".QuotMarque")
    Boite = page.select(".QuotBoite")
    Nrj = page.select(".QuotNrj")
    
    List=[]
    print len(modeles)
    print len(Boite)
    print len(Nrj)
    for i in range(len(Boite)):
        print modeles[i].text.strip()
        print Boite[i].text.strip()
        print Nrj[i].text.strip()
        Modeles={}
        Modeles['FullModele'] =  modeles[i].text.strip()
        Modeles['Version'] =  FindModel(modeles[i].text.strip())
        Modeles['Boite'] =  Boite[i].text.strip()
        Modeles['Energie'] = Nrj[i].text.strip()
        List.append(Modeles)
    df = DataFrame(List)
    df['Boite'][df['Boite']!='Automatique']='Manuelle'
    print df
#    A = CorrectList[(CorrectList.Boite =='Automatique')&(CorrectList.Energie =='Essence')&(CorrectList.Version=="INTENS")]
#    print A
#    print A['FullModele'].iloc[0]
##    print CorrectList.Boite=='Automatique'
##    print DataFrame['Boite']
#    print CorrectList
    return df

def FindModel(text):
    Regex  = re.compile(r"(?i)arizona|business|intens|zen|life")
    results = Regex.search(text)
    if results: 
#            print results.group(0).lower()
            return results.group(0).upper()
    else : return None
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
#    print results
    json = results.json()
    coordinates = json['results'][0]['geometry']['location']
    x,y = coordinates['lat'], coordinates['lng']
    return x,y
    
    
#Return the data from the page cars
def getDataCurrentPage(page,CheckModel,ModelesVersions):
    cars = getCars(page,CheckModel)
#    print cars
    dataPage = []
    
    resultP =  getDataForCar(cars[0],ModelesVersions)
    dataPage.append(resultP)
#    for car in cars:
#            print car
#            resultP =  getDataForCar(car,ModelesVersions)
#            dataPage.append(resultP)
    return dataPage
#
#    
    
#Retrieve the informations for a car from its page
def getDataForCar(car,ModelesVersions):
    data = {}
    data['url'] = car
    lat, lng = "Na","Na"
    page = getPageFromUrl(car)
    Text_Description = page.select(".AdviewContent .content")[0].text
    version = "Na"
    version = FindModel(Text_Description)
    name = page.find('h2',id='ad_subject').text
    phone = getPhoneInText(Text_Description)
    basics_Infos = page.select(".lbcParams.criterias table")
    carburant = basics_Infos[0].find("th",text="Carburant :").next_sibling.next_sibling.text.strip()
    boite  = basics_Infos[0].find("th",text="Boîte de vitesse :").next_sibling.next_sibling.text.strip()
    year =  basics_Infos[0].find("th",text="Année-modèle :").next_sibling.next_sibling.text.strip()
    kms =  basics_Infos[0].find("th",text="Kilométrage :").next_sibling.next_sibling.text.replace("KM","").replace(' ','')
    price = page.select(".price span")[0].text.replace(u'\xa0',u'').replace(u'€',u'').replace(' ','')
    town =  page.select(".lbcParams.withborder table")[0].find("th",text="Ville :")
#    print ModelesVersions    
    FullName = ModelesVersions[(ModelesVersions.Boite == boite)&(ModelesVersions.Energie ==carburant)&(ModelesVersions.Version==version)]
#    print "apres ", ModelesVersions
#    print carburant
#    print boite
#    print version    
#    print A
    if len(FullName):
        version =  FullName['FullModele'].iloc[0]    
    if town:
        town=town.next_sibling.next_sibling.text.strip()
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
#    print name
    data['annonce'] = name
    data['tel'] = phone
    data['kms'] = int(kms)
    data['price'] = int(price)
    data['owner_type'] = seller
    data['year'] = year
    data['version'] = version
    data['lat'] =  lat
    data['lng'] = lng
    data['carburant'] = carburant
    data['boite'] = boite
#    print data
#    print page
    return data
    
    
#Giving the description text, retrieves the phone number of the seller
def getPhoneInText(text):
#    print text
    regex= re.compile("0\d{9}|0\d((-|.)\d{2}){4}")
    phone = regex.search(text)
    if phone :
        phone = phone.group(0)
#    print phone
    return phone
    
    
#Give the list of links in the page    
def getCars(page,CheckModel):
    results = page.find('div',class_="list-lbc")
    results = results.find_all('a')
    cars=[]
    checkmodel = CheckModel.lower().strip()
    for result in results:
        if checkmodel in result.text.lower().strip():
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

results,Prices, Argus = Main()
results.to_excel("Resultats.xlsx")
Argus.to_excel("Argus.xlsx")