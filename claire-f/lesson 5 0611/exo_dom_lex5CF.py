# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 12:31:54 2014

@author: claire

Liste des médicaments remboursés (open data)
 - extraire dosage + unité + forme
 - nouveaux médicaments remboursé 2013
 - médicaments déremboursés en 2013/2012

"""

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse
import unicodedata as uni


# code de Jonathan
def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')


df_med = df = pd.read_excel('MEDICAM 2008-2013-AMELI.xls',1)

print "df.shape :" ,df.shape
columns = ['NOM COURT', 'PRODUIT','Classe EphMRA',u'Montant remboursé 2012', u'Montant remboursé 2013']    

cols_todel = [u'CIP7', u'Code EphMRA', u'Code\nATC', u'Classe\nATC', u'Code\nATC 2', u'Libellé\nATC 2', u'Base de remboursement 2008', u'Base de remboursement 2009', u'Base de remboursement 2010', u'Base de remboursement 2011', u'Base de remboursement 2012', u'Base de remboursement 2013', u'Nombre de boites remboursées 2008', u'Nombre de boites remboursées 2009', u'Nombre de boites remboursées 2010', u'Nombre de boites remboursées 2011', u'Nombre de boites remboursées 2012', u'Nombre de boites remboursées 2013', u'Montant remboursé 2008', u'Montant remboursé 2009', u'Montant remboursé 2010', u'Montant remboursé 2011', u'Prescripteurs de ville Base de remboursement 2008', u'Prescripteurs de ville Base de remboursement 2009', u'Prescripteurs de ville Base de remboursement 2010', u'Prescripteurs de ville Base de remboursement 2011', u'Prescripteurs de ville Base de remboursement 2012', u'Prescripteurs de ville Base de remboursement 2013', u'Autres prescripteurs Base de remboursement 2008', u'Autres prescripteurs Base de remboursement 2009', u'Autres prescripteurs Base de remboursement 2010', u'Autres prescripteurs Base de remboursement 2011', u'Autres prescripteurs Base de remboursement 2012', u'Autres prescripteurs Base de remboursement 2013']

for column in cols_todel:  del df_med[column]

df_med[u'Montant remboursé 2012'].astype(float)
df_med[u'Montant remboursé 2013'].astype(float)

print "df_med.shape : ", df_med.shape
df_med.dropna()
print "df_med.shape : ", df_med.shape


# on va créer les nouvelles colonnes : new_cols=['dosage','forme','qte',]


#PRODUIT = nom du médicament

df_med['dosage_long']=df_med.apply(lambda x: str(x['NOM COURT']).replace (str(x['PRODUIT']), '').strip(),axis=1)
print df_med['dosage_long']
df_med['dosage']=df_med.apply(lambda x: str(x['dosage long']).split(' ')[0],axis=1)
print df_med['dosage']
#df_med['forme']=df_med.apply(lambda x: str(x['NOM COURT']).replace (str(x['PRODUIT']), '').strip(),axis=1)
df_med['forme']=df_med.apply(lambda x: str(x['dosage long']).replace (str(x['dosage']), '').strip(),axis=1)
print df_med['forme']



