# -*- coding: utf-8 -*-
''' Liste des médicaments remboursés, en extraire dosage, unité, forme ; ceux remboursés depuis 2013 et ceux déremboursés depuis 2007
'''

import requests
import html5lib
from bs4 import BeautifulSoup
import re
import numpy
from pandas import DataFrame
import os, sys

def main():
	if len(sys.argv) == 1:
		recupBD()
		histoRemboursement()
		postRemboursement()
	elif len(sys.argv) == 2:
		if sys.argv[1] == "recupBD":
			recupBD()
		elif sys.argv[1] == "rembourse":
			historiqueRemboursement()
		elif sys.argv[1] == "post":
			postRemboursement()
		else:
			print "Erreur : un argument est attendu parmi :"
			print "   recupBD   : pour aspirer la BD de médicaments"
			print "   rembourse : pour récupérer l'historique de remboursement des médicaments"
			print "   post      : pour post-traiter cet historique"
			print "Pour enchaîner ces activités, ne pas donner d'argument"
	else:
		print "Erreur : un argument est attendu parmi :"
		print "   recupBD   : pour aspirer la BD de médicaments"
		print "   rembourse : pour récupérer l'historique de remboursement des médicaments"
		print "   post      : pour post-traiter cet historique"
		print "Pour enchaîner ces activités, ne pas donner d'argument"

def recupBD():
	# Cette fonction aspire et traite le contenu de la BD de médicaments vendus en France
	#
	# Définition de la requête de base
	URL = "http://base-donnees-publique.medicaments.gouv.fr/"
	paramRequetePost = {"page" : 1, "affliste" : 0, "affnumero" : 0, "isAlphabet" : 1, "inClauseSubst" : "", "nomSubstances" : "", \
	                    "typeRecherche" : 0, "choixRecherche" : "medicament", "txtCaracteres" : "", "radLibelle" : 2, \
	                    "txtCaracteresSub" : "", "radLibelleSub" : 4}
	# Définition de la table pandas de stockage des données
	numMedicament = 0
	colonnes = ["Nom","Dosage","Unite","Forme","CIP"]
	tableMedicaments = []
	# Boucle sur la lette initiale du nom du médicament
	for numCaractere in range(ord('A'),ord('Z')+1):
		paramRequetePost["txtCaracteres"] = chr(numCaractere)
		requete = requests.post(URL, data=paramRequetePost)
		if requete.status_code != 200:
			print "BD des médicaments : adresse incorrecte pour la lettre %s" % chr(numCaractere)
			continue
		soupeListeMedicaments = BeautifulSoup(requete.text)
		listeMedicaments = [(element.text,element.get("href")) for element in soupeListeMedicaments.find_all(class_='standart')]
		# Boucle sur la liste de médicaments pour cette lettre initiale
		for medicament in listeMedicaments:
			# Récupération du code CIP utilisé ensuite pour récupérer l'historique de emboursement
			reqMedicament = requests.get(URL+medicament[1])
			if reqMedicament.status_code != 200:
				print "%s : adresse incorrecte" % medicament[0]
				continue
			numMedicament += 1
			soupeMedicament = BeautifulSoup(reqMedicament.text)     # ATTENTION : pour une raison comprise ce qui suit
			stringCodeCIP = soupeMedicament.find_all(text=re.compile(r"Code CIP.*")) # ne marche pas avec html5lib !
			if len(stringCodeCIP) == 0:
				codeCIP = numpy.nan
			else:
				if stringCodeCIP[0].find("ou"):
					# Dans ce cas on a à la fois le code à 7 chiffres et le coe à 13 ; on prend le second
					# et on le nettoie des tirets ou espaces
					codeCIP = int(stringCodeCIP[0].split("ou")[1].replace('-','').replace(' ',''))
				else:
					# On n'en a qu'un
					regex = re.compile(r"(\d| |-){7,}")
					codeCIP = int(regex.search(stringCodeCIP[0]).group().replace('-','').replace(' ',''))
			# Récupération du nom du médicament (chaîne de majuscules avec éventuel espace en tête de libellé)
			regexNom = re.compile(r"( |[A-Z])+")
			nomMedicament = regexNom.match(medicament[0]).group()
			# Récupération de la forme galénique (par défaut on prend le dernier morcé précédé d'une virgule)
			formeMedicament = medicament[0].split(",")[-1]
			# Récupération du dosage et de l'unité
			regexDosage = re.compile(r"(\d+(,\d+)?) (UI|U\.I\.|mg|g|µg|microgrammes|mmol|ml|%|POUR CENT)(/(\d+(,\d+)?)?\s?(l|ml|UI|dose))?")
			stringDosageMedicament = regexDosage.search(medicament[0])
			if stringDosageMedicament:
				stringDosageMedicament = stringDosageMedicament.group()
				dosageMedicament = float(stringDosageMedicament.split(" ")[0].replace(',','.'))
				uniteDosage = "".join(stringDosageMedicament.split(" ")[1:])
			else:
				dosageMedicament = numpy.nan
				uniteDosage = "ND"
			# Ajout dans la table
			tableMedicaments.append([nomMedicament,dosageMedicament,uniteDosage,formeMedicament,codeCIP])
	# Ecriture du tableur
	tableurMedicaments = DataFrame(tableMedicaments,columns=colonnes)
	tableurMedicaments.to_excel("BD_Medicaments.xls",na_rep=['NaN'])

def historiqueRemboursement():
	print "Non implémenté"

def postRemboursement():
	print "Non implémenté"

if __name__ == '__main__':
	main()