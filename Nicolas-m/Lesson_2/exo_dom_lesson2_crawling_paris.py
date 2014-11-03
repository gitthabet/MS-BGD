import requests
from bs4 import BeautifulSoup


annee = 2010

def lignempg(num_ligne):
	eurhab= int(links[num_ligne].text.replace(u'\xa0', u' ').replace(' ',''))
	print ("Montant par habitant :"), eurhab
	num_ligne = num_ligne + 1
	moystrat= int(links[num_ligne].text.replace(u'\xa0', u' ').replace(' ',''))
	print ("Moyenne de la strate:"), moystrat

while (annee <= 2013):
	url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="
	r = requests.get(url + str(annee))
	soup = BeautifulSoup(r.content)
	links=soup.select('td.montantpetit.G')
	print "Annee", annee
	print "\n"
	print ("TOTAL DES PRODUITS DE FONCTIONNEMENT = A ")
	lignempg(1)
	print ("TOTAL DES CHARGES DE FONCTIONNEMENT = B ")
	lignempg(4)
	print ("TOTAL DES RESSOURCES D'INVESTISSEMENT = C")
	lignempg(10)
	print ("TOTAL DES EMPLOIS D'INVESTISSEMENT = D")
	lignempg(13)
	print "\n"
	print "########################################"
	annee = annee + 1