import requests
from bs4 import BeautifulSoup

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getAllMetricsForArtist(artist, page):
    all_metrics = []
    for p in range(page):
        soupYoutube = getSoupFromUrl('https://www.youtube.com/results?search_query='+artist+'&page='+str(p))
        balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")
        links = [balise.get('href') for balise in balises_a]
        a = len(links)
        for link in links[0:a]:
            if link[0:6] == '/watch':
                soupPage = getSoupFromUrl('https://www.youtube.com' +link)
                likes_count = int(soupPage.find_all(id='watch-like')[0].text.replace(u'\xa0', u' ').replace(' ' ,''))
                dislikes_count = int(soupPage.find_all(id='watch-dislike')[0].text.replace(u'\xa0', u' ').replace(' ' ,''))
                views_count = int(soupPage.find_all(class_='watch-view-count')[0].text.replace(u'\xa0', u' ').replace(' ' ,''))
                metrics = {}
                metrics['views_count'] = views_count
                metrics['dislikes_count'] = dislikes_count
                metrics['likes_count'] = likes_count
                metrics['title'] = soupPage.title.text
                all_metrics.append(metrics)
    return all_metrics

def calcPopularity(all_metrics):
    vids_num = len(all_metrics)
    popularity = 0.0
    for vid in range(vids_num):
        metric = all_metrics[vid]
        print metric
        elements = []
        for key in metric:
            elements.append(metric[key])
        views = float(elements[1])
        likes = float(elements[3])
        dislikes = float(elements[2])
        popularity +=  views*((likes-dislikes)/(likes+dislikes))
    return popularity


#---------------------------------------------------------------------------#
rihanna = getAllMetricsForArtist('rihanna', 1)
beyonce = getAllMetricsForArtist('beyonce', 1)

rihanna_pop = calcPopularity(rihanna)
beyonce_pop = calcPopularity(beyonce)

print "Rihanna popularity : ", rihanna_pop
print "beyonce popularity : ", beyonce_pop

if rihanna_pop > beyonce_pop:
    print "Rihanna est plus populaire que Beyonce"
else:
    print "Beyonce est plus populaire que Rihanna"
