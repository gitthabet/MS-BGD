# -*- coding: utf-8 -*-
import re
from sets import Set
import json
import operator
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

#Recuperation des cotations sur la centrale.fr
INTENS=Series([1500,17800,17700,17500])
LIFE=Series([12700,14600])
ZEN=Series([14200,16000,16200])
BUSINESS=Series([17600,16100])
MODELES={'intens':INTENS.mean(),'life':LIFE.mean(),'zen':ZEN.mean(),'business':BUSINESS.mean()}

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url

def getURL_Annonces(Region,Page_courante,type):
	return 'http://www.leboncoin.fr/voitures/offres/'+Region+'/?o='+str(Page_courante)+'&q=Renault%20Captur&f='+type

def nbr_pages_parrecherche(Region,type):
	Result=getSoupFromUrl(getURL_Annonces(Region,1,type))
	Balises_a=Result.find_all("a")
	Numeros_pages= Series([int(A.text) for A in Balises_a if A.text.isnumeric()])
	if len(Numeros_pages)==0:
		return 1
	else:
		return Numeros_pages.max()

def getLINKS_Annonces(Region,type):
	Nbr_pages=nbr_pages_parrecherche(Region,type)
	pattern_href=re.compile(r'^(http://www.leboncoin.fr/voitures/)([0-9]{9})')
	pattern_title=re.compile(r'captur',re.IGNORECASE)
	links=Set()
	for i in range(Nbr_pages):
		Result=getSoupFromUrl(getURL_Annonces(Region,i+1,type))
		for ahref in Result.find_all("a", href=pattern_href, title=pattern_title):
			links.add(ahref.get('href'))
	return links

def Type_Renault_Captur(url):
	Result=getSoupFromUrl(url)
	Title=Result.find_all("h2",id='ad_subject')
	if Title[0].text.lower().count("busines")>0:
		return 'business'
	if Title[0].text.lower().count("zen")>0:
		return 'zen'
	if Title[0].text.lower().count("life")>0:
		return 'life'
	if Title[0].text.lower().count("intens")>0:
		return 'intens'
	Content=Result.find_all("div",class_='content')
	if Content[0].text.lower().count("busines")>0:
		return 'business'
	if Content[0].text.lower().count("zen")>0:
		return 'zen'
	if Content[0].text.lower().count("life")>0:
		return 'life'
	if Content[0].text.lower().count("intens")>0:
		return 'intens'
	return ''

def convertoint(text):
	groupechiffre=text.split()
	lg=len(groupechiffre)-1
	tot=0
	for i in range(lg):
			tot+=int(groupechiffre[lg-1-i])*math.pow(1000, i)
	return int(tot)

def API_Google_position(Adresse):

	#Le mieux 92120,France pour adresse
	Adresse_complete=Adresse+',France'
	API='AIzaSyBOjUcK9lw3OPG-YgdyVQ7d_PscohZykVI'
	req=requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+Adresse_complete+'&key='+API)
	json_position=json.loads(req.text)

	#vérifie si il y a bien eu un résultat
	if len(json_position['results'])!=0:
		#dictionnaire 'lat' et 'lng'
		return json_position['results'][0]['geometry']['location']
	else:
		print "Ville non identifiée"

def GetMetrics(url, type):
	
	#Pro ou particulier?
	if type=='c':
		Type='professionnel'
	elif type=='p':
		Type='particulier'
	else:
		print 'erreur dans le type, attendu c ou p'

	#Prix
	Result=getSoupFromUrl(url)
	Result_Prix=Result.find_all("span",class_='price')
	Prix=convertoint(Result_Prix[0].text)

	#Ville, Code postal, Annee, kilometrage
	Metrics=Result.find_all("td")
	Ville, CodeZIP, Annee, Km=Metrics[1].text,Metrics[2].text,Metrics[5].text.strip(),convertoint(Metrics[6].text)

	#Telephone Proprio
	Result_tel=Result.find_all("div", class_="content")
	pattern_tel=re.compile(r'(\d{10})')
	if len(pattern_tel.findall(Result_tel[0].text))!=0:
		Tel=pattern_tel.findall(Result_tel[0].text)[0]
	else:
		Tel=''

	#Longitude et latitude
	position=API_Google_position(CodeZIP)
	Latitude=position['lat']
	Longitude=position['lng']

	#Type de vehicule
	Modele=Type_Renault_Captur(url)

	#Superieur ARGUS?
	if Modele=='':
		ARGUS=''
	else:
		if Prix>MODELES[Modele]:
			ARGUS='Sup_Argus'
		elif Prix<MODELES[Modele]:
			ARGUS='Inf_Argus'
		else:
			ARGUS='Eq_Argus'

	return Ville, CodeZIP, Latitude, Longitude, Type, Tel, Modele, Annee, Prix, Km, ARGUS

def main():

	Region='aquitaine'

	df = DataFrame([])
	for Statut in ['c','p']:
		for url in list(getLINKS_Annonces(Region,Statut)):
			h = Series(list(GetMetrics(url, Statut)))
			print h
			df=df.append(h,ignore_index=True)

	col=['Ville', 'CodeZIP', 'Latitude','Longitude','Type','Tel','Modele','Annee','Prix','Km','Argus']
	df.columns=col
	df.to_csv('C:\Users\mochkovitch\GitHub\MS-BGD\paul_m\Lesson5\Aquitaine_RenaultCaptur.csv',encoding='utf-8')

if __name__ == "__main__":
    main()