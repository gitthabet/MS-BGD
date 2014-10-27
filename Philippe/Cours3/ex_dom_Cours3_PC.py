'''Exercice donné pour le cours 4, consistant à récupérer les 256 meilleurs
contributeurs de github, puis à les classer en fonction de leur nombre d'étoiles '''

import requests
from bs4 import BeautifulSoup
import html5lib
import os, sys
import json

def getBeautifulSoupFromURL(URL):
	res = requests.get(URL)
	if res.status_code != 200:
		print "Echec de la requete", URL
		return None
	else:
		print "Succes de la requete"
		return BeautifulSoup(res.text, "html5lib")

def getEtoilesContributeur(Id,motDePasse,contributeurGithub):
	# Renvoie le nb moyen d'étoiles des dépots du contributeur
	url = "https://api.github.com/users/" + contributeurGithub + "/starred/owner"
	requete = requests.get(url, auth=(Id,motDePasse))
	if requete.status_code != 200:
		return 0.
	else:
		dicoResultatRequeteJson = json.loads(requete.content)
		nbDepots = 0.
		nbEtoiles = 0.
		for element in dicoResultatRequeteJson:
			nbEtoiles += element.get("stargazers_count",0.)
			nbDepots += 1
		if nbDepots == 0.:
			return 0.
		else:
			return nbEtoiles/nbDepots

def main():
	if len(sys.argv) != 3:
		print "Erreur : l'identifiant et le mot de passe github sont attendus en entrée"
	else:
		githubID = sys.argv[1]
		githubMDP = sys.argv[2]
	soupePage = getBeautifulSoupFromURL("https://gist.github.com/paulmillr/2657075")
	balisesContributeurs = soupePage.find(class_="markdown-body js-file ").find("table").find("tbody").find_all("tr")
	tableContributeurs = [];
	indice = 0
	for balise in balisesContributeurs:
		indice += 1
		Contributeur = {}
		Contributeur["rang"] = indice
		Contributeur["id"] = balise.select("td:nth-of-type(1) > a")[0].string
		Contributeur["lien"] = balise.select("td:nth-of-type(1) > a")[0].get("href")
		Contributeur["etoiles"] = getEtoilesContributeur(githubID,githubMDP,Contributeur["id"])
		tableContributeurs.append(Contributeur)
	triContributeurs = sorted(tableContributeurs, key=lambda contrib: contrib["etoiles"])
	print "Classement des contributeurs de github par étoiles (moyenne sur les dépots):"
	for Contributeur in triContributeurs:
		print "   " + str(Contributeur["id"]) + " : " + str(Contributeur["etoiles"]) + " étoiles"

if __name__ == '__main__':
    main()
