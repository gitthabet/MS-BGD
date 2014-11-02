# -*- coding: utf-8 -*-

import numpy as np 
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import re
import json


#Create the DataFrame to store all the collected data related to Renault Captur small ads.
def createCarsAdsDataFrame():
    columnsNames = ['Region','Version','Annee','Kilometrage','Prix','Cote Argus','Prix vs Cote','Telephone','Type vendeur','Latitude', 'Longitude','URL']
    CarsAds = pd.DataFrame(columns = columnsNames)
    return CarsAds


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None


#Return the Number of pages of results for a given request
def getPagesNumber(url):
    topUrlSoup = getSoupFromUrl(url)
    #Get the number of ads 
    adsNumber = topUrlSoup.select('span b')[0].contents[0]
    return int(np.ceil(int(adsNumber)/100.0))

        
#Create the list of URLs pointing to the small adds 
def createAdsUrlsList(topUrl):
    topUrlSoup = getSoupFromUrl(topUrl)
    
    balises_a = topUrlSoup.find(class_="list-lbc").find_all('a')
    
    return [balise.get('href') for balise in balises_a]


#Build a list of words with the Content tags List as input
def buildCarDescriptionWordsList (tagsList, adsTitle):
    carDescriptionString =adsTitle
    for tag in tagsList:
        carDescriptionString = carDescriptionString + " " +unicode(tag.string)
     
    return carDescriptionString.lower()


