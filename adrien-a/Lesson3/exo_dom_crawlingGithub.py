# -*- coding: utf-8 -*-

import html5lib
import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np


# Donne l'objet soup correspondant à l'url spécifiée
def getSoupFromUrl(url) :
	webPage = requests.get(url)
	if webPage.status_code != 200 :
		print "Failure of the request on web page : " + url

	return BeautifulSoup(webPage.text, 'html5lib')


# Donne le nombre de pages d'une requête (donc d'une url) sur l'api Github 
def getNumberOfPageResults(apiUrl) :

	# Récupération des infos pagination contenues dans le header 
	webPage = requests.get(apiUrl)
	header = webPage.headers
	
	if 'link' in header :
		
		paginationInfos = header['link']
		
		# Ce n'est pas dans un format très friendly => utilisation des regex...
		return int( re.search('page=([0-9]*)>; rel="last"', paginationInfos).group(1) )

	else : 

		return 1


# Retourne la liste des 256 top users de Github 
def getTopUsersOfGithub() : 

	soup = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
	userLinkTags = soup.select('th + td a')
	return [link.text for link in userLinkTags]


def getUserInfos(user) :
	
	token = '02d1ee0de1655df097dfbaeb10a8727dd0012e6f'

	# Obtention du nombre de pages que contient le resultat de la requête
	url = 'https://api.github.com/users/' + user + '/repos?access_token=' + token + '&per_page=100'
	nbResultPages = getNumberOfPageResults(url) 

	# Parcours de toutes les pages pour obtenir un objet python contenant TOUS les repositories
	finalJsonResult = []
	for i in range(1, nbResultPages+1) : 
		finalJsonResult = finalJsonResult +  json.loads( getSoupFromUrl(url + '&page=' + str(i)).text ) 

	stargazersCountList = [item['stargazers_count'] for item in finalJsonResult]
	
	# Si le top user n'a pas de repository public on met son nombre moyen de stars à 0 
	meanStars = np.mean(stargazersCountList) if len(stargazersCountList) > 0 else 0
	
	returnObject = {'user': user, 'meanOfStars': meanStars}
	print returnObject

	return returnObject



# Récupération des top users
topUsers = getTopUsersOfGithub()

# Obtention de leur stars moyen 
stargazersCountOfTopUsers = [ getUserInfos(user) for user in topUsers ]

# Tri en fonction de leur nombre moyen de stars 
sortedData = sorted( stargazersCountOfTopUsers, key = lambda userDict : userDict['meanOfStars'], reverse=True)

# Affichage
print '\n\nAffichage de la liste totale triée : \n\n' 
for userObject in sortedData : 
	print 'User : ' + userObject['user'] + ' => nombre moyen de stars : ' + str(userObject['meanOfStars'])
