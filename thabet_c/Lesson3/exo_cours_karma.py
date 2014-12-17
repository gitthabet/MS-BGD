# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 22:55:25 2014

@author: thabetchelligue
"""

import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
    results=requests.get(url)
    soup=BeautifulSoup(results.text)
    if results.status_code==200:

        return soup
    else:
        print 'Request failed'
    return None
    

def getUserFromYcombinator():
    url='https://news.ycombinator.com/'
    soupY=getSoupFromUrl(url)
    balises_td=soupY.find_all('td',class_="subtext")
    users=[]
    for balise in balises_td:
        info_user=balise.text.split()
        #print info_user
        if info_user[2]=="by":
            user=info_user[3]
            users.append(user)
    print "users are :"+str(users)        
    users.sort()
    return users

def getKarmaFromUser():
    url='https://news.ycombinator.com/'
    users=getUserFromYcombinator()
    for user in users:
        SoupKarma=getSoupFromUrl(url+'user?id='+user)
        karmalevel=SoupKarma.text.find("karma")
        karma=SoupKarma.text[karmalevel+6:].split()[0]
        print user +"___"
