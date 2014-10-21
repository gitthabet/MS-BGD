import requests
# html5lib parser de meilleur qualite
import html5lib
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

""" getMontantABCD recupere les montants states et hab pour les totaux ABCD dans un dictionnaire"""
def users_and_karma(page):
    soupYoutube = getSoupFromUrl('https://news.ycombinator.com/news?p=' + str(page))
    balises_a = soupYoutube.find_all("a")
    links = [balise.get('href') for balise in balises_a]
    """print links"""
    links_users=[]
    for link in links:
        linkp = str(link)
        if 'user' in linkp:
            links_users.append(link)

    for pers in links_users:
        soupYout = getSoupFromUrl('https://news.ycombinator.com/'+ pers)
        print pers
        print soupYout
        balises_karma = soupYout.find_all('td', text='karma:')
        balises_parent = [balise.parent.select("td:nth-of-type(2)") for balise in balises_karma]

    print balises_karma
    print links_users


users_and_karma(1)
