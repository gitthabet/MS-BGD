import requests
from bs4 import BeautifulSoup
import math

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url

def getlinks(artist):
	result_artist=getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
	balise_artist=result_artist.find_all("a",class_="yt-uix-tile-link")
	links_artist=[balise.get('href') for balise in balise_artist]
	for i,link in enumerate(links_artist):
		if link.count("watch")==0:
			links_artist.pop(i)
	return links_artist

def convertoint(text):
	groupechiffre=text.split()
	tot=0
	for i,c in enumerate(groupechiffre):
		tot+=int(c)*math.pow(1000, abs(i-len(groupechiffre)+1))
	return int(tot)
	
def getmetrics(artist):
	views=[]
	likes=[]
	dislikes=[]
	popularity=0
	viewsT=0
	likesT=0
	dislikesT=0
	for i,link in enumerate(getlinks(artist)):
		pageHTML=getSoupFromUrl('https://www.youtube.com/'+link)
		views.append(convertoint(pageHTML.find_all("div",class_='watch-view-count')[0].text)) 
		likes.append(convertoint(pageHTML.find_all(id='watch-like')[0].text))
		dislikes.append(convertoint(pageHTML.find_all(id='watch-dislike')[0].text))
		popularity+=views[i]*(float(likes[i]-dislikes[i])/float(likes[i]+dislikes[i]))
	for i in range(len(getlinks(artist))):
		viewsT+=views[i]
		likesT+=likes[i]
		dislikesT+=dislikes[i]
	return viewsT,likesT,dislikesT,popularity

def affichage(artist,(a,b,c,d)):
	print "L'artiste est : ",artist
	print "-"*20
	print "Nombre de vues : ",a
	print "Nombre de likes : ",b
	print "Nombre de dislikes : ",c
	print "Popularity : ",long(d)
	print

artist="rihanna"
affichage(artist,getmetrics(artist))
artist="michael jackson"
affichage(artist,getmetrics(artist))
