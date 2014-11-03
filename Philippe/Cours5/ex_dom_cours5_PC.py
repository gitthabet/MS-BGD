''' Exercice pour le cours 5.
    Il faut lister les annonces de Renault Captur sur leboncoin.fr, en Aquitaine, PACA
    et IDF, récupérer les coordonnées géographiques de la ville de l'annonceur via
    Google, et bâtir un tableau avec modèle, année, kilométrage, prix, téléphone du 
    prorpiétaire, son statut (particulier ou agence), et la cote à l'argus, récupérée
    sur lacentrale.fr.
'''

import requests
import json
import html5lib
from bs4 import BeautifulSoup
import re
import unicodedata
import numpy
import pandas

def main():
	# Création du tableur pandas
	tableurRenaultCaptur = pandas.DataFrame(columns=["Région","Ville","Latitude (deg)","Longitude (deg)",\
						   "Propriétaire","Téléphone","Type","Année","Kilométrage (km)","Prix (eur)",\
						   "Argus (eur)","Comparaison à l'argus"])
	marque = "Renault"
	modele = "Captur"
	types = ["0.9 TCE90 ENERGY ARIZONA ECO2","0.9 TCE90 ENERGY INTENS ECO2","0.9 TCE90 ENERGY LIFE ECO2",\
			 "0.9 TCE90 ENERGY ZEN ECO2","1.2 TCE120 ARIZONA EDC","1.2 TCE120 INTENS EDC",\
			 "1.2 TCE120 ZEN EDC","1.5 DCI90 ARIZONA EDC ECO2","1.5 DCI90 BUSINESS EDC",\
			 "1.5 DCI90 ENERGY ARIZONA ECO2","1.5 DCI90 ENERGY BUSINESS  ECO2",\
			 "1.5 DCI90 ENERGY INTENS ECO2","1.5 DCI90 ENERGY LIFE ECO2","1.5 DCI90 ENERGY ZEN ECO2",\
			 "1.5 DCI90 INTENS EDC","1.5 DCI90 ZEN EDC"]
	# Récupération de l'argus
	argus = getCote()
	# Récupération des annonces sur leboncoin.fr
	regions = ["Aquitaine","Provence-Alpes-Côte d'Azur","Île-de-France"]
	regionsBonCoin = ["aquitaine","provence_alpes_cote_d_azur","ile_de_france"]
	for region in regions:
		regionBonCoin = regionsBonCoin[regions.index(region)]
		categories = ["p", "c"]  # Catégories particuliers et professionnels
		for categorie in categories:
			if categorie == "p":
				proprietaire = "Particulier"
			else:
				proprietaire = "Professionnel"
			URL = "http://www.leboncoin.fr/voitures/offres/" + regionBonCoin \
			    + "/?f=" + categorie + "&q=renault captur"
			soupePrincipale = getBeautifulSoupFromURL(URL)
			nbAnnonces = int(soupePrincipale.find_all("nav")[1].find("b").text)
			# On cherche le nombre de pages (il y a 35 annonces max par page)
			nbPages = nbAnnonces/35 + 1
			# Boucle sur le numéro de page
			for numPage in range(1, nbPages+1):
				URL = "http://www.leboncoin.fr/voitures/offres/" + regionBonCoin +"/?f=" + categorie \
				    + "&q=renault captur&o=" + str(numPage)
				soupePage = getBeautifulSoupFromURL(URL)
				balisesAnnonces = soupePage.find(class_="list-lbc").find_all("a")
				# Boucle sur les annonces
				for baliseAnnonce in balisesAnnonces:
					lienAnnonce = str(baliseAnnonce.get("href"))
					soupeAnnonce = getBeautifulSoupFromURL(lienAnnonce)
					# On vérifie d'abord la marque et le modèle car le moteur de recherche du
					# bon coin renvoie toute annonce contenant les mots cherchés.
					# S'ils sont incorrects, on gicle l'annonce
					marqueVoiture = soupeAnnonce.find(text="Marque :").find_next().text
					if marque not in  marqueVoiture.capitalize():
						break
					modeleVoiture = soupeAnnonce.find(text="Modèle :").find_next().text
					if modele not in  modeleVoiture.capitalize():
						break
					# On récupère ensuite les différentes caractéristiques : prix, ville du propriétaire
					# (on calcule en passant ses latitude et longitude), kilométrage, année, numéro de
					# téléphone du prorpriétaire
					prix = int(str(soupeAnnonce.find(class_="price").find(class_="price").text[:-2]).replace(' ',''))
					ville = soupeAnnonce.find(text="Ville :").find_next().text
					lat, longi = getCoordonneesGeographiques(ville)
					kilometrageString = str(soupeAnnonce.find(text="Kilométrage :").find_next().text).replace(' ','')
					nombreRegex = re.compile("[0-9]*")
					expressions = nombreRegex.findall(kilometrageString)
					if len(expressions) == 0:
						kilometrage = -1
					else:
						kilometrage = int(expressions[0])
					anneeString = str(soupeAnnonce.find(text="Année-modèle :").find_next().text).replace(' ','')
					anneeRegexp = re.compile("201[3-4]")
					expressions = anneeRegexp.findall(anneeString)
					if len(expressions) == 0:
						annee = -1
					else:
						annee = int(expressions[0])
					# Pour le numéro de téléphone, on récupère le texte de l'annonce, on y
					# supprime espaces et retours à la ligne, et on cherche une expression regulière
					description = soupeAnnonce.find(class_="AdviewContent").find(class_="content").text
					description.replace(' ','').replace('\n','')
					numTelRegexp = re.compile("0[1-9][0-9]{8}")
					expressions = numTelRegexp.findall(description)
					if len(expressions) == 0:
						numeroTelephone = "ND"
					else:
						numeroTelephone = str(expressions[0])
						numeroTelephone = numeroTelephone[0:2] + " " + numeroTelephone[2:4] + " " \
										+ numeroTelephone[4:6] + " " + numeroTelephone[6:8] + " " \
										+ numeroTelephone[8:10]
					# Enfin on tâche d'identifier le modèle, uniquement pour les voitures de 2013
					# (les autres ne figurent pas sur l'argus)
					description = unicodedata.normalize('NFKD',soupeAnnonce.find(class_="AdviewContent").find(class_="content").text).lower
					regexpType1 = re.compile("dci {0,1}90")
					regexpType2 = re.compile("tce {0,1}120")
					regexpType3 = re.compile("tce {0,1}90")
					if len(regexpType1.findall(description)) > 0:
						if description.find(' zen ') != -1:
							typeVoiture = 15
						elif description.find(' intens ') != -1:
							typeVoiture = 14
						elif description.find(' energy ') != -1:
							if description.find(' zen ') != -1:
								typeVoiture = 13
							elif description.find(' life ') != -1:
								typeVoiture = 12
							elif description.find(' intens ') != -1:
								typeVoiture = 11
							elif description.find(' business ') != -1:
								typeVoiture = 10
							elif description.find(' arizona ') != -1:
								typeVoiture = 9
							else:
								typeVoiture = -1 # Cas indéterminé
						elif description.find(' business ') != -1:
							typeVoiture = 8
						elif description.find(' arizona ') != -1:
							typeVoiture = 7
						else :
							typeVoiture = -1
					elif len(regexpType2.findall(description)) > 0:
						if description.find(' zen ') != -1:
							typeVoiture = 6
						elif description.find(' intens ') != -1:
							typeVoiture = 5
						elif description.find(' arizona ') != -1:
							typeVoiture = 4
						else:
							typeVoiture = -1
					elif len(regexpType3.findall(description)) > 0:
						if description.find(' zen ') != -1:
							typeVoiture = 3
						elif description.find(' life ') != -1:
							typeVoiture = 2
						elif description.find(' intens ') != -1:
							typeVoiture = 1
						elif description.find(' arizona ') != -1:
							typeVoiture = 0
						else:
							typeVoiture = 0
					else:
						typeVoiture = 0
					if typeVoiture == -1:
						descVoiture = "ND"
						cote = -1
						compArgus = "ND"
					else:
						descVoiture = types[typeVoiture]
						cote = argus[typeVoiture]
						if prix <= cote:
							compArgus = "<"
						else:
							compArgus = ">"
					if annee > 2013:
						cote = -1
						compArgus = "ND"
					# Insertion dans le tableur
					nouvelleEntree = [region,ville,lat,longi,proprietaire,numeroTelephone,descVoiture,annee,\
					                  kilometrage,prix,cote,compArgus]
					if cote == -1:
						nouvelleEntree[10] = numpy.nan
					if kilometrage == -1:
						nouvelleEntree[8] = numpy.nan
					if annee == -1:
						nouvelleEntree[7] = numpy.nan
					tableurRenaultCaptur.append(nouvelleEntree)
	tableurRenaultCaptur.to_csv("annoncesRenaultCaptur.csv",na_rep="ND")


