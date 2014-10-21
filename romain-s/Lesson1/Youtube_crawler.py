# -*- coding: utf-8 -*-
"""
Youtube web crawler

Created on Tue Oct 14 09:53:16 2014

@author: Romain
"""

# to install requests: conda install requests in Anaconda command prompt
# also possible: pip install requests
import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text)
    else:
        return None

results = requests.get('https://www.youtube.com/results?search_query=rihanna')
results.status_code #returns status code
results.text #markup html

soup = BeautifulSoup(results.text)
print(soup.prettify)

# test du selecteur
balise_a = soup.find_all("a", class_="yt-uix-tile-link")
for balise in balise_a:
    print(balise.text)#link.get('href'))
# il y a un lien user: RihannaVEVO et on ne veut que les liens watch!
# c'est du data cleaning, on verra ca plus tard
    
links = [balise.get('href') for balise in balise_a]
links.pop(0) # remove RihannaVEVO

pagesoup = getSoupFromUrl('https://www.youtube.com/' + links[0])
views_count = pagesoup.find_all(class_='watch-view-count')[0].text
likes_count = pagesoup.find_all(id='watch-like')[0].text
dislikes_count = pagesoup.find_all(id='watch-dislike')[0].text
views_count = int(views_count.replace(u'\xa0',u''))
likes_count = int(likes_count.replace(u'\xa0',u''))
dislikes_count = int(dislikes_count.replace(u'\xa0',u''))

metrics = {}
metrics['title'] = 
metrics['views_count'] = views_count
metrics['likes_count'] = likes_count
metrics['dislikes_count'] = dislikes_count

likes_count/(likes_count+dislikes_count)

<div class="watch-view-count">483&nbsp;015&nbsp;229</div> # comments
<span class="yt-uix-button-icon yt-uix-button-icon-watch-like yt-sprite"></span> # likes
<span class="yt-uix-button-icon yt-uix-button-icon-watch-dislike yt-sprite" aria-label="Je n'aime pas ce contenu" title="Je n'aime pas ce contenu"></span> # dislikes