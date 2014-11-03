# -*- coding: utf-8 -*-
#cd Desktop/MS-BGD/Kit-BigData/Lesson-5/

import requests
from bs4 import BeautifulSoup
import html5lib
import numpy as np
import pandas as pd

# Returns a soup object from a given url
def getSoupFromUrl1(url,page):
	payload = {'o': page , 'q': 'Renault+captur'}
	result = requests.get(url, params=payload)
	#print 'voilaaa', result.text
	#print result.url
	if result.status_code == 200:
		#print 'Request succesful'
		return BeautifulSoup(result.text, "html5lib")
	else:
		print 'Request failed', url
		return None
def getSoupFromUrl(url):
	result = requests.get(url)
	if result.status_code == 200:
		#print 'Request succesful'
		return BeautifulSoup(result.text)
	else:
		print 'Request failed', url
		return None


def getAllCars(region):
	#CHERCHER TOUS MES LINKS
	links=[]
	url='http://www.leboncoin.fr/voitures/offres/'+region+'/'
	soupCar=getSoupFromUrl1(url,1)
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
		soupCar=getSoupFromUrl1(url,j+1)
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
	#df=pd.DataFrame(index=np.zeros(10), columns=columns)
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


getAllCars('ile_de_france')
getAllCars('provence_alpes_cote_d_azur')
getAllCars('aquitaine')


concat=getAllCars('ile_de_france')+getAllCars('provence_alpes_cote_d_azur')+getAllCars('aquitaine')
#print concat
concat.to_csv('myalldata.csv', encoding='utf-8')