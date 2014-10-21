#ycombinator
import requests
from bs4 import BeautifulSoup

url='https://news.ycombinator.com/'
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

print users
