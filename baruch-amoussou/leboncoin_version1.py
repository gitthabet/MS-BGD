# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 16:45:06 2014

@author: Baruch
"""

import requests
import urllib2
from bs4 import BeautifulSoup
import sys
import html5lib


##################Requete request#########"""

###Récupération des liens annonces de la première page #############
listRegion=['ile_de_france','aquitaine']
for region in listRegion:   
    resultat = requests.get('http://www.leboncoin.fr/voitures/offres/'+region+'/?f=a&th=1&q=Renault+Captur+')
    resultat.text

Soup1 = BeautifulSoup(resultat.text)

Annonce_rzoe = Soup1.find(class_="list-lbc").find_all('a')

for Annonce in Annonce_rzoe:
    lien_annonce = Annonce.get("href")
    lien_annonce_voiture = lien_annonce
    print lien_annonce
    
###########Récupération des liens annoncees des autres pages 
########## J'ai compté manuellement le nbre de page à 9
nbre_page = 2
list_url = []

while nbre_page<10:
    string_page=str(nbre_page)
    list_url.append['http://www.leboncoin.fr/voitures/offres/ile_de_france/?o='+string_page+'&q=Renault%20Captur'] 
    nbre_page =nbre_page + 1     
print list_url

for url in list_url:
    resultat1 = requests.get(url)
    Soup2 = BeautifulSoup(resultat1.text)
    Annonce_rzoe1 = Soup2.find(class_="list-lbc").find_all('a')
    for Annonce in Annonce_rzoe:
        lien_annonce = Annonce.get("href")
        lien_annonce_voiture = lien_annonce
        print lien_annonce
        
####Récupération des prix, kilométrage, modèle des annonces page 1 ############
for lien in lien_annonce:
    resultat3 = requests.get(lien)
    soup3 = BeautifulSoup(resultat3.text)
    prix_voit = soup3.find_all("span", class_="price")
    kilom = soup3.find_all("td")

####Récupération des prix, kilométrage, modèle des annonces des pages restantes ############




