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
