# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 23:01:37 2014

@author: Romain
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


'''
Part one - get all users from most active users list
'''

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print('Request succesful')
        return BeautifulSoup(result.text)
    else:
        print('Request failed'), url
        return None

# get github most active users page
soupGH = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')

# puts user profile links into a list (from tbody of html)
usernames = []
for link in soupGH.tbody.find_all('a'):
    if link.get('href').find('https://github.com/') == 0:
        usernames.append(link.get('href').replace('https://github.com/',''))

# checks that we have exactly 256 profiles
#len(usernames)


'''
Part two - use GitHub API to get all stargazers from repositories
owned by those users
'''

# Reads GitHub username and password from user input
username = input("Please enter username: ")
password = input("Please enter password: ")

# we look for stargazers in each repo of each user on the list using the API
result_list=[]
for user in usernames:
    page = 1
    while requests.get('https://api.github.com/users/' + user + '/repos?page=' + str(page), auth=(username, password)).json() != []:
        repos = requests.get('https://api.github.com/users/' + user + '/repos?page=' + str(page), auth=(username, password)).json()
        ind = 0
        while ind < len(repos):
            repo = repos[ind]
            result_list.append([user, repo['name'], repo['stargazers_count']])
            ind+=1
            # prints out wich user/repo is being collected
            print('usernumber: ' + str(usernames.index(user)) + ' | username: ' + user + ' | page: ' + str(page) + ' | repo: ' + repo['name'] + ' | stargazers: ' + str(repo['stargazers_count']))
        page+=1

# we produce the ranking and save it to .csv
result_df = pd.DataFrame(result_list, columns=['User','Repo','Stars'])
ranking=result_df[['User','Stars']].groupby(['User']).mean()
ranking=ranking.sort(['Stars'],ascending=False)
ranking.to_csv('ranking.csv', encoding='utf-8')

