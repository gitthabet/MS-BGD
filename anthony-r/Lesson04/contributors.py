import urllib2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

root_url = "https://gist.githubusercontent.com/paulmillr/4524946/raw/240e0ab2a70b9d3797e4a5716f40e0799adfa039/github-users-stats.json"
api_root_url="https://api.github.com/"

# Authentication
token = "f2b1ca54873985dc187463d9aa0fdf7e6eb5c7ed"

def get_contributors_list():
    raw_data = requests.get(root_url).json()
    user_list = list()
    for data in raw_data:
        user_list.append(data['login'])
    return user_list

users = get_contributors_list()[:5]
gh_users =list()


class GitHubUser:
    def __init__(self,login):
        self.login = login
        self.repositories = list()
        self.stars = 0

    def load(self):
        self.get_repositories()
        self.get_stargazers()

    def get_repositories(self):
        url = api_root_url + "users/" + self.login + "/repos?access_token=" + token + "&per_page=100"
        print url
        self.repositories = requests.get(url).json()

    def get_stargazers(self):
        for repo in self.repositories:
            self.stars += int(repo['stargazers_count'])

    def describe(self):
        print self.login + " has " + str(self.stars) + " stars."

for user in users:
    gh_users.append(GitHubUser(user))

for user in gh_users:
    user.load()
    user.describe()
