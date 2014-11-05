# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 18:41:52 2014

@author: christian
"""

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import re

digit = re.compile(r'(\d+)(.*)?')

# Dans la colonne NOM COURT on peut enlever le produit pour obtenir dosage et forme

def removePRODUIT(row) :
    return str(row['NOM COURT']).replace (str(row['PRODUIT']), '').strip()
 
 # On cherche le dosage
 
def findDosage(s):
    try:
        if s[0].isdigit():
            return str(s)
        else:
            dose = re.search(digit, s[0])
            if dose:
                return str(dose.group(1)+" "+dose.group(2))
    except:
        return ""

# Et la forme (trop compliqué...)

def findForme(s):
    return str(s)
        
def main():
    
    xl = pd.ExcelFile("MEDICAM 2008-2013-AMELI.xls")

    df = xl.parse("MedicAM 0813").dropna()    
 
    # Pour le remboursement il suffit de de chercher les colonnes  Base de remboursement 2013
    # et Base de remboursement 2012
   
    df['Plus Remboursé'] = df['Base de remboursement 2013'] == 0
    df['Nouveau Remboursé'] = (df['Base de remboursement 2013']>0) & (df['Base de remboursement 2012']==0)

    NewRemb2013 = df[(df['Nouveau Remboursé']==True) ]
    NonRemb2013 = df[(df['Plus Remboursé']==True) ]
    NewRemb2013.to_excel("NewRemb2013.xlsx", index=False)
    NonRemb2013.to_excel("NonRemb2013.xlsx", index=False)

    # On cherche à trouver la forme et le dosage de chaque medicament

    df = df[['NOM COURT', 'PRODUIT']]
    
    df['GAL'] = df.apply(lambda x : removePRODUIT(x), axis=1)
    
    df['DOSE'] = df['GAL'].apply (lambda x : findDosage(str(x).split(' ')[:2]))

    df['FORME'] = df['GAL'].apply (lambda x : findForme(str(x).split(' ')[2:]))

    df.to_excel("MedGal2013.xlsx")    
    
if __name__ == "__main__":
    main()