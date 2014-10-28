import requests
from bs4 import BeautifulSoup
import json

def getTopContributors(url):

	r=requests.get(url)
	soup=BeautifulSoup(r.text,'html.parser')

	balises_tr=soup.find_all('tr')

	users=[]
	for balise_tr in balises_tr:
		link =balise_tr.find('td').find('a')
		if link is not None:
			user=link.get('href').replace('https://github.com/','')
			users.append(user)

	return users

def getAverageStars(user):
	url2='https://api.github.com/users/'+user+'/repos'
	r=requests.get(url2)
	soup=BeautifulSoup(r.text,'html.parser')
	
	try:
		newDictionary=json.loads(str(soup))
		
		somme=0.0
		if len(newDictionary)!=0:
			for i in range(len(newDictionary)):
				somme=somme+newDictionary[i]['stargazers_count']


			return somme/len(newDictionary)
		else:
			return None

	except ValueError:
		return None


url='https://gist.github.com/paulmillr/2657075'
contributors=getTopContributors(url)
RepDict={contributor:getAverageStars(contributor) for contributor in contributors}

for key in sorted(RepDict):
    print key, RepDict[key]
