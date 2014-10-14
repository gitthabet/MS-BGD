import requests
from bs4 import BeautifulSoup


result = requests.get('https://www.youtube.com/results?search_query=rihanna')


if result.status_code == 200:
    print 'Request succesful'
    soup = BeautifulSoup(result.text)
    balises_a = soup.find_all("a", class_="yt-uix-tile-link")
    links = [balise.get('href') for balise in balises_a]
    print 'Here are the links', links
    links.pop(0)
    link = links[0]
    pageHTML = requests.get('https://www.youtube.com/'+link).text
    if result.status_code == 200:
        pageSoup = BeautifulSoup(pageHTML)
        print pageSoup.title
    else:
        print 'Request for page failed', link

else:
    print 'Request failed'
