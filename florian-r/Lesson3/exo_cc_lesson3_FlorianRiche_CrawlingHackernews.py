# -*- coding: utf-8 -*-
"""
Created on Wed Oct 15 14:04:09 2014

@author: Florian

"""
import requests
import pprint
from bs4 import BeautifulSoup

url= 'https://news.ycombinator.com/'    
page= requests.get(url)
prettypage= BeautifulSoup(page.text)
   

Dict={}

users = prettypage.select('a[href*="user"]')
for user in users:

    urltmp=url+user.get('href')
    newpage = requests.get(urltmp)
    pretty = BeautifulSoup(newpage.text)
    karma = pretty.find(text='karma:').parent.parent
    cells=karma.contents
    final = cells[1].text
    Dict[user.get_text()]=final
    print Dict





print Dict