# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 16:04:53 2014

@author: Florian
"""

import requests
from requests.auth import HTTPBasicAuth
import json
from bs4 import BeautifulSoup
from pandas import Series

def getListeContributeur():
    url= 'https://gist.github.com/paulmillr/2657075/'
    page= requests.get(url)
    prettypage= BeautifulSoup(page.text)
    report={}
    table = prettypage.find('table')
    #print table
    noms = table.select('a[href*="https://github.com/"]')
    requete = requests.get('https://api.github.com')
    for nom in noms:
                requete = requests.get('https://api.github.com/users/'+nom.text+"/repos",auth=
                HTTPBasicAuth('florianriche', 'Ang49100!'))
    #            print json.dumps(requete.json)
                
                Repositories =  json.loads(requete.text)
                linked_average=getAverageRepositories(Repositories)
                
    #            print linked_average
                report[nom.text]=linked_average
   
    return report
    
def getAverageRepositories(Repositories):
    NbRepos= len(Repositories)
    SumTotal=0
    if NbRepos==0:
        return 0
    for Repositorie in Repositories:        
        SumTotal+= Repositorie['stargazers_count']
#        print Repositorie['stargazers_count']
#        print SumTotal
    return SumTotal/NbRepos

    
data =  getListeContributeur()
data = Series(data)
data.sort(axis=1,ascending=False)
print data