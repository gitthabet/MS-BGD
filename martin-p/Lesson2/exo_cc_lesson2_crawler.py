# si besoin : export PYTHONHOME=/home/martin/anaconda/lib/python2.7/site-packages
import sys
import requests
import html5lib
from bs4 import BeautifulSoup as bs

#Returns a soup object from a given url
def getSoupfromURL(url):
	result = requests.get(url)
	#Request successful
	if result.status_code == 200:
		# print url + " : " + "Request successful"
		return BeautifulSoup(result.text, "html5lib")
	#Request failed
	else:
		# print "Request failed : ", url
		return None

#Display number
def getNumber(num):
	return int(num.replace(u'\xa0', u' ').replace(' ', ''))

#Get the metrics by year
#http://alize2.finances.gouv.fr/ 
def getAllMetrics ():
	sep = '_'
	# 1 : get soup from the webpage
	url = 'https://news.ycombinator.com/'
	soup = getSoupfromURL(url)
	
	# 2 : stock the data
	metrics = {}
	a = req.get(url)
	soup = bs(a.text)

	#for p in range(1,4):
	#find all link
	for link in soup.findall('a'):
		#find link user
		if link.get('href').find('user') != -1:
			cpt = 0
			req = req.get(url + link.get('href'))
			so = bs(r.text)
			for l in so.find_all('td'):
				if cpt == 10:
					print l.text
	return metrics

def main():
	# 1 : initialize the list data required
	#listReqData= ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", 
	#	"TOTAL DES CHARGES DE FONCTIONNEMENT = B", 
	#	"TOTAL DES RESSOURCES D'INVESTISSEMENT = C", 
	#	"TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]

	# 3 : get all data and print 'Metrics'
	#for year in range(2010,2014):
	print getAllMetrics()

if __name__ == "__main__":
	main()
