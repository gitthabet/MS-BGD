import requests
from bs4 import BeautifulSoup
import html5lib

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

soup=getSoupFromUrl('https://news.ycombinator.com/')
balises= soup.find_all("a", href="user?id=pierre-renaux")
#print balises
#print balises[0]
#links=[balise.get('href') for balise in balises]
#print links
link='pierre-renaux'
soupPage = getSoupFromUrl('https://news.ycombinator.com/user?id=' +link)
liste =soupPage.find_all("tr")
listefiltre=liste.find_all("td")
print  listefiltre
karma=listefiltre[4].text



