# -*- coding: utf-8 -*-

import html5lib
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import json
import pandas as pd

# Donne l'objet soup correspondant à l'url spécifiée
def getSoupFromUrl(url) :
	webPage = requests.get(url)
	if webPage.status_code != 200 :
		print "Failure of the request on web page : " + url

	return BeautifulSoup(webPage.text, 'html5lib')


# Retourne le nombre de pages de résultats de recherche 
def getNumberOfResultPages(url) : 

	soup = getSoupFromUrl(url)
	paginationBlock = soup.find(id='paging')
	
	# S'il n'y a pas de bloc d'id paging c'est qu'il n'y a qu'une seule page de résultats
	if not paginationBlock :
		return 1 
	# Sinon on extraie le nombre de pages en exploitant le lien vers la dernière page
	else : 
		linkLastPage = paginationBlock.find('a', text='>>').get('href')
		return int( re.search("\?o=([0-9]*)[^0-9]", linkLastPage).group(1) )


# Retourne la liste des liens vers les annonces pour un tuple (marque, modele, region) donné
def getAdvertLinks(brand, model, area) : 

	# Obtention du nombre de pages de résultats 
	url = 'http://www.leboncoin.fr/voitures/offres/' + area + '/?f=a&th=1&q=' + brand + '+' + model + '&it=1'
	numberOfPages = getNumberOfResultPages(url)

	# Boucle sur les pages de résultats pour obtenir les liens de toutes les annonces
	allAdvertsLinks = []
	for currentPage in range(1, numberOfPages+1) :
		
		# Extraction de tous les liens de voitures présent sur cette page
		url = 'http://www.leboncoin.fr/voitures/offres/' + area + '/?o=' + str(currentPage) + '&q=' + brand + '+' + model + '&it=1'	
		soup = getSoupFromUrl(url)
		links = soup.select('.list-lbc a')
		pageAdvertLinks = [ link.get('href') for link in links ]

		# Concaténation avec les liens précédents 
		allAdvertsLinks.extend(pageAdvertLinks)

	return allAdvertsLinks


# Retourne km, an, numéro tel, version, prix, type de vendeur, ville et code postal dans un dict
def getCarAdvertInfos(carAdvertUrl, argusInfo) : 

	carObject = {}
	soup = getSoupFromUrl(carAdvertUrl)

	# Url de l'annonce 
	carObject['url'] = carAdvertUrl

	# Prix 
	rawPrice = soup.select(".price span")[0].text
	carObject['price'] = int( re.sub('[^0-9]*', '', rawPrice) )

	# Pro ou particulier
	carObject['pro'] = 1 if soup.find('div', class_='upload_by').select('.ad_pro') else 0

	# Numéro de téléphone (à partir de la description)
	description = soup.find('div', class_='content').text.lower()
	carObject['phoneNumber'] = getPhoneNumberFromDescription(description)

	# Infos relatives à la version (toujours à partir de la description)
	carObject['version'] = getVersionFromDescription(description, argusInfo.keys())
	carObject['argus'] = argusInfo[ carObject['version'] ]
	carObject['cheaperThanArgus'] = 1 if carObject['price'] < carObject['argus']  else 0

	# Infos plus génériques
	infos = ['Ville :', 'Code postal :', 'Marque :', 'Modèle :', 'Année-modèle :', 'Kilométrage :', 'Carburant :', 'Boîte de vitesse :']
	infoTypes = ['str', 'str', 'str', 'str', 'int', 'int', 'str', 'str']
	keys = ['town', 'zipCode', 'brand', 'model', 'modelYear', 'km', 'oil', 'gearbox']
	
	for i in range(0, len(infos)) :

		# Présence de la donnée => récupération brute, nettoyage et enregistrement
		try:
			rawData = soup.find('th', text=infos[i]).parent.select('th + td')[0].text
			carObject[keys[i]] = rawData.lower().strip() if infoTypes[i] == 'str' else int( re.sub('[^0-9]*', '', rawData) )
		
		# Abscence de la donnée => signalement par un NaN
		except Exception, e:
			carObject[keys[i]] = np.nan

	# Obtention des coordonnées GPS à partir du nom de la ville et de son code postal
	(latitude, longitude) = getCoordinatesFromTown(carObject['town'], carObject['zipCode'])
	carObject['latitude'] = latitude
	carObject['longitude'] = longitude 

	return carObject 


