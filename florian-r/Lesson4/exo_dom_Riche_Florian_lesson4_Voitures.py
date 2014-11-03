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
import numpy as np

'''
INSTRUCTIONS 
  
Exercice pour la semaine prochaine l'objectif est de générer un fichier de données sur le prix des Renault Zoé sur le marché de l'occasion en Ile de France, PACA et Aquitaine. Vous utiliserez leboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes : version ( il y en a 3), année, kilométrage, prix, téléphone du propriétaire, est ce que la voiture est vendue par un professionnel ou un particulier. Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html.
Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿

erratum : vous travaillerez sur la Renault Captur (beaucoup plus d'annonces que la Zoé)
addendum: Vous ajouterez 2 colonnes avec latitude et longitude de la ville ou est présente la voiture -> utiliser une API Google au choix
'''


######################## MAIN FUNCTION  #############################
def Main():
    #Définitions des régions où chercher et du modèle.
    #Préparation pour la requete
    Regions=['Ile-de-France','Aquitaine','Provence-Alpes-cote d\'azur']

    Regions = NormalizeRegions(Regions)
    model = 'Renault CAPTUR'
    Search_model = NormalizeQuery(model)
    Results=[]
    #Récupération :
    # -De l'Argus des différents modèles
    # -Des caractéristiques des modèles pour les retrouver plus facilement dans les annonces
    PricesArgus,ModelesVersions =  getVersionsEtArgus()
    
    #Parcours des pages du site leboncoin pour chaque région:
    for region in Regions:
        page = getPageResult(region,Search_model)
        Results = Results +  ParcoursPages(page,model,ModelesVersions)
   
    #Stockage des données dans une dataFrame et manipulation des données
    Results = DataFrame(Results)
        #Ajout de l'Argus correspondant à la version
    Results['Argus'] = Results['version'].map(lambda x:PricesArgus[x])
        #Ajout de la moyenne de la version
    Version_Mean = Results.groupby(['version'])['price'].mean()
    Version_Mean = dict(Version_Mean)
    Version_Mean[None] = np.NaN
    Results['MoyenneVersion'] = Results['version'].map(lambda x:Version_Mean[x])
        #Ajout d'un test pour savoir si l'offre est une bonne affaire
    Results['InferieurMoyenne'] = Results['price']<Results['MoyenneVersion']
    #Mise en ordre des indices
    Results = DataFrame(Results,columns=['annonce','version','price','MoyenneVersion','Argus','InferieurMoyenne','boite','carburant','kms','year','owner_type','tel','lat','lng','url'])
    #Retour des résultats
    return Results ,  PricesArgus,ModelesVersions
    
######################## CORE FUNCTIONS  #############################


######################## ARGUS
    
#get the car versions and the corresponding Argus Prices  
def getVersionsEtArgus():
    url="http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html"
    page = getPageFromUrl(url)
    
    #Récupération des caractéristiques des différents modèles
    modeles=getCaracVersion(page)
    
    #Récupérations des liens vers les modèles
    links = page.select(".tdSD.QuotMarque a")
    prices={}
    prices[None] = np.NaN
    #Parcours des Argus, stockage et traitement
    for link in links:
        url_Tmp="http://www.lacentrale.fr/"+link.get("href")
        name = link.text
        newPage=getPageFromUrl(url_Tmp)
        result = newPage.select(".Result_Cote.arial")
        prices[name]=int(result[0].text.replace(u'€',u'').replace(' ',''))
    #Retourne les prix des Argus et les caractéristiques des modèles
    return prices,modeles

#get caracterstics of cars
def getCaracVersion(page):
    
    #Récupération des noms, du type de boite et de l'energie
    #Il est plus aisé de les caractériser et de retrouver les modèles ainsi
    modeles = page.select(".QuotMarque")
    Boite = page.select(".QuotBoite")
    Nrj = page.select(".QuotNrj")
    
    #Parcours et stockage dans une DataFrame pour manipulation ultèrieure
    List=[]
    for i in range(len(Boite)):
        Modeles={}
        Modeles['FullModele'] =  modeles[i].text.strip()
        Modeles['Version'] =  FindModel(modeles[i].text.strip())
        Modeles['Boite'] =  Boite[i].text.strip()
        Modeles['Energie'] = Nrj[i].text.strip()
        List.append(Modeles)
    df = DataFrame(List)    
    return df
    
    
    
    

######################## LE BON COIN


#Method to navigate across the different pages of a research
def ParcoursPages(page,CheckModel,ModelesVersions):
    #Méthode récursive pour parser l'ensemble des pages du site le bon coin pour une recherche
    DatasPages = []    
    #Prendre les données sur cette page et prendre le lien vers la suivante
    DatasPages = DatasPages + getDataCurrentPage(page,CheckModel,ModelesVersions)
    next_page = getNextPage(page)
    #Si le lien existe on effectue le même parsage sur la ligne suivante
    if next_page:
        DatasPages=DatasPages+ParcoursPages(next_page,CheckModel,ModelesVersions)
    return DatasPages
    
    
#Go on the next page on a search result
def getNextPage(page):
    #On récupère le bouton amenant à la page suivante
    next_page_href = page.find("a",text="Page suivante")
    #Si celui-ci existe, on récupère la page suivante
    if next_page_href != None :
        next_page_url=next_page_href.get("href")
        next_page =getPageFromUrl(next_page_url)
        return next_page
    #On retourne "False" sinon
    else: 
        return False

    
