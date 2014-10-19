from __future__ import division
import requests
import sys
import html5lib
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print url + " : "+'Request succesful'
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

def getAllMetricsForArtist(artist):
    print "Recuperation de la soup de la page de :" + artist
    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    #print balises_a[5]
    #print 'Here are the links', links
    
    # REmove links that are not watch video
    all_metrics = []
    #print links[5]
    for link in links[1:]:
        #print "here is the link: " + link
        if (link[0:6] == '/watch') :
            #print"Recuperation de la soup de la page de :" + "https://www.youtube.com/"+link
            
            soupPage = getSoupFromUrl('https://www.youtube.com' +link)
            
            likes_count = soupPage.find_all(id='watch-like')[0].text
            if likes_count == "":
                likes_count=0
            else :
                likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))    
            
            dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
            
            if dislikes_count == "":
                dislikes_count=0
            else:
                dislikes_count = int(dislikes_count.replace(u'\xa0', u' ').replace(' ' ,''))
                
            views_count = soupPage.find_all(class_='watch-view-count')[0].text
            if views_count == "":
                views_count=0
            else:
                views_count = int(views_count.replace(u'\xa0', u' ').replace(' ' ,''))
                
            metrics = {}
            metrics['views_count'] = views_count
            metrics['dislikes_count'] = dislikes_count
            metrics['likes_count'] = likes_count
            metrics['title'] = soupPage.title.text
            #print 'MEtrics for ', metrics
            all_metrics.append(metrics)
            
            
    #print "Resultat all_metrics:" + str(all_metrics)
    return all_metrics

def calculateTotalMetrics(artist):
    metricsInputs = getAllMetricsForArtist(artist)
    totalLikes = 0
    totalDislikes = 0
    totalViews = 0
    for title in metricsInputs :
        like = title.get('likes_count')
        dislike = title.get('dislikes_count') 
        view = title.get('views_count') 
        totalLikes += like
        totalDislikes += dislike
        totalViews += view
        metricsTotal ={}
        metricsTotal['totalLikes'] = totalLikes
        metricsTotal['totalDislikes'] = totalDislikes
        metricsTotal['totalViews'] = totalViews
    return metricsTotal



def main():
    nameArtist1 = sys.argv[1]
    nameArtist2 = sys.argv[2]
    metricsArtist1 = calculateTotalMetrics(nameArtist1)
    metricsArtist2 = calculateTotalMetrics(nameArtist2)
    print "RESULTS : \n"
    print "For " + nameArtist1+  ":"
    likesvsViews = metricsArtist1.get('totalLikes') / metricsArtist1.get('totalViews')
    print "Likes vs Views : " + "{0:.2%} ".format(likesvsViews)
    disLikesvsViews = metricsArtist1.get('totalDislikes') / metricsArtist1.get('totalViews')
    print "Dislikes vs Views : " + "{0:.2%} ".format(disLikesvsViews)
    print "\n"
    print "For " + nameArtist2+  ":"
    likesvsViews = metricsArtist2.get('totalLikes') / metricsArtist2.get('totalViews')
    print "Likes vs Views : " + "{0:.2%} ".format(likesvsViews)
    disLikesvsViews = metricsArtist2.get('totalDislikes') / metricsArtist2.get('totalViews')
    print "Dislikes vs Views : " + "{0:.2%} ".format(disLikesvsViews)

if __name__ == "__main__":
    main()