# Retourne le numéro de téléphone à partir de la description d'une annonce 
def getPhoneNumberFromDescription(description) :

	# On cherche une chaine de type numéro de tel
	regex = '(\D{1}((0\d (\d\d ){3}\d\d)|(0\d\.(\d\d\.){3}\d\d)|(0\d-(\d\d-){3}\d\d)|(0\d(\d\d){4}))\D{1})'
	regexSearchObject = re.search(regex, description)

	# S'il y a une occurence on la renvoie dans un format normalisé sinon on le signale via le marqueur NaN
	if regexSearchObject :
		rawPhoneNumber = regexSearchObject.group(0)
		return re.sub('\D{1}', '', rawPhoneNumber) 
	else :
		return np.nan


# Retourne le modèle à partir de la description d'une annonce
def getVersionFromDescription(description, listOfVersions) :

	mostSimilarVersion = ''
	highestSimilarity = -1

	for version in listOfVersions : 

		# Extraction de tous les éléments du nom de la version 
		termsOfVersion = version.lower().split(' ')
		nbWordsInVersionName = len(termsOfVersion)
		nbWordsInVersionNameInDescription = 0

		# On compte le nombre de mots du modèle présents dans la description
		for versionWord in termsOfVersion :
			if versionWord in description :
				nbWordsInVersionNameInDescription += 1

		# Quelle proportion des mots du modèle sont présents dans la description
		if nbWordsInVersionNameInDescription > 0 :
			similarity = float(nbWordsInVersionNameInDescription) / float(nbWordsInVersionName)
		else :
			similarity = 0

		# Actualisation de la version qui colle le plus à la description si besoin
		if similarity > highestSimilarity : 
			highestSimilarity = similarity
			mostSimilarVersion = version

	return mostSimilarVersion


# Retourne les coordonnées GPS à partir du nom de la ville et de son code postal 
def getCoordinatesFromTown(town, zipCode) :

	apiKey = 'AIzaSyD0Je91FF7XuGcaTwNqH4apLq86DaM7fWc'
	
	# Adaptation de l'url vers l'api en fonction des infos dont on dispose
	if pd.isnull(town) and pd.isnull(zipCode) :
		return (np.nan, np.nan)
	elif pd.isnull(town) :
		url = 'https://maps.googleapis.com/maps/api/geocode/json?components=postal_code:' + str(zipCode) + '&key=' + apiKey
	elif pd.isnull(zipCode) : 
		url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + town + '&key=' + apiKey
	else :
		url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + town + '&components=postal_code:' + str(zipCode) + '&key=' + apiKey

	# Obtention du json contenant la latitude et la longitude de la ville
	jsonObject = json.loads( getSoupFromUrl(url).text )

	# Obtention de la latitude et de la longitude 
	latitude = jsonObject['results'][0]['geometry']['location']['lat']
	longitude = jsonObject['results'][0]['geometry']['location']['lng']
	return ( latitude, longitude )


# Retourne la liste des différentes versions d'un modèle de voiture donné
def getAllCarVersionsArgus(brand, model) :

	url = 'http://www.lacentrale.fr/cote-voitures-renault-captur--2013-.html'
	soup = getSoupFromUrl(url)

	# Obtention des liens vers les différents modèle
	tdContainers = soup.find_all('td', class_="tdSD QuotMarque")
	balisesA = [ td.select('a')[0] for td in tdContainers ]
	links = ['http://www.lacentrale.fr/' + link.get("href") for link in balisesA]
	models =  [link.text for link in balisesA]

	# Pour chaque lien on récupère le nom du modèle et son prix
	argus = {}
	for i in range(0, len(links)) :
		soupCurrentModel = getSoupFromUrl(links[i])
		currentArgus = int( re.sub('\D{1}', '', soupCurrentModel.find('span', class_="Result_Cote").text) )
		argus[ models[i] ] = currentArgus

	return argus


brand = 'renault'
model = 'captur'
potentialAreas = ['aquitaine', 'provence_alpes_cote_d_azur']
argus = getAllCarVersionsArgus(brand, model)

# Obtention de tous les liens vers des annonces LeBonCoin qui nous intéressent
allAdvertsLinks = []
for area in potentialAreas :
	allAdvertsLinks.extend( getAdvertLinks(brand, model, area) )

# Obtention de toutes les infos contenues dans ces annonces 
allCarsInfos = []
for link in allAdvertsLinks :
	carInfos = getCarAdvertInfos(link, argus)
	allCarsInfos.append(carInfos)

# Ecriture de toutes ces infos dans un csv
columnsName = ['version', 'modelYear', 'km', 'price', 'phoneNumber', 'pro', 'argus', 'cheaperThanArgus', 'latitude', 'longitude']
infoAboutAllCars = pd.DataFrame(allCarsInfos, columns=columnsName)
infoAboutAllCars.to_csv('adverts.csv', encoding='utf-8')
