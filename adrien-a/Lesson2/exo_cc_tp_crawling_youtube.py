# -*- coding: utf-8 -*-

import html5lib
import requests
from bs4 import BeautifulSoup
import sys
import re

# Donne l'objet soup correspondant à l'url spécifiée
def getSoupFromUrl(url) :
	webPage = requests.get(url)
	if webPage.status_code != 200 :
		print "Failure of the request on web page : " + url

	return BeautifulSoup(webPage.text, 'html5lib')

# Donne l'objet metrique d'un artiste
def getArtistMetrics(nomArtiste, nombrePagesResultatsDeRecherche) :
	
	artistMetrics = []

	for currentPage in range(1, nombrePagesResultatsDeRecherche+1) :
		url = 'https://www.youtube.com/results?search_query=' + nomArtiste + '&page=' + str(currentPage)
		soup = getSoupFromUrl(url)

		# Extraction des liens des vidéos de cette page de recherche
		a = soup.find_all('a', class_="yt-uix-tile-link")
		links = [ link.get('href') for link in a ]

		cleanLinks = []
		# Nettoyage des liens pour ne garder que les watch
		for i in range(len(links)) :
			if links[i].find('watch') != -1 :
				cleanLinks.append(links[i])

		# Exploration de ces liens pour determiner le nb de vues, likes et dislikes
		for link in cleanLinks : 
			title, views, likes, dislikes = getMetricsFromOneVideo('https://www.youtube.com' + link)
			tmpMetrics = {'title': title, 'views': views, 'likes': likes, 'dislikes': dislikes}
			artistMetrics.append(tmpMetrics)

	return artistMetrics


# Retourne les metriques (titre, vues, likes, dislikes) de l'url spécifiée
def getMetricsFromOneVideo(urlVideo) :
	soup = getSoupFromUrl(urlVideo)

	# Récupération des données brutes
	title = soup.title.text
	views = soup.find_all(class_='watch-view-count')[0].text.encode('ascii', 'ignore')
	likes = soup.find_all(id='watch-like')[0].text.encode('ascii', 'ignore')
	dislikes = soup.find_all(id='watch-dislike')[0].text.encode('ascii', 'ignore')

	# Tests pour détecter les chaines de caractères vides et conversion en int
	views = int( re.sub('[ .a-zA-Z]', '', views) ) if views else 0
	likes = int(likes) if likes else 0
	dislikes = int(dislikes) if dislikes else 0

	return (title, views, likes, dislikes)


# Calcule le score de l'artiste
def computeScoreFromMetrics(artistMetrics) :

	score = 0
	for m in artistMetrics :
		if (m['likes'] + m['dislikes']) > 0 :
			coeff =  float(m['likes'] - m['dislikes']) / float(m['likes'] + m['dislikes'])
			score += m['views']*coeff
		else : 
			score += m['views']*0.5 

	return int(score)


# Retourne le score de l'artiste
def getArtistScore(nomArtiste, nombrePagesResultatsDeRecherche) :
	artistMetrics = getArtistMetrics(nomArtiste, nombrePagesResultatsDeRecherche)
	return computeScoreFromMetrics(artistMetrics)


# Affichage des résultats
def printResults(nomArtiste1, scoreArtiste1, nomArtiste2, scoreArtiste2) :
	
	# Affichage des scores des protagonistes
	print "\n" + nomArtiste1 + " : " + '{:,}'.format(scoreArtiste1).replace(',', ' ')
	print nomArtiste2 + " : " + '{:,}'.format(scoreArtiste2).replace(',', ' ')

	# Affichage du vainqueur
	if scoreArtiste1 > scoreArtiste2 : print "\n=> Victoire de " + nomArtiste1
	if scoreArtiste2 > scoreArtiste1 : print "\n=> Victoire de " + nomArtiste2
	if scoreArtiste1 == scoreArtiste2 : print "\n=> Egalité..."


nomArtiste1 = 'rihanna'
nomArtiste2 = 'beyoncé'
nbPages = 3

scoreArtiste1 = getArtistScore(nomArtiste1, nbPages)
scoreArtiste2 = getArtistScore(nomArtiste2, nbPages)

printResults(nomArtiste1, scoreArtiste1, nomArtiste2, scoreArtiste2)
