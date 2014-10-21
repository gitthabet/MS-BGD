import requests
import sys
import html5lib
import re
from bs4 import BeautifulSoup

#Retrieve the HTML soup from the given URL
def getSoupfromURL(url):
	#Retrieve HTML code for the given URL
  result = requests.get(url)
  #Check that the request was done successfully and return the soup
  if result.status_code == 200:
    print url + " : " + "Request successful"
    return BeautifulSoup(result.text, "html5lib")
  else:
    print "Request failed : ", url
    return None

def getUserList ():
    #print "Recuperation de la soup de la page de :https://news.ycombinator.com/"
    soupCombinator = getSoupfromURL('https://news.ycombinator.com/')
    balises_a = soupCombinator.find_all("a")
    links = [balise.get('href') for balise in balises_a]
    
    all_metrics = []
    userDictionary = dict()
    
    for link in links[1:]:
        #print "here is the link: " + link
        #print link[0:7]
        if (link[0:8] == 'user?id=') :
            print "OK"
            soupPage = getSoupfromURL('https://news.ycombinator.com/' +link)
            
            #print soupPage
            #userProfile = soupPage.find_all('title')[0].text
            userProfile = soupPage.find_all('title')

            print userProfile[0].text
           
            userKarma = soupPage.find_all(re.compile("karma"))
            print userKarma
           
            #userDictionary.update({userProfile : userKarma})
            
            
    return userDictionary
  


def main():
    
  getUserList()

if __name__ == "__main__":
    main()