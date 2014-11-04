# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 13:47:56 2014

@author: wei he
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import numpy as np

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

def getContributors():
    urlContributors = 'https://gist.github.com/paulmillr/2657075'
    tableContributors = getSoupFromUrl(urlContributors).find_all("tbody")
    listContributors = []
    for i in range(1,257):
        userInfo = tableContributors[0].select("tr:nth-of-type("+str(i)+")")
        contributorName = userInfo[0].select("a:nth-of-type(1)")[0].text
        listContributors.append(contributorName)
    return listContributors

def getContributorStars(contributor):
    listStars = []
    for page in range (1,2):
        url = "https://api.github.com/users/" + contributor + "/repos?page=" + str(page) + "&per_page=100"
        conn = requests.get(url, auth=(myAccount, myPassword))
        if conn.status_code == 200:
            userInfos = json.loads(conn.content)
            for line in userInfos:
                listStars.append(line.get('stargazers_count'))
        if len(listStars) == 0:
            return 0
        else:
            return np.mean(listStars)
    #print "Contributors stars got"

"""
Main
"""
listContributors = getContributors()
myAccount = "he-wei"
myPassword = raw_input('Enter your password : ')
listRes = []

for contributor in listContributors:
    listRes.append(contributor+" "+str(getContributorStars(contributor)))
print "Before writing in csv"
with open('results.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    print "Working in progress"
    for res in listRes:
        print res
        spamwriter.writerow(res)

print "Writing csv done"