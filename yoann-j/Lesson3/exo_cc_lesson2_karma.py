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
    soupCombinator = getSoupfromURL('https://news.ycombinator.com/news?p=2')
    balises_a = soupCombinator.find_all("a")
    links = [balise.get('href') for balise in balises_a]
    
    all_metrics = []
    userDictionary = dict()
    
    for link in links[1:]:
        #print "here is the link: " + link
        #print link[0:7]
        if (link[0:8] == 'user?id=') :
            
            soupPage = getSoupfromURL('https://news.ycombinator.com/' +link)
            
            #print soupPage
            userProfile = soupPage.find_all('title')[0].text
            
            #userProfile = soupPage.find_all('title')

            #print userProfile.split()[1]
           
           
            userKarmaTag = soupPage.find(text="karma:").findParent("td").findParent()

        
            userKarma = userKarmaTag.select('td:nth-of-type(2)')[0].string
    
            #print userKarma
            
           
            userDictionary.update({userProfile : userKarma})
            
            
    return userDictionary
  


def main():
    
  userDictionary = dict()
  userDictionary = getUserList()
  for key1, value1 in sorted(userDictionary.items()):
      print str(key1) + " : " + str(value1) + "  \n"
    

if __name__ == "__main__":
    main()