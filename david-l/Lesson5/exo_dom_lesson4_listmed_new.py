"""Exercice medicaments"""
# -*- coding: utf8 -*-

import pandas as pd
from pandas import DataFrame, Series
import re
import io

filename = 'MEDICAM 2008-2013-AMELI.xls'
df = pd.io.excel.read_excel(filename, 1)

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


def getInfo(row):
	"""Create aux column INFO"""
	row['INFO'] = row['NOM COURT'].replace(row['PRODUIT'],'').strip()
	return row

def findDosage(x,regex_dosage):
	"""Gets med dosage from regex match to field INFO"""
	result = re.findall(regex_dosage,x)
	if result:
		dosage = result[0]
	else:
		dosage = ''
	return dosage

def getFormePharma(row):
	"""Gets med's pharma form from INFO\{DOSAGE}"""
	if(row['DOSAGE']):
		row['FORME'] = row['INFO'].replace(row['DOSAGE'],'').strip()
	else:
		row['FORME'] = row['INFO']
	return row

# Create aux column INFO
df=df.apply(lambda x : getInfo(x),axis=1 )

# Create DOSAGE column
regex_dosage = re.compile(
	r'(\d{1,},?\d{0,}\s?\w+\/?\d{1,},?\d{0,}\s?\w+ |\d{1,},?\d{1,}\s?\w+\/?\w+|\d{1,},?\d{0,}\%)')
df['DOSAGE'] = df['INFO'].apply(lambda x : findDosage(x,regex_dosage) )

# Create FORME column
df=df.apply(lambda x : getFormePharma(x),axis=1 )

# Delete aux column
df = df.drop(['INFO'], axis = 1)


filename = 'medicaments.csv'
df.to_csv(filename, encoding='utf-8')
