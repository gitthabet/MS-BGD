from __future__ import division
import requests
import sys
import html5lib
from bs4 import BeautifulSoup
import json
import numpy as np
import operator
import csv


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

def getTopContributors(url):
	
    contributorsList = []

    soupGitHub = getSoupFromUrl(url)
    
    object1 = soupGitHub.find(class_="markdown-body js-file ").find('table').find('tbody')
    
    balises_tr = object1.find_all('tr')
    
    for balise in balises_tr :
    	contributor = balise.select('a:nth-of-type(1)')[0]
    	contributorsList.append(contributor.string)
   
    return contributorsList

def getContributorStars(password, url1, url2):
	
	starsList =[]
	
	req=requests.get (url1, auth=('yjanvier', password))
	
	reposDictionnaryList = json.loads(req.content)
	
	for reposDictionnary in reposDictionnaryList:
		starsList.append(reposDictionnary.get('stargazers_count'))
	
	req=requests.get (url2, auth=('yjanvier', password))
	
	reposDictionnaryList = json.loads(req.content)
	
	for reposDictionnary in reposDictionnaryList:
		starsList.append(reposDictionnary.get('stargazers_count'))
	return np.mean(starsList)
    	
def main():
  password = raw_input('password : ')
  contributorsList = getTopContributors('https://gist.github.com/paulmillr/2657075')
  contributorsRanking = dict()
  for contributorName in contributorsList:
    averageStars = getContributorStars(password, 'https://api.github.com/users/'+contributorName+'/repos?page=1&per_page=100', 'https://api.github.com/users/'+contributorName+'/repos?page=2&per_page=100')
    contributorsRanking.update({contributorName : averageStars})
  contributorsRanking = sorted(contributorsRanking.iteritems(), reverse=True, key=operator.itemgetter(1))
  with open('Githubranking.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for key, value in contributorsRanking:
      print key + " : " + str(value) + "\n"
      spamwriter.writerow(key + " : " + str(value))


if __name__ == "__main__":
    main()
