import requests
from bs4 import BeautifulSoup
import re

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
#        print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getAllHackers():
    soupYoutube = getSoupFromUrl('https://news.ycombinator.com/')
    balises_a = soupYoutube.find_all("a")
    links = [balise.get('href') for balise in balises_a]
#    print 'Here are the links', links

    link = links[0]
    
    for link in links:
#        print link
        if re.search("(user).*",link) :
#           print link
            print 'https://news.ycombinator.com/' +link
            soupPage = getSoupFromUrl('https://news.ycombinator.com/' +link)
            name = soupPage.find_all('td', text='user:')[0].parent.select("td:nth-of-type(2)")[0].string
            karma = soupPage.find_all('td', text='karma:')[0].parent.select("td:nth-of-type(2)")[0].string
            print 'user ', name, ' karma  ', karma



getAllHackers()

