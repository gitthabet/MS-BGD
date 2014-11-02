# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 11:23:38 2014

@author: taigeo
"""

import requests
from bs4 import BeautifulSoup
import json


def getContribList(url):
    req= requests.get(url)
    page= BeautifulSoup(req.text)

    table = page.find('tbody').select('a[href*="https://github.com/"]')
#    print table
    users=[]
    for name in table:
#        print name.text
        users.append(name.text)
    return users
    
    
def getAvgStars(contrib):

    url2='https://api.github.com/users/'+contrib+'/repos'
    req2=requests.get(url2)
    soup=BeautifulSoup(req2.text,'html.parser')

    repos=json.loads(soup.text)
    print repos
#    NbRepos= len(repos)
#    Sum=0.
#    
#    if NbRepos==0:
#        return 0
#    for repo in repos:
#        Sum+=repo['stargazers_count']
#    return float(Sum/NbRepos)

startest=getAvgStars('taylorotwell')
print startest
#url= 'https://gist.github.com/paulmillr/2657075/'
#topContrib=getContribList(url)
