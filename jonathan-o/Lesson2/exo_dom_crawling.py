import requests
# html5lib parser de meilleur qualite
import html5lib
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

def getAllMetricsForArtist(artist):
    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    #print 'Here are the links', links
    link = links[0]
    all_metrics = []
    for link in links:
        if link[0:6] == '/watch':
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
         #print 'MEtrics for ', metrics
         all_metrics.append(metrics)
    print 'parser succesful, metric calculated for ' + artist
    return all_metrics

# def calculMetric(all_metrics):
#     sum_views=0
#     sum_likes=0
#     sum_dislikes=0
#     results = 0
#     for metric in all_metrics:
#         sum_views += metric['views_count']
#         sum_dislikes += metric['dislikes_count']
#         sum_likes += metric['likes_count']
#     results = sum_views*(sum_likes - sum_dislikes)/len(all_metrics)
#     return results      

def calculMetric2(all_metrics):
    results = 0
    for metric in all_metrics:
        results += metric['views_count']*(metric['likes_count']-metric['dislikes_count'])/(metric['likes_count']+metric['dislikes_count'])
    results = results/len(all_metrics)
    return results      

def compare(artist1,artist2):
   met1 = getAllMetricsForArtist(artist1)
   met2 = getAllMetricsForArtist(artist2)
   if calculMetric2(met1) < calculMetric(met2):
     return artist1 + ' wins and is the best'
   else: return artist2 + ' wins and is the best'

print compare('rihanna','beyonce')




