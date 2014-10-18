# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 09:48:59 2014

@author: Paco
"""

import requests as req
from bs4 import BeautifulSoup as bs

'''
r = req.get('https://www.youtube.com/results?search_query=rihanna')

# print "status: "+r.status_code
print "encoding: "+r.encoding 
# print r.json()
soup = bs(r.text)

for link in soup.find_all('a', attrs={'class' : 'yt-uix-tile-link'}):       
    ref = link.get('href') 
    content = link.contents
    print "-----------------------------------------"    
    print content 
    print "https://www.youtube.com/"+ref[1:len(ref)]
    print "-----------------------------------------"  
    
    
print "-----------------------------------------"    
print soup.title.string
'''

rr = req.get('https://www.youtube.com/results?search_query=beyonce')
soupp = bs(rr.text)

count_like = 0
count_dislike = 0
count_view = 0

for link in soupp.find_all('a', attrs={'class' : 'yt-uix-tile-link'}):
    if link.get('href').find("watch") != -1:   
        r = req.get("https://www.youtube.com/"+link.get('href'))
        
        soup = bs(r.text)         
        print soup.title.string
        print soup.find_all(class_='watch-view-count')[0].text
        print soup.find_all(id='watch-like')[0].text
        print soup.find_all(id='watch-dislike')[0].text


'''
----------------------------------------------
Today news from popurls.com
----------------------------------------------
'''
'''
r = req.get('http://www.popurls.com')
soup = bs(r.text)

listres = []

for link in soup.find_all('a'):
    ref = link.get('href')
    content = link.contents
    # if ref.find("go") != -1 and content[0].find("<img") == -1 and content[0].find("Apple") != -1:
    if ref.find("go") != -1 and content[0].find("<img") == -1:
        listres.append( (ref,content[0]) )        
        print "-----------------------------------------"
        print "link: http://popurls.com"+ref     
        print "title: "+content[0]
        print "-----------------------------------------"
'''        