""" Exercice crawl GitHub """
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

# Returns list of users from top users page
def getGitUser():
	soup = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
	userInfo = soup.select("tr > td:nth-of-type(1)") 
	#Note: alternative: userInfo = soup.select('th + td a')
	users = []
	for item in userInfo:
		users.append( item.text.split(' ')[0].replace('\n','') )
	return users

topGitUsers = getGitUser()

# Returns all repos data from a given user
def getRepos(user):
    myrepos=requests.get("https://api.github.com/users/"+ user +"/repos", \
    	headers={'Authorization': 'token 5218551eb082bffa572318de0c2de10d255170b1'}).json()
    return myrepos

# Getting number of stars
data = DataFrame()
i = 0
for user in topGitUsers:
    userRepos = getRepos(user)
    i += 1
    print i #check progress
    if len(userRepos) > 0:
	    stars = []
	    listUserStars = [('',0)]
	    for repo in userRepos:
	        #print repo['stargazers_count']
	        stars.append(repo['stargazers_count'])
	    userStars = DataFrame(stars)
	    userMeanSt = userStars.mean(axis=0)
	    listUserStars.append((user,userMeanSt))
	    #print user + str(userMeanSt[0])
	    result = DataFrame({'userId': user,'Mean of stars': userMeanSt})
	    data = data.append(result)
    else:
		print user + ': No repos found for this user'

data.to_csv('gitTopUsersMean.csv')

