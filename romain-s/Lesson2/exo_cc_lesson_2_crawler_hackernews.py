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
         # get user name
        userids.append(link[8:])

# get corresponding karmas
karmas = {}
for userid in userids:
    # load user id page
    soupHN_user = getSoupFromUrl('https://news.ycombinator.com/user?id=' + userid)
    #<bound method Tag.get of <td valign="top">karma:</td>>
    count = 0
    for html in soupHN_user.find_all('td'):
        count = count+1    
        if count==11: 
            karma = int(html.text)
    
    # add karma of user
    karmas[userid]=karma

karmas