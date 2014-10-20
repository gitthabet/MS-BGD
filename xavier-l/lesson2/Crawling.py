import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
	result = requests.get(url)
	if result.status_code == 200:
		print 'Request succesful'
		return BeautifulSoup(result.text)
	else:
		print 'Request failed', url
		return None

soup = getSoupFromUrl('https://www.youtube.com/results?search_query=rihanna')
balise_a = soup.find_all("a", class_='yt-uix-tile-link')
#    for balise in balise_a:
#   	print balise.text
links = [balise.get('href') for balise in balise_a]
links.pop(0)

link = links[0]
soupPage = getSoupFromUrl('https://www.youtube.com'+link)
likes_count = soupPage.find_all(id='watch-like')[0].text
dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
likes_count.replace(u'\xa0',u' ')
likes_count = int(likes_count.replace(u'\xa0',u''))

print likes_count


