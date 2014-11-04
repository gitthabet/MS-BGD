# -*- coding: utf-8 -*-
"""
Created on Fri Oct 31 19:47:11 2014

@author: roms
"""

###############################################################################
# 0 - imports and methods to be used
###############################################################################

# initialization
import requests
from bs4 import BeautifulSoup
import csv
import shutil
import subprocess
import difflib

# gets 'Le bon coin' homepage
lbcHome = requests.get('http://www.leboncoin.fr/')
lbcHomeSoup = BeautifulSoup(lbcHome.text,'html5lib')

# method that extract some infos from a single ad page soup
def extractInfosLbc(lbcResultSoup):
    # get id
    url=lbcResultSoup.find('link',rel='canonical').get('href')
    id_=url.replace('http://www.leboncoin.fr/voitures/','').replace('.htm?ca=12_s','').replace('.htm','')
    print('Extracting info from ad number: ' + id_)
    # get brand/model/year/mileage
    brand=model=year=mileage='NA'
    for spec in lbcResultSoup.find('div',class_='lbcParams criterias').table.tbody.find_all('tr'):
        if(spec.th.text=='Marque :'):
            brand = spec.td.text.strip().lower()
        if(spec.th.text=='Modèle :'):
            model = spec.td.text.strip().lower()
        if(spec.th.text=='Année-modèle :'):
            year = spec.td.text.strip().lower()
            if year != '':
                year = int(year)
            else:
                year = 'NA'
        if(spec.th.text=='Kilométrage :'):
            mileage = spec.td.text.strip().lower()
            mileage=mileage.replace('\n','').replace('km','').replace(' ','')
            mileage = int(mileage)
    # get price
    price=lbcResultSoup.find('span',class_='price').text.lower()
    price=price.replace('\xa0','')
    price=price.replace(' ','')
    price=price[:len(price)-1]
    price=int(price)
    return [id_,brand,model,'',year,mileage,price,'','','','','']

# imports a dict: <model,casco value>
cascos = requests.get('http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html')
cascosSoup = BeautifulSoup(cascos.text,'html5lib')

cascoValues={}
for casco in cascosSoup.find_all('a',style="color:#007EFF; text-decoration:underline"):
    model=casco.text
    cascoUrl = 'http://www.lacentrale.fr/' + casco.get('href')
    cascoPage = requests.get(cascoUrl)
    cascoPageSoup = BeautifulSoup(cascoPage.text,'html5lib')
    cascoValue = cascoPageSoup.find('span',class_='Result_Cote arial tx20').text
    cascoValue = cascoValue.replace(' ','')
    cascoValue = cascoValue[:len(cascoValue)-1]
    cascoValue = int(cascoValue)
    cascoValues[model]=cascoValue

# method that extracts the version of the car
## returns the %of words/characters in common between two lists, using a
## distance parameter to specify if two words are the same
def partInCommon(smallString, bigString, alpha):
    smallList=smallString.split()    
    bigList=bigString.split()    
    count = 0.0
    found = 0.0
    for smallWord in smallList:
        for bigWord in bigList:
            if difflib.SequenceMatcher(None,smallWord.lower(),bigWord.lower()).ratio() >= alpha and len(smallWord)>1 and len(bigWord)>1:
                found=1
        count+=found
        found=0
    return count/len(smallList)

## returns model and casco corresponding to ad
def getModelAndCasco(adString):
    adModel = 'NA'
    ressemblance = 0.0
    for model in cascoValues.keys():
        if(partInCommon(model,adString,0.80)>ressemblance):
            ressemblance = partInCommon(model,adString,0.80)
            adModel = model
    if adModel == 'NA':
        adCasco = 'NA'
    else:
        adCasco = cascoValues[adModel]
    return [adModel,adCasco]

# method that extracts the phone number from ad id
# NOTE: not perfect, most of the time, 6s are mistaken for 5s
def getPhoneNumber(id_):
    # get phone number link
    phoneNumberUrl1='http://www2.leboncoin.fr/ajapi/get/phone?list_id='+id_
    phoneNumberUrl2=requests.get(phoneNumberUrl1).json()
    if phoneNumberUrl2 != '':    
        # downloads image and save it on HDD
        phoneNumberImage=requests.get(phoneNumberUrl2['phoneUrl'], stream=True)
        with open('phoneNumber.gif', 'wb') as out_file:
            shutil.copyfileobj(phoneNumberImage.raw, out_file)
        del phoneNumberImage
        # launch tesseract (OCR) on image
        subprocess.call(['tesseract', 'phoneNumber.gif', 'phoneNumberText','-psm', '7'])
        # reads result
        phoneNumberFile = open('phoneNumberText.txt', 'r')
        phoneNumber = str(phoneNumberFile.read(10))
        phoneNumberFile.close()
        # erase files
        subprocess.call(['rm','phoneNumber.gif'])
        subprocess.call(['rm','phoneNumberText.txt'])
        return phoneNumber
    else:
        return 'NA'

