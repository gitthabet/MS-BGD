import requests
from bs4 import BeautifulSoup


#returns...

def getSoupFromUrl(url):
	result = requests.get(url)
	if result.status_code==200:
		print 'Request successful'
		return BeautifulSoup(result.text)
	else:
		print 'Request failed', url
		return None
		




result = requests.get('http://www.youtube.com/results?search_query=rihanna')

if result.status_code == 200:
	print 'Request successful'
	soup = BeautifulSoup(result.text)
	balises_a = soup.find_all("a", class_="yt-uix-tile-link") #look for delimiters of type a
	links = [balise.get('href') for balise in balises_a]
	print 'Here are the links', 
	links.pop(0)
	link = links[0]
	pageHTML = requests.get('https://www.youtube.com/ + link').text
	PageSoup = BeautifulSoup(pageHTML)
	print PageSoup.title


else:
	print 'Request failed'

result.text  #recupere tout le code markup du site

##stop