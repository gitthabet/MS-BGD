# -*- coding: utf-8 -*-

###############################################################################
# Imports, déclarations
###############################################################################
#Imports
import pandas as pd
import re

#Déclarations
b_2008 = "Base de remboursement 2008"
b_2009 = "Base de remboursement 2009"
b_2010 = "Base de remboursement 2010"
b_2011 = "Base de remboursement 2011"
b_2012 = "Base de remboursement 2012"
b_2013 = "Base de remboursement 2013"
col_res = ['PRODUIT','INFOS','QTE','UNITE','FORME']

###############################################################################
# Fonctions
###############################################################################
def infos(ligne):
    texte = str(ligne["NOM COURT"]).replace(str(ligne['PRODUIT']),'').strip()
    unite, forme = "", ""
    try:
        qte = re.search(r'\d+[,.]*\d*', texte).group(0)
        splits = [split.strip() for split in texte.split(qte,1)]
        splits = splits[1].split(None,1) if len(splits)>=2 else [""]
        unite = splits[0].split("/")[0].strip()
        forme = splits[1].strip() if len(splits) >= 1 else ""
    except:
        qte = None          
    return pd.Series({'INFOS':texte, 'QTE':qte, 'UNITE':unite, 'FORME':forme})

###############################################################################
# Programme principal
###############################################################################
#Lecture du fichier
df = pd.read_excel("MEDICAM 2008-2013-AMELI.xls",sheetname=1)

#Informations provenant du nom du produit
df = df.merge(df.apply(lambda x: infos(x), axis=1), left_index=True, right_index=True)

#1 - Médicaments remboursés en 2013
df1 = df[df[b_2013]>0].loc[:,col_res]

#2 - Médicaments remboursés en 2013 mais pas avant
df2 = df[(df[b_2012]<=0) & (df[b_2011]<=0) & (df[b_2010]<=0) & (df[b_2009]<=0) & (df[b_2008]<=0)].loc[:,col_res]

#3 - Médicaments remboursés en 2008 mais pas en 2013
df3 = df[df.loc[:,b_2013]<=0][df.loc[:,b_2008]>0].loc[:,col_res]

#Enregistrement des résultats
df1.to_csv('rembourse.csv', index=False)
df2.to_csv('rembourse_new.csv', index=False)
df3.to_csv('derembourse.csv', index=False)