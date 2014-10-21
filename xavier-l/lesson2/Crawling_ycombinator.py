import requests
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


def getAllPeople(page):
    soupPeople = getSoupFromUrl("https://news.ycombinator.com/news?p="+str(page))
    balises_P = soupPeople.find_all("td", class_="subtext")
    People={}
    for balise in balises_P:
        Name = balise.find_all("a")
        Name = str(Name[0])
        if Name.index("id="):
            i = Name.index("id=")
            j = Name.index("\"=")
            Name = Name[i+3:j]
            Karma = getKarma(Name)
            People[Name]=Karma
    return People


def getKarma(people):
    soupKarma = getSoupFromUrl("https://news.ycombinator.com/user?id="+str(people))
    balises_K = soupKarma.find_all("td")
    for balise in balise_k:
        if 'Karma' in str(balise):
            baliseatraiter = balise
            balisetraiter = 0
    return balisetraiter


pages = [1,2,3]
print "Name Karma"
for page in pages:
    PeopleName =  getAllPeople(page)
    print PeopleName

