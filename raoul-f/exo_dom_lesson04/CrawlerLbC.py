# -*- coding: utf-8 -*-
# Crawler le bon coin, Renault Capture

import time
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pandas import DataFrame
import re


def getURLfromRegion (strRegion, strQuery):
	#genere l'URL de la recherche pour une région donnée
	#Recherche dans le titre uniquement (it=1)
	return 'http://www.leboncoin.fr/voitures/offres/'+strRegion+'/?q='+strQuery+'&it=1'

def getHTMLpagefromURL (strURL):
  	HTMLPageRequest = requests.get(strURL)
 	if HTMLPageRequest.status_code == 200:
          return BeautifulSoup(HTMLPageRequest.text) #, 'html5lib')
 	else:
          print "Request failed with ", strURL

def getNextHTMLpagefromHTML (HTMLpage):
    HasNextpage = HTMLpage.find("a",text="Page suivante")
    print HasNextpage
    NextHTMLpage=''
    if HasNextpage == None :
        return False
    else:
        NextHTMLpage = HasNextpage.get("href")
        NextHTMLpage = getHTMLpagefromURL(NextHTMLpage)
    return NextHTMLpage

def getAnnoncesfromHTMLpage (HTMLpage):
    Annonces = HTMLpage.find('div',class_="list-lbc")
    Annonces = Annonces.find_all('a')
    for Annonce in Annonces:
        Annonces_URL.append(Annonce.get("href"))
    NextHTMLpage = getNextHTMLpagefromHTML (HTMLpage)
    #print NextHTMLpage
    if NextHTMLpage:
        getAnnoncesfromHTMLpage(NextHTMLpage)
    return

def getTelephone(strtext): #Javascript !!!
    regex= re.compile("0\d{9}|0\d((-|.)\d{2}){4}")
    Telephone = regex.search(strtext)
    if Telephone :
        Telephone = Telephone.group(0)
    return Telephone
    
def getGPS (strVille):
    strGoogleAPIToken = 'AIzaSyCHm4msRkOxGwmI3qhV-gXOsAKBPcH_IoM'
    strURL = 'https://maps.googleapis.com/maps/api/geocode/json?address='+strVille+'&region=fr&key='+ strGoogleAPIToken
    Lat = 'NaN'
    Lng = 'NaN'
    HTMLPageRequest = requests.get(strURL)
    if HTMLPageRequest.status_code == 200:
        JSON = HTMLPageRequest.json()
        if JSON['results'] != []:
            GPS = JSON['results'][0]['geometry']['location']
            Lat,Lng = GPS['lat'], GPS['lng']
    return Lat,Lng
        
def getAnnonceDetail (strRegion, Annonce_URL):
    try:
        AnnonceDetail={}
        HTMLpage = getHTMLpagefromURL (Annonce_URL)
        Description = HTMLpage.select(".AdviewContent .content")[0].text
        telephone = getTelephone(Description)
        info = HTMLpage.select(".lbcParams.criterias table")
        annee =  info[0].find("th",text="Année-modèle :").next_sibling.next_sibling.text.strip()
        kilometrage =  info[0].find("th",text="Kilométrage :").next_sibling.next_sibling.text.strip()
        prix = HTMLpage.select(".price span")[0].text.strip()
        ville =  HTMLpage.select(".lbcParams.withborder table")[0].find("th",text="Ville :").next_sibling.next_sibling.text.strip()
        lat,lng = getGPS(ville)
        typevendeur = HTMLpage.select(".upload_by .ad_pro")

        if len(typevendeur) > 0:
            typevendeur="Pro"
        else:
            typevendeur="Part"

        AnnonceDetail['Region'] = strRegion
        AnnonceDetail['Ville'] = ville
        AnnonceDetail['Version'] = ''
        AnnonceDetail['Annee'] = annee
        AnnonceDetail['Kilometrage'] = kilometrage
        AnnonceDetail['Prix'] = prix.strip()
        AnnonceDetail['Telephone'] = telephone #javascript ??
        AnnonceDetail['Type Vendeur'] = typevendeur
        AnnonceDetail['Latitude'] = lat
        AnnonceDetail['Longitude'] = lng
        #AnnonceDetail['URL'] = Annonce_URL
       
        return AnnonceDetail             
    except:
        pass


#MAIN:
lstRegions =['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
#lstRegions =['ile_de_france']
outputfile = "lbc_"+ time.strftime("%Y%m%d_%H%M%S")+".txt"
strQuery = "Renault%20Captur"
strcolumnsResults = ['Region','Ville', 'Version', 'Annee', 'Kilometrage', 'Prix','Telephone','Type Vendeur','Latitude', 'Longitude']
dfResults = pd.DataFrame(columns=strcolumnsResults) 
Annonces_URL=[]
for strRegion in lstRegions:	
    HTMLpage = getHTMLpagefromURL(getURLfromRegion(strRegion, strQuery))
    getAnnoncesfromHTMLpage (HTMLpage)
    for Annonce_URL in Annonces_URL:
        #print Annonce_URL
       dfAnnonce= getAnnonceDetail(strRegion, Annonce_URL)
       dfResults=dfResults.append(dfAnnonce, ignore_index=True)
dfResults.to_csv(outputfile)