#Figure out the car version on the basis of the www.lacentrale.fr version list :
#Cars Versions : "0.9 TCE 90 ENERGY ARIZONA ECO2" ; "0.9 TCE 90 ENERGY S&S INTENS ECO2" ; "0.9 TCE 90 ENERGY S&S LIFE ECO2";
#                "0.9 TCE 90 ENERGY S&S ZEN ECO2" ; "1.2 TCE 120 ARIZONA EDC Essence" ; "1.2 TCE 120 INTENS EDC  Essence"
#                "1.2 TCE 120 ZEN EDC Essence" ; "1.5 DCI 90 ARIZONA EDC ECO2 Diesel" ; "1.5 DCI 90 BUSINESS EDC Diesel"
#                "1.5 DCI 90 ENERGY ARIZONA ECO2" 
def findCarVersion(wordsList):
    
    carVersionAttributes = {'Cylindre' : "" , 'OilType1' : "" , 'Digits' : "", 'Name1' : "", 'Name2' : "", 'Name3' : "", 'Name4' : "", 'Name5' : "",'OilType2' : ""}
    carVersion =""
    if wordsList.count('0.9')>0 :
        carVersionAttributes['Cylindre'] = '0.9'
    if wordsList.count('1.2')>0 :
        carVersionAttributes['Cylindre'] = '1.2'
    if wordsList.count('1.5')>0 :
        carVersionAttributes['Cylindre'] = '1.5'
    
    if wordsList.count('tce')>0 :
        carVersionAttributes['OilType1'] = 'TCE'
    if wordsList.count('dci')>0 :
        carVersionAttributes['OilType1'] = 'DCI'
    
    if wordsList.count('90')>0 :
        carVersionAttributes['Digits'] = '90'
    if wordsList.count('120')>0 :
        carVersionAttributes['Digits'] = '120' 
    
    if wordsList.count('energy')>0 :
        carVersionAttributes['Name1'] = 'ENERGY' 

    if wordsList.count('s&s')>0 :
        carVersionAttributes['Name2'] = 'S&S'

    if wordsList.count('arizona')>0 :
        carVersionAttributes['Name3'] = 'ARIZONA'
    if wordsList.count('intens')>0 :
        carVersionAttributes['Name3'] = 'INTENS'
    if wordsList.count('life')>0 :
        carVersionAttributes['Name3'] = 'LIFE'
    if wordsList.count('zen')>0 :
        carVersionAttributes['Name3'] = 'ZEN'
    if wordsList.count('business')>0 :
        carVersionAttributes['Name3'] = 'BUSINESS'

    if wordsList.count('edc')>0 :
        carVersionAttributes['Name4'] = 'EDC'
  
    if wordsList.count('ec02')>0 :
        carVersionAttributes['Name5'] = 'EC02'       
    
    if wordsList.count('essence')>0 :
        carVersionAttributes['OilType2'] = 'Essence' 
    if wordsList.count('diesel')>0 :
        carVersionAttributes['OilType2'] = 'Diesel' 
    
    # "0.9 TCE 90 ENERGY ARIZONA ECO2" ; 
    if carVersionAttributes['Cylindre'] == '0.9' and  carVersionAttributes['Name1'] == 'ENERGY' and carVersionAttributes['Name3'] == 'ARIZONA' and carVersionAttributes['Name5'] == 'EC02' : return "0.9 TCE 90 ENERGY ARIZONA ECO2"
    if (carVersionAttributes['Cylindre'] == '0.9' or (carVersionAttributes['OilType1'] == 'TCE' and carVersionAttributes['Digits'] == '90')) and carVersionAttributes['Name3'] == 'ARIZONA' : return "0.9 TCE 90 ENERGY ARIZONA ECO2"
    
    # "1.2 TCE 120 ARIZONA EDC Essence" ;
    if (carVersionAttributes['Cylindre'] == '1.2' or carVersionAttributes['Digits'] == '120') and carVersionAttributes['Name3'] == 'ARIZONA' and carVersionAttributes['Name4'] == 'EDC' : return "1.2 TCE 120 ARIZONA EDC Essence"
    if (carVersionAttributes['Cylindre'] == '1.2' or carVersionAttributes['Digits'] == '120') and carVersionAttributes['Name3'] == 'ARIZONA' : return "1.2 TCE 120 ARIZONA EDC Essence"
    
    # "1.5 DCI 90 ENERGY ARIZONA ECO2"
    if (carVersionAttributes['Cylindre'] == '1.5' or carVersionAttributes['OilType1'] == 'DCI') and carVersionAttributes['Name1'] == 'ENERGY' and carVersionAttributes['Name3'] == 'ARIZONA' and carVersionAttributes['Name5'] == 'EC02': return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
    if (carVersionAttributes['Cylindre'] == '1.5' or carVersionAttributes['OilType1'] == 'DCI') and carVersionAttributes['Name1'] == 'ENERGY' and carVersionAttributes['Name3'] == 'ARIZONA' : return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
    
    # "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
    if (carVersionAttributes['Cylindre'] == '1.5' or carVersionAttributes['OilType1'] == 'DCI') and carVersionAttributes['Name3'] == 'ARIZONA' and carVersionAttributes['Name4'] == 'EDC' and carVersionAttributes['Name5'] == 'EC02': return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
    if (carVersionAttributes['Cylindre'] == '1.5' or carVersionAttributes['OilType1'] == 'DCI') and carVersionAttributes['Name3'] == 'ARIZONA' and carVersionAttributes['Name4'] == 'EDC': return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
    
    #"0.9 TCE 90 ENERGY S&S INTENS ECO2" 
    if (carVersionAttributes['Cylindre'] == '0.9' or carVersionAttributes['Digits'] == '90') and carVersionAttributes['Name3'] == 'INTENS' and (carVersionAttributes['Name5'] == 'EC02' or carVersionAttributes['Name2'] == 'S&S'): return "0.9 TCE 90 ENERGY S&S INTENS ECO2"
    if (carVersionAttributes['Cylindre'] == '0.9' or carVersionAttributes['Digits'] == '90') and carVersionAttributes['Name3'] == 'INTENS': return "0.9 TCE 90 ENERGY S&S INTENS ECO2"
    
    # "1.2 TCE 120 INTENS EDC Essence"
    if (carVersionAttributes['Cylindre'] == '1.2' or carVersionAttributes['Digits'] == '120') and carVersionAttributes['Name3'] == 'INTENS' and carVersionAttributes['Name4'] == 'EDC' : return "1.2 TCE 120 INTENS EDC Essence"
    if (carVersionAttributes['Cylindre'] == '1.2' or carVersionAttributes['Digits'] == '120') and carVersionAttributes['Name3'] == 'INTENS': return "1.2 TCE 120 INTENS EDC Essence"

    # "0.9 TCE 90 ENERGY S&S LIFE ECO2"
    if carVersionAttributes['Name3'] == 'LIFE' : return "0.9 TCE 90 ENERGY S&S LIFE ECO2" 
    
    # "0.9 TCE 90 ENERGY S&S ZEN ECO2"
    if (carVersionAttributes['Cylindre'] == '0.9' or carVersionAttributes['Digits'] == '90') and carVersionAttributes['Name3'] == 'ZEN' and carVersionAttributes['Name5'] == 'EC02' : return "0.9 TCE 90 ENERGY S&S ZEN ECO2"
    if (carVersionAttributes['Cylindre'] == '0.9' or carVersionAttributes['Digits'] == '90') and carVersionAttributes['Name3'] == 'ZEN': return "0.9 TCE 90 ENERGY S&S ZEN ECO2"

    # "1.2 TCE 120 ZEN EDC Essence"
    if (carVersionAttributes['Cylindre'] == '1.2' or carVersionAttributes['Digits'] == '120') and carVersionAttributes['Name3'] == 'ZEN' and carVersionAttributes['Name4'] == 'EDC' : return "1.2 TCE 120 ZEN EDC Essence"
    if (carVersionAttributes['Cylindre'] == '1.2' or carVersionAttributes['Digits'] == '120') and carVersionAttributes['Name3'] == 'ZEN': return "1.2 TCE 120 ZEN EDC Essence"

    # "1.5 DCI 90 BUSINESS EDC Diesel"
    if carVersionAttributes['Name3'] == 'BUSINESS' : return "1.5 DCI 90 BUSINESS EDC Diesel"
    
    return carVersion

 
