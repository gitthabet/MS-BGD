# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 09:49:58 2014

@author: christian
"""

import requests

#import logging

from bs4 import BeautifulSoup

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

def get_page_chanteuse(str):
    r = requests.get('http://www.youtube.com/results?search_query='+str)
    if (r.status_code != 200):
        print ("Erreur "+str+" "+r.status_code)
        exit(1)
    return r

def getSoupFromUrl(url):
    r = requests.get(url)
    if (r.status_code != 200):
        print ("Erreur "+str+" "+r.status_code)
        exit(1)
    else:
        return(BeautifulSoup(r.text))
        
    
#----------------------------------------------------

def main():

    rihanna = get_page_chanteuse('rihanna')
    
    # logger.debug(rihanna.text)

    soup = BeautifulSoup(rihanna.text)

    print "-----------------------------------------------------------------"
    
    # On va rechercher dans la page par la classe CSS
    
    balises_a = soup.find_all("a", class_="yt-uix-tile-link")

    # On crée un tableau 
    links = [balise.get('href') for balise in balises_a] 
    
    print 'Here ae the links ', links

    # On enlève le lien /user/RihannaVEVO

    links.pop(0)
    links.pop(1)
    
    
    for link in links:
        soupPage = getSoupFromUrl('http://www.youtube.com/'+link)
        print 'Titre : ',soupPage.title
        
        datas =      soupPage.find_all(id='watch-like')
        print datas
        continue
        
        likes_count = soupPage.find_all(id='watch-like')[0].text
        dislikes = soupPage.find_all(id='watch-dislike')[0].text
        viewcounts = soupPage.find_all(class_='watch-view-counts')[0].text
        nblikes = (int)(likes_count)
        nbdislikes = (int)(dislikes)
        nbviewcounts = (int)(viewcounts)
        print "Likes ", nblikes, " DisLikes ", nbdislikes," Viewcounts ", nbviewcounts

#----------------------------------------------------

if __name__ == '__main__':
  main()