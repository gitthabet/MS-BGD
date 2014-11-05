# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 14:38:59 2014

@author: louarradi
"""
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import re
import xlrd
import pandas as pd
from StringIO import StringIO


DonneeMedicament = pd.read_excel('file:///home/louarradi/Documents/Info721/MEDICAM%202008-2013-AMELI.xls', 'MedicAM 0813', index_col=None, na_values=['NA'])
DonneeNomCourt =DonneeMedicament[DonneeMedicament.columns[1]]
DonneeMedicament['Plus Remboursé'] = DonneeMedicament['Base de remboursement 2013'] == 0
DonneeMedicament['Nouveau Remboursé'] = (DonneeMedicament['Base de remboursement 2013']>0) & (DonneeMedicament['Base de remboursement 2012']==0)
Rembourse2013 = DonneeMedicament[(DonneeMedicament['Nouveau Remboursé']==True) ]
NonRembourse2013 = DonneeMedicament[(DonneeMedicament['Plus Remboursé']==True) ]
Rembourse2013.to_excel("rembourse.xlsx", index=False)
NonRembourse2013.to_excel("NonRembourse2013.xlsx", index=False)

#on remarque qu'on peut avoir le sodage si l'on leve produit de Nom court
def ObtenirDosage(ligne):
    return str(ligne['NOM COURT']).replace (str(ligne['PRODUIT']), '').strip()



