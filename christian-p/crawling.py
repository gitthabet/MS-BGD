# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re

# Returns a soup object from a given url
def getSoupFromUrl(url):
    
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        result.encoding = 'utf-8'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def correct_unicode(s):
    """ Corrects things like \xe9 """
    errs ={ u"\xe9":u"e",
            u"\xe8":u"e",
            u"\xea":u"e",
            u"\xf6":u"o",
            u"\xf8":u"o",
            u"\xf3":u"o",
            u"\xfc":u"u", 
            u"\xe4":u"a", 
            u"\xe1":u"a", 
            u"\xe3":u"a", 
            u"\xed":u"i" 
          }
    for err in errs: 
       if err in s:
            ss = s.split(err)
            res =  errs[err].join(ss)
            return res
    return s

def getAllMetricsForArtist(artist):
    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    print 'Here are the links', links

    #TODO    
    # REmove links that are not watch video

    link = links[0]
    all_metrics = []
    
    for link in links:      
        print link
        if (re.match('\/watch', link) != None):
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
            metrics['title'] = correct_unicode(soupPage.title.text)
            print 'MEtrics for ', metrics
            all_metrics.append(metrics)
    return all_metrics


def main():

    rihanna = getAllMetricsForArtist('rihanna')
    beyonce = getAllMetricsForArtist('beyonce')


if __name__ == '__main__':
  main()