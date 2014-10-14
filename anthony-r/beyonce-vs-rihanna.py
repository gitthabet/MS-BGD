import urllib2
import requests
from bs4 import BeautifulSoup
import re

yt_root_url = "https://www.youtube.com/"
beyonce_root_url = yt_root_url+"results?search_query=beyonce"
rihanna_root_url = yt_root_url+"results?search_query=rihanna"

# Defining class
class SongInfo:
  def __init__(self,data):
    self.data = data
    self.title = ""
    self.view_count = 0
    self.likes = 0
    self.comment_count = 0

  def parse(self):
    self.view_count = self.data.findAll(attrs={'class': re.compile(r".*\bwatch-view-count\b.*")})[0].get_text()

    self.likes = self.data.find_all(id='watch-like')[0].text

    self.title = self.data.title

  def describe(self):
    print self.title.string + " | View count :" + self.view_count + " | Likes : " + self.likes



# Retrieving data for beyonce

bey_data = requests.get(beyonce_root_url)
bey = bey_data.text
bey = BeautifulSoup(bey)

bey_child_urls = list()

for node in bey.findAll(attrs={'class': re.compile(r".*\byt-lockup-title\b.*")}):
  bey_child_urls.append(node.find('a').get('href'))

## Cleaning invalid links

for idx, url in enumerate(bey_child_urls):
  if url:
    if url[:6] != "/watch":
      bey_child_urls.pop(idx)
  else:
    bey_child_urls.pop(idx)

## Crawling to sublinks

bey_child_data = list()

for url in bey_child_urls:
  bey_child_data.append(SongInfo( BeautifulSoup(requests.get(yt_root_url+url).text) ))

for songinfo in bey_child_data:
  songinfo.parse()


# Retrieving Data for Rihanna
rih_data = requests.get(rihanna_root_url)
rih = rih_data.text
rih = BeautifulSoup(rih)

rih_child_urls = list()

for node in rih.findAll(attrs={'class': re.compile(r".*\byt-lockup-title\b.*")}):
  rih_child_urls.append(node.find('a').get('href'))

## Cleaning invalid links

for idx, url in enumerate(rih_child_urls):
  if url:
    if url[:6] != "/watch":
      rih_child_urls.pop(idx)
  else:
    rih_child_urls.pop(idx)



## Crawling to sublinks

rih_child_data = list()

for url in rih_child_urls:
  rih_child_data.append(SongInfo( BeautifulSoup(requests.get(yt_root_url+url).text) ))

for songinfo in rih_child_data:
  songinfo.parse()


for songinfo in rih_child_data:
  songinfo.describe()

for songinfo in bey_child_data:
  songinfo.describe()
  
