import urllib2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re
import sqlite3 as lite

yt_root_url = "https://www.youtube.com/"
beyonce_root_url = yt_root_url+"results?search_query=beyonce"
rihanna_root_url = yt_root_url+"results?search_query=rihanna"

def num(st):
  return int( st.encode('ascii','ignore') )

# Defining classes

class Artist:
  def __init__(self,name,songinfos):
    self.name = name
    self.songinfos = songinfos
    print len(songinfos)
    self.total_likes = 0
    self.total_views = 0
    self.total_dislikes = 0
    self.popularity_index = 0

  def compute_stats(self):
    for songinfo in self.songinfos:
      self.total_likes += songinfo.likes
      self.total_views += songinfo.view_count
      self.total_dislikes += songinfo.dislikes

    self.popularity_index = self.total_views*((self.total_likes - self.total_dislikes)/float(self.total_likes + self.total_dislikes))

  def describe(self):
    print self.name
    print "Likes : ",self.total_likes
    print "Dislikes : ", self.total_dislikes
    print "Views : ", self.total_views

    print "Popularity index : ", self.popularity_index

  def export_aggregate_to_db(self):
    export = list()
    export.append(datetime.now().strftime("%d-%m-%Y"))
    export.append(self.total_likes)
    export.append(self.total_dislikes)
    export.append(self.total_views)

    return tuple(export)

  def export_details_to_db(self):
    export = list()
    for info in self.songinfos:
      info_tuple = (datetime.now().strftime("%d-%m-%Y"),info.title,info.view_count,info.likes,info.dislikes)
      export.append(info_tuple)

    return export

class SongInfo:
  def __init__(self,raw_data):
    self.data = raw_data
    self.title = ""
    self.view_count = 0
    self.likes = 0
    self.dislikes = 0


  def parse(self):
    self.data = BeautifulSoup(self.data)

    self.view_count = self.data.findAll(attrs={'class': re.compile(r".*\bwatch-view-count\b.*")})[0].text
    self.title = self.data.title.string
    self.likes = self.data.find_all(id='watch-like')[0].text
    self.dislikes = self.data.find_all(id='watch-dislike')[0].text

    # Parsing strings to integer
    self.view_count = num(self.view_count)
    self.likes = num(self.likes)
    self.dislikes = num(self.dislikes)

  def describe(self):
    print self.title.string , " | View count :", self.view_count , " | Likes : " , self.likes, "| Dislikes : ", self.dislikes


def get_url_list(url_data):
  data = BeautifulSoup(requests.get(url_data).text)
  urls = list()
  for node in data.findAll(attrs={'class': re.compile(r".*\byt-lockup-title\b.*")}):
    urls.append(node.find('a').get('href'))

  # Cleaning the data
  for idx, url in enumerate(urls):
    if url:
      if url[:6] != "/watch":
        urls.pop(idx)
    else:
      urls.pop(idx)

  return urls

def get_information_from_urls(urls):
  child_data = list()

  for url in urls:
    newdata = SongInfo( requests.get(yt_root_url+url).text) # Instantiate a SongInfo object
    child_data.append( newdata )

  for songinfo in child_data:
    songinfo.parse()

  return child_data

def save_beyonce(artist):
  con = lite.connect('beyonce_vs_rihanna.db')
  with con:
    cur = con.cursor()
    # Saving detailled data
    details = artist.export_details_to_db()
    cur.executemany(''' INSERT INTO Beyonce_details(Curr_date, Title, Views, Likes, Dislikes) VALUES(?,?,?,?,?)''', details)

    # Saving aggregated data
    aggregate = artist.export_aggregate_to_db()
    cur.execute(''' INSERT INTO Beyonce_stats(Curr_date, Total_likes, Total_dislikes, Total_Views) VALUES(?,?,?,?)''',aggregate)

    con.commit()

# Retrieving Data
bey_child_urls = get_url_list(beyonce_root_url)
rih_child_urls = get_url_list(rihanna_root_url)


beyonce_data = get_information_from_urls(bey_child_urls)
rihanna_data = get_information_from_urls(rih_child_urls)


Beyonce = Artist("Beyonce",beyonce_data)
Rihanna = Artist("Rihanna",rihanna_data)

Beyonce.compute_stats()
Rihanna.compute_stats()

print "Stats on ",datetime.now().strftime("%d-%m-%Y")
Beyonce.describe()
Rihanna.describe()

save_beyonce(Beyonce)
