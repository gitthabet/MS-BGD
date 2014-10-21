# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

    
user = []
soupHacker = getSoupFromUrl('https://news.ycombinator.com/')
balises_a = soupHacker.find_all("td", class_ = 'subtext')

for l in range(0,len(balises_a)):
   user = balises_a[l].find_all("a")[0].text
   # user_id = ligne.get("href")
   print user
   

    

    
        

