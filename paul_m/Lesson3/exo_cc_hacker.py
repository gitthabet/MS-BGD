import requests
from bs4 import BeautifulSoup
import math

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url

def contains_karma(liste):
	#for l in liste:
	if liste.text.count("karma")>0:
		return True
	return False

hackers=[]
url="https://news.ycombinator.com/news"
result=getSoupFromUrl(url)
balises_td=result.find_all("td",class_='subtext')

for balise_td in balises_td:
	balises_a=balise_td.find_all("a")
	if len(balises_a)!=0:
		hackers.append(balises_a[0].text)

Ha={}
for hacker in hackers[:3]:
	print hacker
	result=getSoupFromUrl("https://news.ycombinator.com/user?id="+hacker)
	balises_tr=result.find_all("tr")
	for balise_tr in balises_tr:
		if contains_karma(balise_tr):
			Ha[hacker]=balise_tr.text.split(":")[1]
print Ha