# method that search for the lat/long of the city into Google geocode
def findLatLng(lbcResultSoup):
    # get town/zipcode
    city=zipcode=''
    for line in lbcResultSoup.find_all('table')[0].tbody.find_all('tr'):
        if(line.th.text=='Ville :'):
            city = str(line.td.text)
        if(line.th.text=='Code postal :'):
            zipcode = str(line.td.text)
    
    # get long/lat from google Geocode API
    api_key='AIzaSyAF1DGjNqXDpsik9pSAARs35PVnxJkL744'
    api_search='https://maps.googleapis.com/maps/api/geocode/json?address=' + city + '+' + zipcode + '+France' + '&key=' + api_key
    resultApi=requests.get(api_search)
    lat=resultApi.json()['results'][0]['geometry']['location']['lat']
    lng=resultApi.json()['results'][0]['geometry']['location']['lng']
    return [lat,lng]

###############################################################################
# 1 - scope definition and crawling
###############################################################################

# puts all links to regions into a dict
regions={}
for child in lbcHomeSoup.find('td',class_='CountyList').find_all('a'):
    regions[child.contents[0]]=child.get('href')

# we will only search for PACA, IDF and Aquitaine
regions_redux={}
for region in ['Provence-Alpes-Côte d\'Azur','Ile-de-France','Aquitaine']:
    regions_redux[region]=regions[region]

# loops and crawl
resultCsv=open('lbc.csv', 'w', newline='')
csvwriter=csv.writer(resultCsv,quoting=csv.QUOTE_NONNUMERIC)
csvwriter.writerow(['ID','BRAND','MODEL','VERSION','YEAR','MILEAGE','PRICE','PHONE','TYPE','CASCO','LATITUDE','LONGITUDE'])

counter=0
for url in regions_redux.values():
    # looks specifically for cars and 'captur'
    url=url.replace('http://www.leboncoin.fr/','http://www.leboncoin.fr/voitures/')
    url=url.replace('annonces/','')
    url=url+'?q=captur'
    for type_ad in ['c','p']: # p = particuliers, c = pros
        page=1     
        # results page
        lbcResultPage=requests.get(url+'&f=' + type_ad + '&o=' + str(page))
        lbcResultPageSoup=BeautifulSoup(lbcResultPage.text,"html5lib")   
        # while there are pages/results (ie 'aucune annonce' not found in page)
        while(lbcResultPageSoup.text.lower().find('aucune annonce')== -1):
            # extracts all links from results page
            for resultLink in lbcResultPageSoup.find('div',class_='list-lbc').find_all('a'):
                # link from one ad
                lbcResult=requests.get(resultLink.get('href'))
                lbcResultSoup=BeautifulSoup(lbcResult.text,"html5lib")
                # for each ad, get the infos from page into a new row to be written
                counter+=1     
                print('(Extraction number : ' + str(counter) + ')')
                resultRow=extractInfosLbc(lbcResultSoup)
                # get description
                desc = lbcResultSoup.find('meta',attrs={"name":"description"}).get('content')
                # add model and casco
                modelAndCasco = getModelAndCasco(desc)
                resultRow[3]=modelAndCasco[0]
                resultRow[9]=modelAndCasco[1]
                # add phone number
                resultRow[7]=getPhoneNumber(resultRow[0])
                # add type
                if(type_ad == 'p'):
                    resultRow[8]='particulier'
                else:
                    resultRow[8]='professionnel'
                # add lat/long                
                resultRow[10:]=findLatLng(lbcResultSoup)
                # add row to csv file if car is indeed a Renault Captur
                if(resultRow[1].lower() in ['na','renault'] and resultRow[2].lower() in ['na','captur']):
                    csvwriter.writerow(resultRow)
            page+=1            
            lbcResultPage=requests.get(url+'&f=' + type_ad + '&o=' + str(page))
            lbcResultPageSoup=BeautifulSoup(lbcResultPage.text,"html5lib")   
            
resultCsv.close()

