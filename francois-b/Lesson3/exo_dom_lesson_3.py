# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 09:41:15 2014

@author: Paco
"""

import requests as req
from bs4 import BeautifulSoup as bs

'''
Récupérer via crawling la liste des 256 top contributors sur cette page 
https://gist.github.com/paulmillr/2657075 puis en utilisant l'API github 
https://developer.github.com/v3/ récupérer pour chacun de ces users le nombre moyens de stars des repositories 
qui leur appartiennent. Pour finir classer ces 256 contributors par leur note moyenne.﻿
'''

'''
-------------------------------------------------
If program failed, it's because of API's 
rate limit: 
"For unauthenticated requests, the rate limit 
allows you to make up to 60 requests per hour."
https://developer.github.com/v3/#rate-limiting
-------------------------------------------------
'''

# Def varaibles
p = 0
nb_contrib = 1
max_contrib = 256
offset = 2

# Page to crawl
r = req.get('https://gist.github.com/paulmillr/2657075')
soup = bs(r.text)

for link in soup.find_all('a', attrs={'rel' : 'noreferrer'}):
    if link.get('href').startswith("https://github.com/") and link.get('href').count('/')==3:
        if(p>offset and p<max_contrib+offset): 
            user = link.get('href').split('/')[3]
            print user        
            sum = 0.0
            rr = req.get("https://api.github.com/users/"+user+"/repos")
            rep = rr.json()
            for count in range(0,len(rep)):
                sum = sum + rep[count]['stargazers_count']
            print "Stars average: "+str(sum/len(rep))    
            nb_contrib = nb_contrib + 1
        p = p + 1
print nb_contrib # verify that nb_contrib = 256
