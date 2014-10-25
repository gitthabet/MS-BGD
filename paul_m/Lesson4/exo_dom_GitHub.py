# -*- coding: utf-8 -*-

import json
import operator
import requests
from bs4 import BeautifulSoup
import math

GitHub_API='1e954a1242e3e3b342f26e3b070fe3b68436734f'

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url

def GetMeanStars(json_user):
	sum=0
	for i in range(len(json_user)):
		sum=sum+json_user[i]['stargazers_count']
	return sum/len(json_user)

def main():
	#--------------------CRAWLING
	#On récupère la liste des users dans le dictionnaire GitHub_MoreActive_Users:
	GitHub_MoreActive_Users={}
	url="https://gist.github.com/paulmillr/2657075"
	result=getSoupFromUrl(url)
	balises_tr=result.find_all("tr")
	for balise_tr in balises_tr:
		GitHub_MoreActive_Users[balise_tr.select("td:nth-of-type(1)")[0].text.split(" ")[0].strip()]=0

	#PB: HTTPSConnectionPool(host='%20api.github.com', port=443): 
	#Max retries exceeded
	#--------------------API
	#On interroge via l'API de GitHub:
	for user in GitHub_MoreActive_Users.keys():
		req=requests.get('https:// api.github.com/users/'+user+'/repos')
		json_user=json.loads(req.text)
		GitHub_MoreActive_Users[user]=GetMeanStars(json_user)
	
	#On trie le dictionnaire
	print sorted(GitHub_MoreActive_Users.iteritems(), reverse=True, key=operator.itemgetter(1))

if __name__ == "__main__":
    main()