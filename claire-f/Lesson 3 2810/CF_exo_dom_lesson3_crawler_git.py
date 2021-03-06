# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 09:03:13 2014

@author: claire
exo crawling github pour le 28/10/14
"""
import requests
import json
from bs4 import BeautifulSoup
import numpy as np

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url
  
  
def calc_moy_stars(json_user):
    sum=0
    for i in range(len(json_user)):
        sum=sum+json_user[i]['stargazers_count']
#    print "*** sum == ", sum
    if len(json_user) == 0:
        return 0
    else:
        return sum/len(json_user)
  
  
#Github_top_contrib = np.arange(768).reshape((256,3))
Github_top_contrib = np.arange(512).reshape((256,2))

Github_top_contrib_str=Github_top_contrib.astype(np.string_)

url="https://gist.github.com/paulmillr/2657075"
result=getSoupFromUrl(url)
balises_tr=result.find_all("tr")
    
i=0

#print balises_tr
for balise_tr in balises_tr:
# 
    if i<256:    
        texte = balise_tr.select("td:nth-of-type(1)")[0].text
#        print i
        user_nom = texte.split(">")[0].strip()
        user = user_nom.split(" (")[0]
        print i, " user :", user
#        nom = user_nom.split("(")[1].strip(")")
#¹        print "nom :", nom
        Github_top_contrib_str[i,0]=user
#        Github_top_contrib_str[i,1]=nom
        i=i+1

#print Github_top_contrib_str

#Connect to github
from pygithub3 import Github
username = raw_input("Please enter your Github username: ")
password = raw_input("Please enter your account password: ")
#○gh = Github(login=username, password = password)


j=0
# on recherche les stars et on fait la moyenne
while j<256:
    user = Github_top_contrib_str[j,0]
    url = "https://api.github.com/users/"+user+"/repos"
    print j
    results2=requests.get(url,auth=(username, password))
    if results2.status_code != 200:
        print '*****Request failed with ',url
        Github_top_contrib_str[j,1]=0
    else:
        json_user=json.loads(results2.text)
        Github_top_contrib_str[j,1]=calc_moy_stars(json_user)
    j=j+1

print Github_top_contrib_str

np.savetxt("liste.csv",Github_top_contrib_str,fmt=" %.4e %+.4j %.4e %+.4j",delimiter=";")
  
