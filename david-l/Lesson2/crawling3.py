import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):  
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text)
    else:
        print 'Error: request failed at ', url
        return None



#find_all(name, attrs, recursive, text, limit, **kwargs)
# The find_all() method looks through a tags descendants and retrieves all descendants that 
# match your filters.
# search by CSS class using the keyword argument class_

def getAllMetricsforArtist(artist):
  url = 'https://www.youtube.com/results?search_query=' + artist
  soup = getSoupFromUrl(url)
  balises_a = soup.find_all("a",class_="yt-uix-tile-link")
  links = [balise.get('href') for balise in balises_a]
  print 'Here are the links', links
  links.pop(1) #pop first link (link to artist's channel)
#Note: The 'u' in front of the string values means the string has been represented as unicode. 
#It is a way to represent more characters than normal ascii can manage.

  url = 'https://www.youtube.com'
  all_metrics = []
  for link in links:
		soupPage = getSoupFromUrl(url+link)
		likes_count = soupPage.find_all(id='watch-like')[0].text	
		dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
		views_count = soupPage.find_all(class_='watch-view-count')[0].text
		dislikes_count = int(dislikes_count.replace(u'\xa0', u' ').replace(' ' ,''))
		likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))
		views_count = int(views_count.replace(u'\xa0', u' ').replace(' ' ,''))
		metrics = {}
		metrics['views_count'] = views_count
		metrics['dislikes_count'] = dislikes_count
		metrics['likes_count'] = likes_count
		metrics['title'] = soupPage.title.text
		print 'Metrics for ', metrics
		all_metrics.append(metrics)
  return all_metrics

rihanna = getAllMetricsforArtist('Rihanna')
beyonce = getAllMetricsforArtist('Beyonce')

