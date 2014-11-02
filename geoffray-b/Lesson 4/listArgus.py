
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

# GetArgus
def getArgusVal():
	soup = getSoupFromUrl('http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html')
	Argus_val = []

# find the list of referenced models
	soup1 = soup.find_all('td', class_="tdSD QuotMarque")
	Models = [getUniString(balise.select('a')[0].text) for balise in soup1]

# get the car's energy
	soup2 = soup.find_all('td', class_="tdSD QuotNrj")
	Energy = [getUniString(balise.select('a')[0].text) for balise in soup2]
	

# get the links of models to extract value
	car_links = [getUniString(balise.select('a')[0].get('href')) for balise in soup1]

	CarValue = []
	for i in range(0,len(car_links)):
		soupVal = getSoupFromUrl('http://www.lacentrale.fr/' + car_links[i])
		cote = soupVal.find('span', class_="Result_Cote").text
		CarValue.append(int(getUniString(cote).replace(' ','')))	
		# print CarValue[i]
	




	for i in range(0,len(Models)):
		Argus_val.append([Models[i], Energy[i] ,CarValue[i]])
	return Argus_val


# get normal form of string and encode in ascii
def getUniString(string):
	return ucd.normalize('NFKD',string).encode('ascii','ignore')



ArgusValue = getArgusVal()
dfArgus = pd.DataFrame(ArgusValue,columns = ['Model','Energy','Value'])

# Put DataFrame in CSV file
dfArgus.to_csv('Argus.csv')