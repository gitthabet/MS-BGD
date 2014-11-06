

 
import requests
from bs4 import BeautifulSoup


t='https://www.youtube.com/results?search_query=Rihanna'
       
# Returns a soup otps://www.youtube.com/results?search_query='+ibject from a given url
def SoupdeUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getAlllinkForArtist(artist):
    soupYtArtist = SoupdeUrl('https://www.youtube.com/results?search_query='+artist)
    balises_a = soupYtArtist.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    for i in links:
        if i[0:6]!='/watch':
            links.remove(i)
    print links
    return links
    
def score(artist):
    
   for i in getAlllinkForArtist(artist):
       o=SoupdeUrl('https://www.youtube.com/results?search_query='+i)
       nbrvue=int(o.find('div',class_="watch-view-count").text.replace(u'\xa0', u' ').replace(' ',''))
       nbrdelike=int(o.findAll('span',class_="watch-like").text.replace(u'\xa0', u' ').replace(' ',''))
       nbrdedislike=int(o.findAll('span',class_="watch-dislike").text.replace(u'\xa0', u' ').replace(' ',''))
       return nbrvue,nbrdelike
      
score('Rihanna')
score('Beyonce')

