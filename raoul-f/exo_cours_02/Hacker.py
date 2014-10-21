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

def getusers:
    soupHacker = getSoupFromUrl('https://news.ycombinator.com/news')
    balises_user = soupHacker.findall("", href="user?id=")
    links_user = [balise.get('href') for balise_u in balises_user]
    print "Here are the names & Karma" , links_user, getinfo(links_user)

def getinfo(user):
    soupHacker = getSoupFromUrl('https://news.ycombinator.com/user?id='+user)
    balises_karma = soupHacker.find_all("a", class_="karma:")
    links_karma = [balise.get('href') for balise_k in balises_karma]
    print 'Here are the karma', links_karma
    for link in links_user:
        getusers
        getinfo
    return all_metrics


# TO FINISH