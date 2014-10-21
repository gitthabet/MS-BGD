# si besoin : export PYTHONHOME=/home/martin/anaconda/lib/python2.7/site-packages
import sys
import requests
import html5lib
from bs4 import BeautifulSoup

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
def getAllMetricsByYear (year, listReqData):
	sep = '_'
	# 1 : get soup from the webpage
	url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
	soup = getSoupfromURL(url + year)
	
	# 2 : stock the data
	metrics = {}

	for reqData in listReqData:
		#Get the Object associated to the required data
		reqDataObject = soup.find('td', text=reqData)
		#Get the Parent Object
		reqDataObjectParent = reqDataObject.findParent()
		#"Euros par habitant"
		eurosParHabitantInformation = reqDataObjectParent.select('td:nth-of-type(2)')[0].string
		#"Moyenne de la strate"
		moyenneDeLaStrateInformation = reqDataObjectParent.select('td:nth-of-type(3)')[0].string

		#Add data to the metrics
		metrics['EPH' + sep + year + sep + reqData[-1:]] = getNumber(eurosParHabitantInformation)
		metrics['MPS' + sep + year + sep + reqData[-1:]] = getNumber(moyenneDeLaStrateInformation)

	return metrics

def main():
	# 1 : initialize the list data required
	listReqData= ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", 
		"TOTAL DES CHARGES DE FONCTIONNEMENT = B", 
		"TOTAL DES RESSOURCES D'INVESTISSEMENT = C", 
		"TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]

	# 3 : get all data and print 'Metrics'
	for year in range(2010,2014):
		print getAllMetricsByYear(str(year), listReqData)

if __name__ == "__main__":
	main()
