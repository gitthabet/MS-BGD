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

def getnamehacker(hacker):
    soupYoutube = getSoupFromUrl('https://news.ycombinator.com/')
    namhacker = soupYoutube.find_all("a", class_="user?id=")
    nameh = [namhacker.get('href') for namehack in namehacker]
    print 'the name', nameh 


