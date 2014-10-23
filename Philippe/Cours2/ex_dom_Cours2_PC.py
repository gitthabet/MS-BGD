# Ce script a pour but de récupérer des données dans un tableau de chiffres
# issus des comptes de la ville de Paris donnée sur une page internet

import requests
from bs4 import BeautifulSoup
import html5lib

print "Récupération de données des comptes de la ville de Paris en 2013 :"
URLComptesParis = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=2013"
res = requests.get(URLComptesParis)
if res.status_code != 200:
	print "Echec de la requete", URL
else:
	print "\nSucces de la requete\n"
	print "Résultats : "
	print "---------\n"
	soupeComptesParis = BeautifulSoup(res.text, "html5lib")
	libelleDonneesArecuperer = ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", \
	                            "TOTAL DES CHARGES DE FONCTIONNEMENT = B", \
	                            "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", \
	                            "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
	balisesLibelleDonneesArecuperer = [soupeComptesParis.find("td", text=libelle) for libelle in libelleDonneesArecuperer]
	balisesMeres = [balise.find_parent() for balise in balisesLibelleDonneesArecuperer]
	balisesDonneesArecupererEuroParHabitant = [balise.select("td:nth-of-type(2)") for balise in balisesMeres]
	balisesDonneesArecupererMoyenneStrate = [balise.select("td:nth-of-type(3)") for balise in balisesMeres]
	for libelle in libelleDonneesArecuperer:
		indice = libelleDonneesArecuperer.index(libelle)
		print libelle
		print "   En euros par habitant : %s" % balisesDonneesArecupererEuroParHabitant[indice][0].get_text()
		print "   Moyenne de la strate  : %s" % balisesDonneesArecupererMoyenneStrate[indice][0].get_text()
