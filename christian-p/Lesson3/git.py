# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 10:52:28 2014

@author: christian
"""

import requests
import json
from bs4 import BeautifulSoup
import operator

logins = {} # couple login / nom complet
stars = {} # couple login / score

# Returns a soup object from a given url
def getSoupFromUrl(url):
    
    result = requests.get(url)
    if result.status_code == 200:
        result.encoding = 'utf-8'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getPeopleFromGit():
    
    soupGit = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')

    table = soupGit.find_all("table")    
    
    for i in range (1,256):
        longname = table[0].select("tr:nth-of-type("+str(i)+")")[0].select("td:nth-of-type(1)")[0].text
        user = longname.split("(")
        if len(user) > 1:
            login = user[0][1:-1]
            name = user[1][:-1]
        else:
            login = longname
            name = longname

        logins[login] = name
        stars[login] = name
        
    return logins

def getDataFromGit(login):
    
    r = requests.get('https://api.github.com/users/'+login+'/repos',auth=('christianBGD', 'T&l&c0m'))
    
    if(r.ok):
        repoItems = json.loads(r.text or r.content)

        total=0
        for i in range(len(repoItems)):
            total+=repoItems[i]['stargazers_count']
        
        if len(repoItems)>0:
            stars[login] = total/len(repoItems)
        else:
            stars[login] = 0
        
    else:
        print "Erreur récup data repos : ", r.content


def main():
    
    # On va chercher les contributeurs
    logins = getPeopleFromGit()
    
    # On va chercher son score pour chacun des contributeurs
    for login in logins.iterkeys():
        getDataFromGit(login)
        
    # On trie la liste en fonction des scores
    s_stars = sorted(stars.iteritems(), reverse=True, key=operator.itemgetter(1))
        
    # On affiche la liste avec le nom complet
    for line in s_stars:
        print logins[line[0]], "a une moyenne de ", line[1]
 

if __name__ == '__main__':
  main()