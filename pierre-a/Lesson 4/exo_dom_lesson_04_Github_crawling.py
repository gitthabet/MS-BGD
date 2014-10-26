# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pygithub3 import Github

#import ssl
#from functools import wraps
#def sslwrap(func):
#    @wraps(func)
#    def bar(*args, **kw):
#        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
#        return func(*args, **kw)
#    return bar

#ssl.wrap_socket = sslwrap(ssl.wrap_socket)


def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


def getContributors():
    contributors = []
    soupGit = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
    balises_tr = soupGit.find_all("tr")
    contributors = [ balise.td.a.next_element for balise in balises_tr]
    return contributors

def getStargazers_count(user):
    print "processing " + user + "..."
    stars = 0
    #get_user = gh.users.get(user)
    user_repos = gh.repos.list(user = user).all()
    for repo in user_repos:
        stars += repo.stargazers_count
    if len(user_repos) != 0:
        return stars/len(user_repos)
    else:
        return None


#**************MAIN********************#

Contributors = getContributors()

#Connect to github
username = raw_input("Please enter your Github username: ")
password = raw_input("Please enter your account password: ")
gh = Github(login=username, password = password)

STARS = {}

for contr in Contributors:
    STARS[contr] = getStargazers_count(contr)

print "\n"
print "**** Users sorted by mean of stars ****\n"

i=0
for user in sorted(STARS, key=STARS.get, reverse=True):
  i += 1
  print str(i) + " - " + user + " -> mean of repos stars : " + str(STARS[user])

