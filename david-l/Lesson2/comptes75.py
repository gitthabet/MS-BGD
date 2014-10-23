""" This exercise returns info from users in ycombinator.com """
# -*- coding: iso-8859-15 -*-
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None



def getUsersFromY():
	soup = getSoupFromUrl('https://news.ycombinator.com/')
	balises_td = soup.find_all("td", class_="subtext")
	users=[]
	for balise in balises_td:
		aa = balise.text.split()
		#print aa
		if aa[2]=='by':
			user = aa[3]
			users.append(user)
	#print "Users are: " + str(users)
	users.sort()
	return users

def getComptes(year):
	urlBase = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
	urlToCook = urlBase + str(year)
	soup = getSoupFromUrl(urlToCook)
	colEur_p_hab = soup.select("body > table:nth-of-type(3) tr > td:nth-of-type(2)")
	colMoy_d_str = soup.select("body > table:nth-of-type(3) tr > td:nth-of-type(3)")
	numEur_p_hab = []
	numMoy_d_str = []

	rowst = 3
	rowskip = 2  # careful: there are 2 table headers that are not tr
	for c1 in colEur_p_hab[rowst:]:
		if c1.text!='':
			numEur_p_hab.append(int(c1.text.replace(' ', '')) )
	for c2 in colMoy_d_str[rowst:]:	
		if c2.text!='':
			numMoy_d_str.append(int(c2.text.replace(' ', '')) )

	data = DataFrame({'Eur/hab': numEur_p_hab,'Moy strate':numMoy_d_str})
	rowIds=[i-(rowst+rowskip) for i in [5,9,16,21]]
	print "Résultats consolidés pour la ville de Paris (exercice "+str(year)+")"
	print data.irow(rowIds)


for year in [2010, 2011, 2012, 2013]:
	getComptes(year)

