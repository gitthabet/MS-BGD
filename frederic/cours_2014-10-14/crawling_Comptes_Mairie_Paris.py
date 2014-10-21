import requests
from bs4 import BeautifulSoup
import re
#from tinycss.css21 import CSS21Parser

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print  (result.text)
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


soupYoutube = getSoupFromUrl('http://www.paris.fr/politiques/documents-legaux/budget/p9825')
#    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
   # links = [balise.get('href') for balise in balises_a]

  
   


