# -*- coding: utf-8 -*-

#With HUGE Jonathan Support

import numpy as np 
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import re
import json

def dosage(pattern,x):
	if (pattern.match(str(x)) is not None) : 
		return pattern.match(str(x)).group(2) 
		#print pattern.match(str(x)).group(3)#, pattern.match(str(x)).group(0)
	else : 
		return x


def removeWords(row) :
	wordsToRemove = str(row['PRODUIT']).split(' ')
	textToReplace = str(row['NOM COURT'])
	for word in wordsToRemove:
		textToReplace = textToReplace.replace (word, '')
	return textToReplace

def premiereAnneeRemboursement(row) :
	stringBase = 'Base de remboursement'
	premiereAnnee = 0
	for i in range(2008,2014):
		stringAnnee = stringBase + ' ' + str(i)
		montantAnnee = int(re.sub(r'\D', '', row[stringAnnee]))
		if montantAnnee >0 : 
			premiereAnnee = i
			break
	return premiereAnnee
		
def derniereAnneeRemboursement(row) :
	stringBase = 'Base de remboursement'
	derniereAnnee = 0
	for i in range(2008,2014):
		stringAnnee = stringBase + ' ' + str(i)
		montantAnnee = int(re.sub(r'\D', '', row[stringAnnee]))
		if montantAnnee >0 : 
			derniereAnnee = i
	return derniereAnnee

def main():
   
	medicamentsSource = pd.read_csv('medicamentsDB.csv', sep=';')
	medicamentsSource = medicamentsSource.dropna()
	medicaments=pd.DataFrame(columns = ['Nom', 'Description', 'Premiere Annee remboursement', 'Derniere Annee connue remboursement'])
	medicaments['Nom']=medicamentsSource['PRODUIT']
	medicaments['Description']= medicamentsSource.apply(lambda x : removeWords(x), axis=1)

	medicaments['Premiere Annee remboursement'] = medicamentsSource.apply (lambda x : premiereAnneeRemboursement(x),axis=1) 
	medicaments['Derniere Annee connue remboursement'] = medicamentsSource.apply (lambda x : derniereAnneeRemboursement(x),axis=1) 
	
	print medicaments['Premiere Annee remboursement'][0:20]
	print medicaments['Derniere Annee connue remboursement'][0:20]
	

if __name__ == "__main__":
    main()