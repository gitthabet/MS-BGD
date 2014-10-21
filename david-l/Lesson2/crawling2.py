import requests
from bs4 import BeautifulSoup
# Returns a soup object from a given url
def getSoupFromUrl(url):
	result = requests.get(url)
	if result.status_code == 200:
		print 'Request succesful'
		return BeautifulSoup(result.text)
	else:
		print 'Request failed', url
		return None

soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query=rihanna')
balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
links = [balise.get('href') for balise in balises_a]
print 'Here are the links', links
links.pop(0)
link = links[0]
soupPage = getSoupFromUrl('https://www.youtube.com' +link)
print soupPage.title

likesCount = soupPage.find_all(id='watch-like')[0].text
dislikesCount = soupPage.find_all(id='watch-dislike')[0].text
viewCount = soupPage.find_all(id='watch-view-count')[0].text

likesCount = int(likesCount.replace(u'\xa0',u' ').replace(u' ', u''))
dislikesCount = int(dislikesCount.replace(u'\xa0',u' ').replace(u' ', u''))
viewCount = int(viewCount.replace(u'\xa0',u' ').replace(u' ', u''))


metrics = {}
metrics['views_count'] = viewCount
metrics['dislikes_count'] = viewCount
metrics['likes_count'] = viewCount



