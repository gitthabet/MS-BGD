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
    balises_P = soupKarma.find_all("td", class_="subtext")
    
   for 

    return 

def getAllKarma(people):
    soupKarma = getSoupFromUrl("https://news.ycombinator.com/user?id="+str(people))
    balises_K = soupKarma.find_all("td", class_="valign")


pages = [1,2,3]
print "Name Karma"
People =  getAllKarmaForPeople(date)


for date in Dates: 
    print date
    print getAllValuesForABCD(date)

