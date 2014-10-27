#ycombinator
import requests
from bs4 import BeautifulSoup


def getUser(page):
	url='https://news.ycombinator.com//news?p=',page
	result=requests.get(url)
	soup=BeautifulSoup(result.text)
	balises_a = soup.find_all("a",id)

	links = [balise.get('href') for balise in balises_a]
	i=0
	users=[]
	for link in links:
		#print link[0:7]
		if link[0:7]=='user?id':
			users.append(link.replace('user?id=',""))
		i=i+1

	return users

for page in [1,2,3]:
	user=getUser(page)
	print user