#Return the refined argus for the given car at www.lacentrale.fr, taking into account the number of kilometers 
#If car is from 2014, apply a 1.06 coef to the 2013 argus 

def getArgus(carVersion, kmsNumber, carYear) :
    
    laCentraleUrl = "Inconnue"

    if carVersion == "0.9 TCE 90 ENERGY ARIZONA ECO2": #1
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+arizona+eco2-2013.html'

    if carVersion == "1.2 TCE 120 ARIZONA EDC Essence": #5
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+arizona+edc-2013.html'

    if carVersion == "1.5 DCI 90 ENERGY ARIZONA ECO2": #10
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+arizona+eco2-2013.html'

    if carVersion == "1.5 DCI 90 ARIZONA EDC ECO2 Diesel": #8
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+arizona+edc+eco2-2013.html'

    if carVersion == "0.9 TCE 90 ENERGY S&S INTENS ECO2": #2
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+intens+eco2-2013.html'
    
    if carVersion == "1.2 TCE 120 INTENS EDC Essence": #6
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+intens+edc-2013.html'

    if carVersion == "0.9 TCE 90 ENERGY S&S LIFE ECO2": #3
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+life+eco2-2013.html'

    if carVersion == "0.9 TCE 90 ENERGY S&S ZEN ECO2": #4
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+zen+eco2-2013.html'

    if carVersion == "1.2 TCE 120 ZEN EDC Essence": #7
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+zen+edc-2013.html'

    if carVersion == "1.5 DCI 90 BUSINESS EDC Diesel": #9
        laCentraleUrl = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+business+edc-2013.html'
    
    if laCentraleUrl== "Inconnue": return float('nan')

    laCentraleUrlSoup = getSoupFromUrl(laCentraleUrl)
    argusString = laCentraleUrlSoup.find(class_="Result_Cote arial tx20").string
    argusInt = int(re.sub(r'\D',"",argusString))
    
    if carYear=='2014' : argusInt = argusInt*1.06
    
    if (type (kmsNumber) is not int) : return argusInt

    else :

        if carVersion.count('DCI')>0 : averageKmsNumber = 20000
        else : averageKmsNumber = 15000
        
        if kmsNumber > averageKmsNumber : refinedargusInt = argusInt - 0.035 * (kmsNumber - averageKmsNumber)
        
        elif kmsNumber <= averageKmsNumber : refinedargusInt = argusInt + 0.031 * (kmsNumber - averageKmsNumber)

    return np.ceil(refinedargusInt)
 

#Get the GPS coordinates of a given location

def getGPSCoordinates(zipCode):
    req=requests.get ('https://maps.googleapis.com/maps/api/geocode/json?address='+str(zipCode)+'+France&key=AIzaSyAWelhRJMkKfVZee_EC-qz6GGQ-mipGy3M')
    feedbackJson = json.loads(req.content)
    latitude = feedbackJson.get('results')[0].get('geometry').get('location').get('lat')
    longitude = feedbackJson.get('results')[0].get('geometry').get('location').get('lng')
    return (str(latitude) +',' + str(longitude))


#Get the Phone Numbers from the ads text

def getPhoneNumbers(adsTextTagsList):
    
    phoneNumbers=""
    phoneNumbersList=[]
    for tag in adsTextTagsList:
        phonePattern = re.compile(r'([0]\d{1}[-\.\s]*\d{2}[-\.\s]*\d{2}[-\.\s]*\d{2}[-\.\s]*\d{2})')
        phoneNumbersTagList = list(set(phonePattern.findall(unicode(tag.string))))
        if phoneNumbersTagList:
            phoneNumbersList = phoneNumbersList + phoneNumbersTagList
    for phoneNumber in list(set(phoneNumbersList)):        
            phoneNumbers = phoneNumbers + re.sub(r'\D',"", unicode(phoneNumber)).strip() + " / "
    phoneNumbers = phoneNumbers[:-2]
    if phoneNumbers=="":
        phoneNumbers = 'Inconnu'

    return phoneNumbers


