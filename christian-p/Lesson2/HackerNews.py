# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 20:28:26 2014

@author: christian

De http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013
récupérer les données A,B,C et D sur les colonnes Euros par habitant et par strate.
"""
import requests
from bs4 import BeautifulSoup
import re

# Returns a soup object from a given url
def getSoupFromUrl(url):
    
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        result.encoding = 'utf-8'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getKarmaFromHackerNews(user):
    
    return 0
    
    
def main():

    soupHack = getSoupFromUrl('https://news.ycombinator.com/') ;
    
    user = soupHack.find_all(name="a")
    
    for line in user:
        print line.text
        if re.match("user?id", line.text):
            #print "Ca matche"
            #print line.text
            username = line.text ........
            
            name = getSoupFromUrl("https://news.ycombinator.com/user?id="+username)
            karma = name.find(text="karma")
            print "user :" , username , " Karma : " , karma , karma[1].text
            
            
    

if __name__ == '__main__':
    main()