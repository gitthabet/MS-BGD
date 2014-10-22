import requests
from bs4 import BeautifulSoup
import math

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url

def contains_TOTAL(liste):
	#for l in liste:
	if liste.text.count("TOTAL")>0:
		return True
	return False

def convertoint(text):
	groupechiffre=text.split()
	tot=0
	for i,c in enumerate(groupechiffre):
		tot+=int(c)*math.pow(1000, abs(i-len(groupechiffre)+1))
	return int(tot)

#------------------------------------------MAIN 
Dates=[2013,2012,2011]
Tab_Carac=['A','B','C','D']
url="http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
totaux_financiers_eph={}
totaux_financiers_ms={}

result=getSoupFromUrl(url+str(2013))
balises_tr=result.find_all("tbody nth-of-type(6)")
print "test",balises_tr

#for date in Dates:
for date in Dates:
	result=getSoupFromUrl(url+str(date))
	balises_tr=result.find_all("tr")
	j=0
	for balise_tr in balises_tr:

		if contains_TOTAL(balise_tr):

			#On est bien à une ligne avec Total
			balises_td=balise_tr.find_all("td")

			#Regarde les initialisations
			if Tab_Carac[j] not in totaux_financiers_eph.keys():
				totaux_financiers_eph[Tab_Carac[j]]={}
				totaux_financiers_ms[Tab_Carac[j]]={}

			#on enregistre les totaux
			totaux_financiers_eph[Tab_Carac[j]][date]=convertoint(balises_td[1].text)
			totaux_financiers_ms[Tab_Carac[j]][date]=convertoint(balises_td[2].text)
				
			#On incremente les lettres
			j=j+1

print "Euros Par Habitant"
print totaux_financiers_eph
print "Moyenne de la strate"
print totaux_financiers_ms

