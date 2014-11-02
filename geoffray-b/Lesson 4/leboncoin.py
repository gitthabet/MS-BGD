

import requests
import html5lib
from bs4 import BeautifulSoup
import json
import pandas as pd

import re
import unicodedata as ucd

def getSoupFromUrl(url):
	result = requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text,"html5lib")
	else:
		print 'Request failed', url
		return None


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
	
	

# Try to find seller's number in description, always in pro , sometimes in private seller

def getSellerPhone(desc):

	regex= re.compile("((\+|00)33\s?|0)[1-9]([\s-.]?\d{2}){4}")
	phone = regex.search(desc)
	if phone :
		phone = phone.group(0)
	
	return phone

# Get the number of items for sale, evaluate the number of pages knowing that 35 links is max/page
def getItemPages(soup):
	
	balise = soup.select('ul li span + span')[0].text
	tab= balise.split()
	nbitems = int(getUniString(tab[-1]))
	# print nbitems
	nbpages = nbitems/35 + 1
	
	return nbpages

# Get normal form of string and encode in ascii
def getUniString(string):
	return ucd.normalize('NFKD',string).encode('ascii','ignore')	




soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&q=Renault%20Captur')
num = getItemPages(soup)
print num

