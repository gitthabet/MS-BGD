# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import html5lib


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

def getAllcontributors():
    soupGitHub = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
    balises= soupGitHub.find("table")
    #print balises
    balises_a=balises.find_all("a")
    #print balises_a
    links=[balise.get('href') for balise in balises_a]
    #print links
    toplinks=[]
    print links[0][0:19]
    for link in links:
        if link[0:19]=='https://github.com/':
            toplinks.append(link[19:100].encode('ascii','ignore'))
    #print toplinks[0]
    userstars=[('',0)]
    for user in toplinks:
        repos=requests.get("https://api.github.com/users/"+user+"/repos", auth=('ysewa', 'MDP')).json()
        sumstars=0
        for repo in repos:
            #print repo['stargazers_count']
            sumstars+=int(repo['stargazers_count'])
        #print user, sumstars
        if len(repos)!=0:
            meanstars=sumstars/len(repos)
            userstars.append((user,meanstars))
        else:
            userstars.append((user,0))
    userstars.sort(key=lambda star: star[1], reverse=True)
    print userstars

getAllcontributors()

