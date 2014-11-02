

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
	return ucd.normalize('NFKD',string).encode('utf-8','ignore')	


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

def getSellerPhone(desc):

	regex= re.compile("((\+|00)33\s?|0)[1-9]([\s-.]?\d{2}){4}")
	phone = regex.search(desc)
	print phone
	# if phone :
	# 	phone = phone.group(0)
	# return phone

def getSellerInfo(soup):
	Seller =[]
	sell=soup.find('div', class_="upload_by")
	name=getUniString(sell.find('a').text)
	print name
	pro= getUniString(soup.find('span', class_="ad_pro").text)
	
	desc= getUniString(soup.find('div', class_="content").text)
	#print desc
	# phone=getSellerPhone('desc')
	
	return Seller.append([name, pro ,phone])



def getCarInfo(url):
	
	soup = getSoupFromUrl(url)
	price = getUniString(soup.find('span', class_="price").text)
	print price

	Infos = soup.select('.lbcParams.criterias table')
	# test = Infos.find('th', text="Ann&eacute;e-mod&egrave;le :")
	print Infos.find("th", text="Kilom&eacute;trage :").

# soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/726730103.htm?ca=12_s')
# getSellerInfo(soup)
getCarInfo('http://www.leboncoin.fr/voitures/726736296.htm?ca=12_s')
# liens = []
# liens = getItemlinks('ile_de_france','Renault%20Captur')
# print liens[3]

