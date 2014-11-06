"""Exercice medicaments"""
# -*- coding: utf8 -*-

import pandas as pd
from pandas import DataFrame, Series
import re

filename = 'MEDICAM 2008-2013-AMELI.xls'
df = pd.io.excel.read_excel(filename, 1)

(m0,n0) = df.shape
#find and remove NaN rows at end
nullRows = pd.isnull(df).any(1).nonzero()[0]
df = df.drop(nullRows)
(m,n) = df.shape

#Note:
#df.ix[line] #returns line
#index = df.index #returns index

colNames = df.columns  #noms des colonnes

#colNames[9:15] remboursements 08-13
#derembourses en 2013
df['Deremb'] = (df[colNames[9:14]].sum(axis=1)>0) * (df[colNames[15]]==0)
#rembourses en 2013
df['Remb'] = (df[colNames[9:14]].sum(axis=1)==0) * (df[colNames[15]]>0)

## Trouver dosage, forme
## peut se faire en lambda function (pas le temps ...)
nomCourt = df['NOM COURT']
produit = df['PRODUIT']
df['Dosage'] = ''
df['Forme'] = ''
mDos = []
mFor = []
#for i in range(m-10,m):
for i in range(0,m):
	# for word in df.ix[i]['NOM COURT']:
	# 	print word
	print '%i of %i lines' %(i,m)
	nom = df.ix[i]['NOM COURT']
	prod = df.ix[i]['PRODUIT']
	#print nom
	#print listWordsProd
	if nom.split(' ')[0] != prod.split(' ')[0]:
		print 'Warning: names do not match in line ' + str(i)
	else:
		info = nom.replace(prod,'').strip()
		dosage = re.findall(r'\d{1,}\s\w*',info)  #regex marche mal, optimiser...
		if dosage:
			forme = info.replace(dosage[0],'')
		else:
			dosage = ['']
			forme = ['']
	mDos.append(dosage[0])
	mFor.append(forme)

df['Dosage'] = mDos
df['Forme'] = mFor
