# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 09:54:24 2014

@author: Wei He
"""

import requests
from bs4 import BeautifulSoup
#import html5lib

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

# Remove links that are not watch video
def removeNoVideoLinks(links):
    count = 0
    for link in links:
        if link.find("watch") == -1:
            links.pop(count)
        count = count+1
    return links

def getAllMetricsForArtist(artist):
    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    links=removeNoVideoLinks(links)
    print 'Here are the video links', links
    
    link = links[0]
    all_metrics = []
    for link in links:
        soupPage = getSoupFromUrl('https://www.youtube.com' +link)
        likes_count = soupPage.find_all(id='watch-like')[0].text
        dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
        views_count = soupPage.find_all(class_='watch-view-count')[0].text
        dislikes_count = int(dislikes_count.replace(u'\xa0', u' ').replace(' ' ,''))
        likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))
        views_count = int(views_count.replace(u'\xa0', u' ').replace(' ' ,''))
        metrics = {}
        metrics['views_count'] = views_count
        metrics['dislikes_count'] = dislikes_count
        metrics['likes_count'] = likes_count
        metrics['title'] = soupPage.title.text
        print 'Metrics for ', metrics
        all_metrics.append(metrics)
    return all_metrics


rihanna = getAllMetricsForArtist('rihanna')
beyonce = getAllMetricsForArtist('beyonce')