#Get all the required data from the small ads 

def getAdsData (adsUrl):
    
    #print "URL : ", adsUrl
    adsUrlSoup = getSoupFromUrl(adsUrl)

    adsTitle = adsUrlSoup.title.string
    
    priceString = adsUrlSoup.find(class_="price").select('span')[0].string
    priceInt = int(re.sub(r'\D',"",priceString))
    
    yearString = adsUrlSoup.find(class_="lbcParams criterias").select('tr + tr + tr td')[0].string
    yearString = re.sub(r'\D', "", yearString)

    kmString = adsUrlSoup.find(class_="lbcParams criterias").select('tr + tr + tr + tr td')[0].string
    try:
        kmInt = int(re.sub(r'\D', "", kmString))
    except ValueError:
        kmInt = float('nan')
    
    zipCodeString = adsUrlSoup.find(class_="floatLeft").select('tr + tr + tr td')[0].string
    zipCodeInt = int(re.sub(r'\D', "", zipCodeString))

    adsTextTagsList = adsUrlSoup.find(class_="content").contents
    
    phoneNumbers = getPhoneNumbers(adsTextTagsList)
    
    carDescriptionString = buildCarDescriptionWordsList (adsTextTagsList,adsTitle) 
    
    carVersion =  findCarVersion (carDescriptionString)
    
    carArgus = getArgus(carVersion, kmInt, yearString)

    prixVsCoteMoyenne=''
    if carArgus > priceInt : prixVsCoteMoyenne = 'Moins cher'
    if carArgus == priceInt : prixVsCoteMoyenne = 'Prix identique a argus'
    if carArgus < priceInt : prixVsCoteMoyenne = 'Plus cher'

    gpsCoordinates = getGPSCoordinates (zipCodeInt)
    latitude = gpsCoordinates.split(',')[0]
    longitude = gpsCoordinates.split(',')[1]
    
    valuesList  = [('',carVersion, yearString, kmInt, priceInt, carArgus, prixVsCoteMoyenne, phoneNumbers, '', latitude, longitude, adsUrl)]
                                  
    dataFrameRecord = pd.DataFrame(valuesList, columns=['Region','Version', 'Annee', 'Kilometrage', 'Prix', 'Cote Argus','Prix vs Cote','Telephone', 'Type vendeur', 'Latitude', 'Longitude', 'URL'])
    
    return dataFrameRecord
    

#Clean-Up the DataFrame
def cleanUp(carsAdsDataFrame):
    #carsAdsDataFrame = carsAdsDataFrame['Version' != ""]
    carsAdsDataFrame = carsAdsDataFrame.dropna(subset=['Version','Kilometrage', 'Prix', 'Cote Argus'], how='any')
    return carsAdsDataFrame


#Create and feed the DataFrame with all the cars ads and export it to Excel and CSV format
def main():
    carsAdsDataFrame = createCarsAdsDataFrame()
    
    regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
    typeVendeurs = {'f=p' : 'Particulier', 'f=c' : 'Professionnel'}
    
    #Requests per region and per vendor type made without retrieving the pictures to limit the bandwidth usage 
    for region in regions:
        for cleTypeVendeur, valueTypeVendeur in typeVendeurs.items():
            pagesNumber = getPagesNumber('http://www.leboncoin.fr/voitures/offres/'+region+'?o=0&q=Captur&it=1&th=0&'+cleTypeVendeur)
            
            for pageIndex in range(pagesNumber):
                adsUrlsList = createAdsUrlsList('http://www.leboncoin.fr/voitures/offres/'+region+'?o='+str(pageIndex+1)+'&q=Captur&it=1&th=0&'+cleTypeVendeur)
                for adsUrl in adsUrlsList:
                    dataFrameRecord = getAdsData (adsUrl)
                    dataFrameRecord['Region'] = region
                    dataFrameRecord['Type vendeur'] = valueTypeVendeur
                    carsAdsDataFrame = carsAdsDataFrame.append(dataFrameRecord)
    
    carsAdsDataFrame = cleanUp(carsAdsDataFrame)
    carsAdsDataFrame.to_excel('Renault_Captur.xlsx', sheet_name='Sheet1')
    carsAdsDataFrame.to_csv('Renault_Captur.csv')

if __name__ == "__main__":
    main()

