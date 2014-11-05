# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 15:40:12 2014

@author: wei he
"""

import pandas as pd
from pandas import DataFrame

datas = pd.read_excel("MEDICAM 2008-2013-AMELI.xls",sheetname=1).dropna()

nomC = "NOM COURT"
c08 = "Base de remboursement 2008"
c09 = "Base de remboursement 2009"
c10 = "Base de remboursement 2010"
c11 = "Base de remboursement 2011"
c12 = "Base de remboursement 2012"
c13 = "Base de remboursement 2013"

df = DataFrame(datas,columns=[nomC, c08, c09, c10, c11, c12, c13])
                             
df['Nouveau remboursé'] = (df[c13]>0) & (df[c12]<=0)
df['Déremboursés 2013﻿'] = (df[c13] == 0)
df['Déremboursés 2008-2013'] = (df[c13] == 0) & (df[c12] == 0) & (df[c11] == 0) & (df[c10] == 0) & (df[c09] == 0) & (df[c08] == 0)

nouveauxRembourses = df[nomC][(df['Nouveau remboursé']==True)]
derembourses2013 = df[nomC][(df['Déremboursés 2013﻿']==True)]
deremboursesDepuis2008 = df[nomC][(df['Déremboursés 2008-2013']==True)]

nouveauxRembourses.to_csv('nouveauRém.csv', encoding='utf-8')
derembourses2013.to_csv('Déremboursés 2013﻿.csv', encoding='utf-8')
deremboursesDepuis2008.to_csv('Déremboursés 2008﻿-2013.csv', encoding='utf-8')

print "Csv files saved"


#nomCourt = datas['NOM COURT']
#produit = datas['PRODUIT']
#print nomCourt

#df = DataFrame(datas,columns=['NOM COURT', 'PRODUIT'])
#print str(df['NOM COURT']).replace(str(df['PRODUIT']), '')

#print datas[['NOM COURT', 'PRODUIT']].apply(lambda x: str(df['NOM COURT']).replace(str(df['PRODUIT']), ''), axis=1)[0:20]
#print produit