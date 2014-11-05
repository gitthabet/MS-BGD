# -*- coding: utf-8 -*-
#cd Desktop/MS-BGD/Kit-BigData/Lesson-6/

import requests
from bs4 import BeautifulSoup
#import html5lib
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import re
import pdb
from datetime import datetime
from dateutil.parser import parse

#names=['NOM COURT','PRODUIT','Montant remboursé 2008',	'Montant remboursé 2009','Montant remboursé 2010','Montant remboursé 2011','Montant remboursé 2012','Montant remboursé 2013']
data=pd.read_csv('/Users/ysewanono/Desktop/MS-BGD/Kit-BigData/Lesson-6/MEDICAM 2008-2013-AMELI.csv')
data=data.dropna()
#print data[:5]
def remove(ligne):
	return str(ligne['NOM COURT']).replace(str(ligne['PRODUIT']),'')
data['DOSAGE ET FG']=data[['NOM COURT','PRODUIT']].apply(lambda x: remove(x),axis=1)
#print data['DOSAGE ET FG'][:20]
#for year in range(2008,2014):
#	print data['Montant remboursé '+str(year)][16550]

def getfirst(x):
	liste=[]
	for year in range(2008,2014):
		mont = re.sub(r'\D+','',x['Montant remboursé '+str(year)])
		#print mont
		mont=int(mont)
		if(mont>0):
			liste.append(year)	
	if (liste==[]):
		liste.append(0)
	minimum=min(liste)
	return minimum
data['Date de 1er remboursement']=data[['Montant remboursé 2008','Montant remboursé 2009','Montant remboursé 2010','Montant remboursé 2011','Montant remboursé 2012','Montant remboursé 2013']].apply(lambda x: getfirst(x), axis=1)
print data['Date de 1er remboursement'][:10]

nbmedocsrembourses=data.groupby('Date de 1er remboursement').size()

index_medocs_rembourses2013=data['PRODUIT'].index[data['Date de 1er remboursement']>=2013]
print "liste des médicaments remboursés en 2013"
datalistemedocrembourses=data['PRODUIT'][index_medocs_rembourses2013]
print datalistemedocrembourses

def getlast(x):
	liste=[]
	for year in range(2008,2014):
		mont = re.sub(r'\D+','',x['Montant remboursé '+str(year)])
		#print mont
		mont=int(mont)
		if(mont>0):
			liste.append(year)	
	if (liste==[]):
		liste.append(0)
	maximum=max(liste)
	return maximum

data['Date de dernier remboursement']=data[['Montant remboursé 2008','Montant remboursé 2009','Montant remboursé 2010','Montant remboursé 2011','Montant remboursé 2012','Montant remboursé 2013']].apply(lambda x: getlast(x), axis=1)
print data['Date de dernier remboursement'][:10]

index_medocs_derembourses2013=data.index[data['Date de dernier remboursement']<2013]
print "liste des médicaments déremboursés depuis 2013"
datamedocsderembourses=data['PRODUIT'][index_medocs_derembourses2013] #2620 medocs
print datamedocsderembourses

datalistemedocrembourses.to_csv('listeMedicamentsRembourses2013', encoding='utf-8')
datamedocsderembourses.to_csv('listeMedicamentsDerembourses2013', encoding='utf-8')







