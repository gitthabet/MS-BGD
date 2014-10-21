# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 08:40:26 2014

@author: Paco
"""

import requests as req
from bs4 import BeautifulSoup as bs

# liste user + karma

# https://news.ycombinator.com/news?p=2

# url = "https://news.ycombinator.com/"

for page in range(1,4):
    url = "https://news.ycombinator.com/news?p="+str(page)
    print "Page: "+str(page)
    rr = req.get(url)
    soupp = bs(rr.text)
    for link in soupp.find_all('a'):
        if link.get('href').find("user") != -1:
            r = req.get("https://news.ycombinator.com/"+link.get('href'))
            # print link.get('href') 
            soup = bs(r.text)
            print soup.title.string
            count = 0
            for linkk in soup.find_all('td'):
                if count == 10:
                    print "Karma: "+linkk.text
                count = count + 1        