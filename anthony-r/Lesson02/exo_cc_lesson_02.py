import urllib2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

root_url = "https://news.ycombinator.com/"

users = list()

class User:
  def __init__(self,id):
    self.data = None
    self.id = id
    self.karma = 0
    self.root_url = "https://news.ycombinator.com/user?id="
    self.url = self.root_url+self.id

  def get_karma(self):
    self.data = BeautifulSoup(requests.get(self.url).text)
    tags = self.data.findAll('tr')
    karmainfos = tags[6]
    self.karma = karmainfos.findChildren()[1].text
    print self.karma

  def describe(self):
    print "User : " + self.id
    print "Karma : " + self.karma


# Loading the page
page = BeautifulSoup(requests.get(root_url).text)

userlinks = page.findAll('a',{'href':re.compile(r".*\buser\b.*" )})

for user in userlinks:
    users.append(User(user.text))


for user in users:
  user.get_karma()
  user.describe()
