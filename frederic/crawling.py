import requests
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getAllMetricsForArtist(artist):
    soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist)
    balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    print 'Here are the links', links
    #links.pop(0)
    #links.k ', linkop(0)
    #TODO
    # REmove links that are not watch video
    link = links[0]
    print 'a'
    all_metrics = []
    for link in links:
        soupPage = getSoupFromUrl('https://www.youtube.com' +link)
        print 'b'
        print 'link ', link
        likes_count = soupPage.find_all(id='watch-like')[0].text
        print 'c'
        dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
        print 'd'
        views_count = soupPage.find_all(class_='watch-view-count')[0].text
        print 'e'
        dislikes_count = int(dislikes_count.replace(u'\xa0', u' ').replace(' ' ,''))
        likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))
        views_count = int(views_count.replace(u'\xa0', u' ').replace(' ' ,''))
        metrics = {}
        metrics['views_count'] = views_count
        metrics['dislikes_count'] = dislikes_count
        metrics['likes_count'] = likes_count
        metrics['title'] = soupPage.title.text
        print 'MEtrics for ', metrics
        all_metrics.append(metrics)
    return all_metrics


rihanna = getAllMetricsForArtist('rihanna')
beyonce = getAllMetricsForArtist('beyonce')
