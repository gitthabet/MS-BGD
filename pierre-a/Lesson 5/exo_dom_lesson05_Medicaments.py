# -*- coding: utf-8 -*-

import requests
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import re
import unicodedata as uni

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')

# read xls
#meds = pd.io.excel.read_excel('MEDICAM.xls', 'MedicAM 0813', na_values=['NA'],encode='utf-8')
meds = pd.read_csv('MedicAM 0813-Tableau 1.csv', sep = ';')
meds = meds.dropna()

# get columns
noms = meds['NOM COURT']
produits = meds['PRODUIT']

# remove nom_produit from noms
def remove_prod(df):
    res = str(df['NOM COURT']).replace(str(df['PRODUIT']), '')
    return res
print meds[['NOM COURT', 'PRODUIT']].apply(lambda x: remove_prod(x), axis=1)[0:20]


# médicaments nouvellement remboursés en 2013
def NxRemboursement(df):
    col2012 = 'Montant remboursé 2012'
    col2013 = 'Montant remboursé 2013'
    remb2012 = long(re.sub(r'\D','',df[col2012]))
    remb2013 = long(re.sub(r'\D','',df[col2013]))
    print (remb2012 == 0) and (remb2013 != 0)
    if (remb2012 == 0) and (remb2013 != 0):
        NouvRemb = 'OUI'
    else:
        NouvRemb = 'NON'
    return NouvRemb

meds['NouveauRemboursement'] = meds.apply(lambda x: NxRemboursement(x), axis = 1)

# médicaments déremboursés en 2013
def DeRemboursement(df):
    col2012 = 'Montant remboursé 2012'
    col2013 = 'Montant remboursé 2013'
    remb2012 = long(re.sub(r'\D','',df[col2012]))
    remb2013 = long(re.sub(r'\D','',df[col2013]))
    if (remb2012 != 0) and (remb2013 == 0):
        DeRemb = 'OUI'
    else:
        DeRemb = 'NON'
    return DeRemb

meds['Déremboursé'] = meds.apply(lambda x: DeRemboursement(x), axis = 1)

meds.to_csv('Resultats.csv')