def getBeautifulSoupFromURL(URL):
	res = requests.get(URL)
	if res.status_code != 200:
		print "Echec de la requete ", URL
		return None
	else:
		#print "Succes de la requete"
		return BeautifulSoup(res.text, "html5lib")    # text contient le code HTML associé à res

def getCoordonneesGeographiques(lieu):
	clef = "AIzaSyBvCoNmPsxjiQin8Yb7BekF8iuS4ufriq8"
	URL = "https://maps.googleapis.com/maps/api/directions/json?origin="+lieu \
	    +"&destination="+lieu+"&langage=fr&key="+clef
	requete = requests.get(URL)
	if requete.status_code != 200:
		return 0., 0.
	else:
		dicoResultatsRequete = json.loads(requete.content)
		lat = float(dicoResultatsRequete["routes"][0]["legs"][0]["start_location"]["lat"])
		longi = float(dicoResultatsRequete["routes"][0]["legs"][0]["start_location"]["lng"])
		return lat, longi

def getCote():
	argus = []
	URL = ["http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+arizona+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+intens+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+life+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+zen+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+arizona+edc-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+intens+edc-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+zen+edc-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+arizona+edc+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+business+edc-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+arizona+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+business+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+intens+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+life+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+s%5Es+zen+eco2-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+intens+edc-2013.html",\
		   "http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+zen+edc-2013.html"]
	for lien in URL:
		soupeArgus = getBeautifulSoupFromURL(lien)
		coteString = str(soupeArgus.find(class_="Result_Cote arial tx20").text[:-1]).replace(" ","")
		cote = int(coteString)
		argus.append(cote)
	return argus

if __name__ == '__main__':
	main()