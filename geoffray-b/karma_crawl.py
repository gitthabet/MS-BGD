import urllib2
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


	soupYoutube = getSoupFromUrl('https://www.ycombinator.com')
    balises_a = soupYoutube.find_all('a')
    links = [balise.get('href') for balise in balises_a]
    print 'Here are the links of user', links
    print links

    users[]
    for link in links :
		if link.find('user') != -1 :
			users.append('https://news.ycombinator.com/' + link)

    for user in users
    	usersoup=getSoupFromUrl(user)
    	valkarma = soup.find(text=Karma).content	