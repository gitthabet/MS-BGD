# -*- coding: utf-8 -*-

import requests
import html5lib
from bs4 import BeautifulSoup
import json
import pandas as pd

import re
import unicodedata as ucd

# Returns a soup object from a given url

def getSoupFromUrl(url):
	result = requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text,"html5lib")
	else:
		print 'Request failed', url
		return None

# Get normal form of string and encode in utf-8

def getUniString(string):
	return ucd.normalize('NFKD',string).encode('ascii','ignore')	


# Returns the coordinates using google geoloc API

def getCoordinates(city):
	
	token ="AIzaSyBv0WT6o0l9ywxmlOmVw2s4acoj_t57Up4"
	url='https://maps.googleapis.com/maps/api/geocode/json?address='+city+'&region=fr&key='+token
	results = requests.get(url)
	if (results.ok):
		repoItem = json.loads(results.text)
		lat = repoItem['results'][0]['geometry']['location']['lat']
		lng = repoItem['results'][0]['geometry']['location']['lng']
		coordinate = [str(lat),str(lng)]
		return coordinate
	
######################################################################################################################

# Get the number of items for sale, evaluate the number of pages knowing that 35 links is max/page

def getTotalPages(soup):
	
	balise = soup.select('ul li span + span')[0].text
	tab= balise.split()
	nbitems = int(getUniString(tab[-1]))
	# print nbitems
	nbpages = nbitems/35 + 1
	
	return nbpages


# Get item's links from search in a given region

def getItemlinks(region,search):
	soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/'+region+'/?q='+ search)
	pages = getTotalPages(soup)
	links=[]

	for i in range(1,pages):
		soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+ str(i) + '&q='+ search)
		listItem = soup.find('div', class_="list-lbc")
		urlItem = listItem.find_all('a')
		links += [getUniString(link.get('href'))for link in urlItem]
	return links


######################################################################################################################	

# Try to find seller's number in description, always in pro , sometimes in private seller

def getSellerInfo(soup):
	Seller =[]
	sell=soup.find('div', class_="upload_by")
	name=getUniString(sell.find('a').text)
	#print name

	pro= getUniString(soup.find('span', class_="ad_pro").text)
	if len(pro)>0:
		pro ="Professionnel"
	else:
		pro ="Particulier"
	#print pro
	desc= getUniString(soup.find('div', class_="content").text)
		
	regex= re.compile(r"((\+|00)33\s?|0)[1-9]([\s\-\.]?\d{2}){4}")
	phone = regex.search(desc)
	if phone :
	 	phone = phone.group(0)
	#print phone

	return Seller.append([name, pro ,phone])



def getCarInfo(soup):
	
	price = int(getUniString(soup.find('span', class_="price").text).replace(' ',''))
	# print type(price)
	# print price
	Infos = soup.find('div', class_="lbcParams criterias").find_all("td")
	#print type(Infos)
	#print Infos
	manufacturer = Infos[0].text
	model = Infos[1].text
	year = Infos[2].text.strip()
	#print year
	mileage = Infos[3].text
	#print mileage
	energy = Infos[4].text
	gear = Infos[5].text
	
	CarInfo=[]
	return CarInfo.append([manufacturer,model,year,mileage,energy,gear])


vendeur=[]
soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/716161502.htm?ca=12_s')
#print soup
# vendeur = getSellerInfo(soup)
# print vendeur
CarInfo= getCarInfo(soup)
print vendeur
# getCarInfo('http://www.leboncoin.fr/voitures/726736296.htm?ca=12_s')
# liens = []
#liens = getItemlinks('ile_de_france','Renault Captur')
#print liens[3]

