# -*- coding: utf-8 -*-

"""

Created on Wed Nov 5 2014
    
@author: Ohayon

"""
import unicodedata as uni
import re
from pandas import Series, DataFrame
import numpy as np
import pandas as pd

################################################################################################
# Some String manipulation functions

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')


################################################################################################
# get the csv

DataMed = DataFrame.from_csv('MEDICAMDB.csv')
DataMed = DataMed
print DataMed.columns
DataMed = DataMed.dropna()
print DataMed.shape
#print DataMed
# remove produit from noms court

################################################################################################
# Remove Product Name to extract info

def RemoveProduct(df):
	word_to_remove = str(df['PRODUIT']).split(' ')
	name = str(df['NOM COURT'])
	for word in word_to_remove:
		name = name.replace(word,'')
	return name

DataMed['NOM COURT'] = DataMed.apply(lambda x : RemoveProduct(x),axis = 1)
DataMed.rename(columns={'NOM COURT':'MED INFO'},inplace=True)

print DataMed['MED INFO'][0:20]

################################################################################################
# extract dosage et unite

def ExtractDosage(df,pattern1,pattern2):
	dos2 =  re.search(pattern2,df['MED INFO'])
	dos = re.search(pattern1,df['MED INFO'])
	dosage = float('NaN')
	Unite= float('NaN')
	if dos:
			#dosage = re.sub(r'\D','',dos.group(1))
			dosage = dos.group(1)
			#Unite = re.sub(r'\W','',dos.group(2))
			Unite = dos.group(2)
	if dos2:
		if dos2.group(2) == dos2.group(5):
			dosage = dos2.group(1) + '|' + dos2.group(4)
			Unite = dos2.group(2)
		else :
			dosage = dos2.group(1) + '/' + dos2.group(4)
			Unite = dos2.group(2) + '/' + dos2.group(5)
	
	return [dosage,Unite]

patternBASE = re.compile(r'(\d*,{0,1}\d+)\s*([A-Z]{1,3}((\s*)/(\s*)[A-Z]{1,3})*|%)')
patternDOUBLE = re.compile(r'(\d*,{0,1}\d+)\s*([A-Z]{1,3})(\s*\W{1}\s*)(\d*,{0,1}\d+)\s*([A-Z]{1,3})')

DataMed[['DOSAGE','UNITE']] = DataMed.apply(lambda x : pd.Series(ExtractDosage(x,patternBASE,patternDOUBLE)),axis = 1)

################################################################################################
# extract type

def ExtractType(df,pattern):
	Type = pattern.search(str(df['MED INFO']))
	result =float('NaN')
	if Type:
		result = Type.group(0)
	return result

pattern = re.compile(r'CPR|INJ|SOL|GEL|PDR|[A-Z]{4,15}')

DataMed['TYPE'] = DataMed.apply(lambda x : pd.Series(ExtractType(x,pattern)),axis = 1)
print  DataMed[['PRODUIT','DOSAGE','UNITE','TYPE','MED INFO']][DataMed['TYPE'] == 'CPR']

#Drop some ubdetermined value
#DataMed = DataMed.dropna()

################################################################################################
# Liste des Medicaments derembourses

def Deremboursement(df):
	col ='Base de remboursement ' 
	last_year = 2008
	for year in range(2008,2014):
		remb = int(re.sub(r'\D','',df[col + str(year)]))
		if remb > 0:
			last_year = year + 1
	return last_year

DataMed['Date de Deremboursement'] = DataMed.apply(lambda x : Deremboursement(x),axis = 1)
print DataMed[['PRODUIT','Date de Deremboursement']][DataMed['Date de Deremboursement']<2014].shape

################################################################################################
# Liste des Medicaments nouvellement rembourses

def Remboursement(df,discontinue):
	col ='Base de remboursement ' 
	first_year = 2008
	last_year = 2008
	for year in range(2008,2014):
		remb = int(re.sub(r'\D','',df[col + str(year)]))
		if remb > 0:
			last_year = year + 1
	if last_year == 2014 or discontinue == True:
		for year in range(2008,2014):
			remb = int(re.sub(r'\D','',df[col + str(year)]))
			if remb > 0:
				first_year = year
				break
	
	return first_year

DataMed['Date de Remboursement'] = DataMed.apply(lambda x : Remboursement(x, False),axis = 1)
print DataMed[['PRODUIT','Date de Remboursement']][DataMed['Date de Remboursement']>2008].shape