#Return the data from the page cars
def getDataCurrentPage(page,CheckModel,ModelesVersions):
    #Récupération des liens vers les voitures qui correspondent à la recherche
    cars = getCars(page,CheckModel)
    dataPage = []
    
    #Parcours des liens et stockage dans une liste de dictionnaire    
    for car in cars:
            resultP =  getDataForCar(car,ModelesVersions)
            dataPage.append(resultP)
            
    return dataPage
    
#Give the list of links in the page    
def getCars(page,CheckModel):
    #Trouve la liste des liens dans la table
    results = page.find('div',class_="list-lbc")
    results = results.find_all('a')
    cars=[]
    checkmodel = CheckModel.lower().strip()
    #Pour chaque annonce, vérification de la conformité 
    #et ajout du lien à la liste des liens
    for result in results:
        if checkmodel in result.text.lower().strip():
            cars.append(result.get("href"))
    return cars
    
#Retrieve the informations for a car from its page
def getDataForCar(car,ModelesVersions):
    #Initialisation des données
    data = {}
    lat, lng = "Na","Na"
    version = "Na"
    #Récupération des infos de la page 
    page = getPageFromUrl(car)
    #Récupération du texte descriptif et recherche du nom de version et du numéro de telephone
    Text_Description = page.select(".AdviewContent .content")[0].text
    version = FindModel(Text_Description)
    phone = getPhoneInText(Text_Description)

    #Récupération des infos dans le reste de l'annonce et mise en forme 
    name = page.find('h2',id='ad_subject').text
    basics_Infos = page.select(".lbcParams.criterias table")
    carburant = basics_Infos[0].find("th",text="Carburant :").next_sibling.next_sibling.text.strip()
    boite  = basics_Infos[0].find("th",text="Boîte de vitesse :").next_sibling.next_sibling.text.strip()
    year =  basics_Infos[0].find("th",text="Année-modèle :").next_sibling.next_sibling.text.strip()
    kms =  basics_Infos[0].find("th",text="Kilométrage :").next_sibling.next_sibling.text.replace("KM","").replace(' ','')
    price = page.select(".price span")[0].text.replace(u'\xa0',u'').replace(u'€',u'').replace(' ','')
    town =  page.select(".lbcParams.withborder table")[0].find("th",text="Ville :")
   
    #Récupération du vrai nom du modèle    
    FullName = ModelesVersions[(ModelesVersions.Boite == boite)&(ModelesVersions.Energie ==carburant)&(ModelesVersions.Version==version)]
    if len(FullName)>0:
        version =  FullName['FullModele'].iloc[0]    
    else:
        version = None
    #Récupération des coordonnées de la ville si elle est mentionnée
    if town:
        town=town.next_sibling.next_sibling.text.strip()
        lat,lng = getTownCoordinates(town)
        
    #Récupération du type de vendeur
    seller = page.select(".upload_by .ad_pro")
    if len(seller)>0:
        seller="Pro"
    else:
        seller="Particulier"

    #Stocage des informations dans un dictionnaire
    data['url'] = car
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

    return data
    
    

    
    

    

########################TOOLS FUNCTIONS#############################
    
#Giving the description text, retrieves the phone number of the seller
def getPhoneInText(text):
    #Trouve 1 numéro sous la forme 0123456789 ou 01-23-45-67-89
    regex= re.compile("0\d{9}|0\d((-|.)\d{2}){4}")
    phone = regex.search(text)
    
    #Si trouvé, on récupère le match
    if phone :
        phone = phone.group(0)
        
    return phone
    
    
#Mise en forme des noms des régions pour la recherche
def NormalizeRegions(rawList):
    pattern = re.compile(r"\s|\'|-")    
    cleanedList=[]
    for rawString in rawList:
        cleanString = rawString.lower().strip()
        cleanString=pattern.sub("_",cleanString)
        cleanedList.append(cleanString)
    return cleanedList

#Mise en forme de la recherche pour pouvoir l'incorporer dans la requete HTML
def NormalizeQuery(query):
    return query.replace(' ','+')

#Effectue la recherche pour une région et 1 modèle
def getPageResult(region,model):
    url = 'http://www.leboncoin.fr/voitures/offres/'+region+'/?f=a&th=1&q='+model    
    return getPageFromUrl(url)
    
#Retourne le code html de la page d'une URL
def getPageFromUrl(url):
    page= requests.get(url)
    prettypage= BeautifulSoup(page.text)
    return prettypage

#Returns the coordinates of the town
def getTownCoordinates(town):
    token ="AIzaSyAxu2GEhusJPMwMBsQs6scZJlhmX39WGy0"
    url='https://maps.googleapis.com/maps/api/geocode/json?address='+town+'&region=fr&key='+token
    x,y="Na","Na"    
    results = requests.get(url)
    if results.status_code==requests.codes.ok:
        geo = results.json()
        coordinates = geo['results'][0]['geometry']['location']
        x,y = coordinates['lat'], coordinates['lng']
    return x,y
    
#Trouve l'un des modèles et le retourne sous forme majuscule
def FindModel(text):
    Regex  = re.compile(r"(?i)arizona|business|intens|zen|life")
    results = Regex.search(text)
    if results: 
            return results.group(0).upper()
    else : return None

########################EXECUTION#############################

results,Prices, Argus = Main()
results.to_excel("ResultatsExcel.xlsx")
results.to_csv("ResultatsCSV.csv")