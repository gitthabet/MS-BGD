# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 03:22:15 2014

@author: thabetchelligue
"""


import requests
import json
import html5lib
from bs4 import BeautifulSoup
import re
import unicodedata
import numpy
import pandas

## Get Soup	
def getSoupFromUrl(url):
	res = requests.get(url)
	if res.status_code == 200:
         return BeautifulSoup(res.text)
		
	else:
         return None

## Get Cote Argus	    

def getCote():
    
    argus_km=[]
    argus = []
    url = ["http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+arizona+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+intens+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+life+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+zen+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+arizona+edc-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+intens+edc-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+zen+edc-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+arizona+edc+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+business+edc-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+arizona+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+business+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+intens+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+life+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+zen+eco2-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+intens+edc-2013.html",
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+zen+edc-2013.html"]
    for lien in url:
         soupeArgus = getSoupFromUrl(lien)
         cote = int( re.sub('\D{1}', '', soupeArgus.find('span', class_="Result_Cote").text) )
         argus.append(cote)
         grilleString=soupeArgus.find(class_="txnoir tx11").text[6:][:5]
         grille=int(grilleString)
         argus_km.append(grille)
  
    return argus,argus_km
   
## Get Coordonnées Géographiques
    
def getGeocodeMap(ville):
    key ="AIzaSyAB6oLMw8sSbqpGqOvPXfpNNZQg3O0UEJY"
    url='https://maps.googleapis.com/maps/api/geocode/json?address='+ville+'&region=fr&key='+key
    latitude,longitude=0.,0.    
    results = requests.get(url)
    if results.status_code==requests.codes.ok:
        geo = results.json()
        coordinates = geo['results'][0]['geometry']['location']
        latitude,longitude = coordinates['lat'], coordinates['lng']
    return latitude,longitude
    
## Get Cars
    
def getCars(region):
	#CHERCHER TOUS MES LINKS
	links=[]
	url='http://www.leboncoin.fr/voitures/offres/'+region+'/'
	soupCar=getSoupFromUrl(url)
	#print soupCar.prettify()
	encadrer=soupCar.find('body')
	#print encadrer
	balise_div=encadrer.find('div', class_='list-lbc')
	#print balise_div
	#print balise_div('a')[0]['href']
	i=0
	n=len(balise_div('a'))
	#print n
	for i in range(n):		
		links.append(balise_div('a')[i]['href'])
	#afficher le nombre de pages
	balise_li=soupCar.find_all('li')
	#print balise_li[-1]
	liendernierepage=balise_li[-1]('a')[0]['href']
	#print liendernierepage
	nbpage=liendernierepage[-18:-16]
	#print nbpage
	if str(nbpage[1])=='&':
		nbpage=nbpage.replace('&',' ')
	nbpage=int(nbpage)
	#print nbpage
	for j in range(nbpage-1):
		soupCar=getSoupFromUrl(url,j+1)
		#print soupCar.prettify()
		encadrer=soupCar.find('body')
		#print encadrer
		balise_div=encadrer.find('div', class_='list-lbc')
		#print balise_div
		#print balise_div('a')[0]['href']
		i=0
		n=len(balise_div('a'))
		#print n
		for i in range(n):		
			links.append(balise_div('a')[i]['href'])
	#print len(links)
	#creation de la data frame
	columns=['Version', 'Année', 'Kilométrage', 'Prix', 'Téléphone', 'Flag professionnel','Ville', 'Codepostal']
	df=pd.DataFrame(index=np.zeros(10), columns=columns)
	#df=df.fillna(0)
	#print df
	df=pd.DataFrame()
	#GESTION DE MES LINKS:
	for newlink in links:
		souplink=getSoupFromUrl(newlink)
		#print souplink
		elementLink={}
		prix=souplink.find('span', class_='price').text
		#print int(prix.replace(u'\u20ac', u' ').replace(' ' ,''))
		elementLink['Prix']=int(prix.replace(u'\u20ac', u' ').replace(' ' ,''))
		body=souplink.find_all('td')
		#print len(body)
		ville=body[1].text
		#print ville
		elementLink['Ville']=ville
		codepostal=body[2].text
		#print codepostal
		elementLink['Codepostal']= codepostal
		#print annee.strip()
		if len(body)==9:
			annee=body[4].text
			elementLink['Année']=annee.strip()
		if len(body)<9:
			annee=body[3].text
			elementLink['Année']=annee.strip()			
		else:
			annee=body[5].text
			elementLink['Année']=annee.strip()
		#print body
		if len(body)==9:
			kilometre=body[5].text
			if str(kilometre)=='Diesel':
				kilometre=body[4].text
			if str(kilometre)=='Essence':
				kilometre=body[4].text
			kilometre=int(kilometre.replace('KM' ,'').replace(' ' ,''))
			elementLink['Kilométrage']=kilometre
		if len(body)<=8:
			kilometre=body[4].text
			if str(kilometre)=='Diesel':
				kilometre=body[3].text
			if str(kilometre)=='Essence':
				kilometre=body[3].text
			kilometre=int(kilometre.replace('KM' ,'').replace(' ' ,''))
			elementLink['Kilométrage']=kilometre
		else:
			kilometre=body[6].text
			if str(kilometre)=='Diesel':
				kilometre=body[5].text
			if str(kilometre)=='Essence':
				kilometre=body[5].text
			kilometre=int(kilometre.replace('KM' ,'').replace(' ' ,''))
			elementLink['Kilométrage']=kilometre
		myVar=souplink.find('span', class_='ad_pro')
		#if myVar in globals():
		if str(myVar)=='<span class="ad_pro">Pro Véhicules</span>':
			pro=souplink.find('span', class_='ad_pro').text
			elementLink['Flag professionnel']='Oui'
			#print 'bla', pro
		else:
			elementLink['Flag professionnel']='Non'
		version=souplink.find('h2', id="ad_subject")
		#print version.text
		elementLink['Version']=version.text
		#print elementLink
		#tel=souplink.find('img', class_='AdPhonenum')
		#print tel
		df=df.append(elementLink,ignore_index=True)
	#print df
	return df


getCars('ile_de_france')
getCars('provence_alpes_cote_d_azur')
getCars('aquitaine')


concat=getCars('ile_de_france')+getCars('provence_alpes_cote_d_azur')+getCars('aquitaine')
#print concat
concat.to_csv('myalldata.csv', encoding='utf-8')

