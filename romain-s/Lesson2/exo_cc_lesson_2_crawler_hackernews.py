import requests
from bs4 import BeautifulSoup

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print('Request succesful')
        return BeautifulSoup(result.text)
    else:
        print('Request failed'), url
        return None

# get hackernews page
soupHN = getSoupFromUrl('https://news.ycombinator.com/')
soupHN.link.get('href')
links = []

# get all links from page
for link in soupHN.find_all('a'):
    links.append(link.get('href'))

# get all user ids
userids = []
for link in links:
    if link[0:8]=='user?id=':
        userids.append(link[8:])
        # get user name

# get corresponding karmas
karma = {}
for userid in userids:
    # load user id page
    soupHN_user = getSoupFromUrl('https://news.ycombinator.com/user?id=' + userid)
    # get karma from user

#userid = 'iprashantsharma'
#soupHN_user = getSoupFromUrl('https://news.ycombinator.com/user?id=' + userid)
#soupHN_user.find_all('.valign')