# -*- coding: utf-8 -*-

import html5lib
import requests
from bs4 import BeautifulSoup

# Donne l'objet soup correspondant à l'url spécifiée
def getSoupFromUrl(url) :
	webPage = requests.get(url)
	if webPage.status_code != 200 :
		print "Failure of the request on web page : " + url

	return BeautifulSoup(webPage.text, 'html5lib')



# Obtention de la liste des liens utilisateurs de la page 1 
soup = getSoupFromUrl('https://news.ycombinator.com/')
a = soup.find_all('a')
linksPage1 = [ link.get('href') for link in a ]

# Obtention de la liste des liens utilisateurs de la page 2 
soup = getSoupFromUrl('https://news.ycombinator.com/news?p=2')
a = soup.find_all('a')
linksPage2 = [ link.get('href') for link in a ]

# Obtention de la liste des liens utilisateurs de la page 3 
soup = getSoupFromUrl('https://news.ycombinator.com/news?p=3')
a = soup.find_all('a')
linksPage3 = [ link.get('href') for link in a ]

links = linksPage1 + linksPage2 + linksPage3

userLinks = []

for link in links : 
	if link.find('user') != -1 and link.find('blog') == -1 :
				userLinks.append('https://news.ycombinator.com/' + link)

# Pour chaque user on recupere son carma 
users = []
for link in userLinks : 
	userSoup = getSoupFromUrl(userlinks[0])
	try:
		username = userSoup.find_all('td', text='user:')[0].parent.select("td:nth-of-type(2)")[0].string
		karma = userSoup.find_all('td', text='karma:')[0].parent.select("td:nth-of-type(2)")[0].string
		users.append( {'username': username, 'karma': karma} )
	except Exception, e:
		print 'Page inaccessible : ' + link
	

print '\n\nListe des users avec leur karma :\n'
print users

