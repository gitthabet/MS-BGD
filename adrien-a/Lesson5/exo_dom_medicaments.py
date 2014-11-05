# -*- coding: utf-8 -*-

import re
import pandas as pd

# Pour un médicament récupère le dosage 
def getDosage(row) :

	productName = str(row['PRODUIT'])
	shortName = str(row['NOM COURT'])
	dosage = shortName.replace(productName, '')
	return dosage

# Pour un médicament on récupère ses infos de remboursements 
def getFirstYear(row) :

	years = ['2008', '2009', '2010', '2011', '2012', '2013']

	for currentYear in years : 

		montantRemboursement = int(re.sub('\D', '', str(row['Base de remboursement ' + str(currentYear)])))
		if( montantRemboursement > 0 ) :
			return int(currentYear)

	return int(0)

# Pour un médicament on récupère ses infos de remboursements 
def getLastYear(row) :

	years = ['2008', '2009', '2010', '2011', '2012', '2013']
	lastYearPayback = 0

	for currentYear in years : 

		montantRemboursement = int(re.sub('\D', '', str(row['Base de remboursement ' + str(currentYear)])))
		if( montantRemboursement > 0 ) :
			lastYearPayback = currentYear

	return int(lastYearPayback)


# Récupération des données 2008-2013
rawData = pd.read_csv('medicamentsDB.csv')

rawData = rawData.dropna()

# Création du nouveau dataframe contenant les infos voulues 
cleanData = pd.DataFrame( columns=['nom', 'dosage', 'premiereAnneeRemboursement', 'derniereAnneeRemboursement'] )
cleanData['nom'] = rawData['PRODUIT']
cleanData['dosage'] = rawData.apply(lambda x : getDosage(x), axis=1)
cleanData['premiereAnneeRemboursement'] = rawData.apply(lambda x : getFirstYear(x), axis = 1)
cleanData['derniereAnneeRemboursement'] = rawData.apply(lambda x : getLastYear(x), axis=1)

# Affichage des 20 premiers medicaments nouvellements remboursés
print "\nMédicaments nouvellement remboursés\n"
print cleanData[cleanData['premiereAnneeRemboursement'] == 2013][0:20]

# Affichage des 20 premiers médicaments qui ne sont plus remboursés
print "\nMédicaments qui ne sont plus remboursés\n"
print cleanData[ cleanData['derniereAnneeRemboursement'] < 2013 ][0:20]

