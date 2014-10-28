import requests
import json
from bs4 import BeautifulSoup
import numpy as np
from pygithub3 import Github

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
         return BeautifulSoup(result.text)
	else:
         print 'Request failed with ',url
         return None
  
def getuserinfo(json_user):
    sum=0
    for intuser in range(len(json_user)):
        sum=sum+json_user[intuser]['stargazers_count']
    if len(json_user) == 0:
        return 0
    else:
        return sum/len(json_user)
  
contrib= np.arange(512).reshape((256,2))
strcontrib= contrib.astype(np.string_)

url="https://gist.github.com/paulmillr/2657075"
result=getSoupFromUrl(url)
balises=result.find_all("tr")
    
i=0
for balise in balises:
    if i<256:    
        strtext = balise.select("td:nth-of-type(1)")[0].text
        username = strtext.split(">")[0].strip()
        user = username.split(" (")[0]
        print i, " user :", user
        strcontrib[i,0]=user
        i=i+1
#Connect to github
login = raw_input("Please enter your Github username: ")
pwd = raw_input("Please enter your account password: ")

i=0
Output = open('github.csv', 'w')
Outputfile = csv.writer(Output, delimiter=';')
# on recherche les stars et on fait la moyenne
while i<256:
    user = strcontrib[i,0]
    url = "https://api.github.com/users/"+user+"/repos"
    result=requests.get(url,auth=(user, pwd))
    if result.status_code != 200:
        print '*****Request failed with ',url
        strcontrib[i,1]=0
    else:
        json_user=json.loads(result.text)
        strcontrib[i,1]=getuserinfo(json_user)
	Outputfile.writerow(strcontrib[i,1])
    i=i+1
# Saving crawling data
#np.savetxt("github.csv",strcontrib,fmt=" %.4e %+.4j %.4e %+.4j",delimiter=";")
#np.savetxt("github.csv",delimiter=";")


