import requests
from bs4 import BeautifulSoup
import re
#from tinycss.css21 import CSS21Parser

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
#        print  (result.text)
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None




def recup_ligne(num_ligne) :
	ligne_mtt = balises_a[num_ligne].find_all("td", class_="montantpetit G")	
	val_hab=ligne_mtt[1].text.replace(u'\xa0', u' ').replace(' ' ,'')
	mtt_hab = int(val_hab)
	print '     mtt par habitant',mtt_hab
	val_strate=ligne_mtt[2].text.replace(u'\xa0', u' ').replace(' ' ,'')
	mtt_strate = int(val_strate)
	print '     mtt par strate',mtt_strate

annee = 2010
while (annee<=2013) :
	soupYoutube = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(annee))
	balises_a = soupYoutube.find_all("tr", class_="bleu")
	print 'Pour', annee
	print("     TOTAL DES PRODUITS DE FONCTIONNEMENT = A")
	recup_ligne(3)
	print("     TOTAL DES CHARGES DE FONCTIONNEMENT = B")
	recup_ligne(7)
	print("     TOTAL DES RESSOURCES D'INVESTISSEMENT = C")
	recup_ligne(15)
	print("     TOTAL DES EMPLOIS D'INVESTISSEMENT = D")
	recup_ligne(20)
	annee=annee +1

 


