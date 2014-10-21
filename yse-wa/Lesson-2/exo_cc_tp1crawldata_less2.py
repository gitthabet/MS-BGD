# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:02:50 2014

@author: ysewanono
"""
import requests 
from bs4 import BeautifulSoup 
import html5lib


def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

def getAllMetricsForArtist(artist):
    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
    #print soupYoutube
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    links.pop(0)
    ###MODIFIER POUR PRENDRE QUE LES VIDEOS WATCHS
    print 'Here are the links', links 
    link = links[0]
    all_metrics = []
    for link in links:
            #if link[0:7]=='u'/watch':
                soupPage = getSoupFromUrl('https://www.youtube.com' +link)
                likes_count = soupPage.find_all(id='watch-like')[0].text
                dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
                views_count = soupPage.find_all(class_='watch-view-count')[0].text
                #print "likes", likes_count, "dislike", dislikes_count, "view", views_count
                dislikes_count = int(dislikes_count.replace(u'\xa0', u' ').replace(' ' ,''))
                likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))
                views_count = int(views_count.replace(u'\xa0', u' ').replace(' ' ,''))
                #print "likes", likes_count, "dislike", dislikes_count, "view", views_count
                metrics = {}
                metrics['views_count'] = views_count
                metrics['dislikes_count'] = dislikes_count
                metrics['likes_count'] = likes_count
                metrics['title'] = soupPage.title.text
                #print 'MEtrics for ', metrics
                all_metrics.append(metrics)
            # else None    
    return all_metrics

rihanna=getAllMetricsForArtist('rihanna')
print rihanna
beyonce=getAllMetricsForArtist('beyonce')  
print beyonce  

'''SoupYoutube=getSoupfromUrl('https://www.youtube.com/results?search_query=rihanna')
balises_a=SoupYoutube.find_all("a", class_="yt-uix-tile-link")
links=[balise.get('href') for balise in balises_a ] 
print 'Here are the links'+ links'''




'''    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query=rihanna')
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    print 'Here are the links'+ links


if result.status_code==200:
    print  'Request successful'
    soup=BeautifulSoup(result.text)
    balises_a=soup.find_all("a", class_="yt-uix-tile-link")
    links=[ balise.get('href') for balise in balises_a]
    print 'Here are the links', links
    links.pop(0)
    pageHTML=requests.get('https://www.youtube.com/'+ links).text
    soupPage=getSoupFromUrl('https://www.youtube.com/'+ links)
    print soupPage.title
    
    
    
    
    button= soup.find_all(class_="yt-uix-button-content"
    
    
    dislikes_count= int("watch-like-dislike-buttons"'''