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

#soup=getSoupFromUrl('https://news.ycombinator.com/')
#balises= soup.find_all("a", href="user?id=pierre-renaux")
#print balises
#print balises[0]
#links=[balise.get('href') for balise in balises]
#print links
def getKarmaForEachName (name):
	soupPage = getSoupFromUrl('https://news.ycombinator.com/user?id=' +name)
	liste =soupPage.find_all("tbody")
	#print type(liste)
	#print "LISTE", liste[0]
	liste=liste[0]
	#print liste
	listebis=liste.find_all("tr")[3]
	#print "blaaaaaa", listebis.text
	listeter=listebis.find_all("td")[6]
	print "le karma de ", name ,  int(listeter.text)

getKarmaForEachName ('pierre-renaux')
getKarmaForEachName ('iprashantsharma')
getKarmaForEachName ('ot')


#listefiltre=liste.find_all("td")
#listefiltre=liste.find_all("td")
#print  listefiltre
#karma=listefiltre[4].text



