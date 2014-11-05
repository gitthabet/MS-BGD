# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 23:39:50 2014

@author: Florian
"""

from pandas import DataFrame
import pandas as pd


datas = pd.read_excel("MEDICAM 2008-2013-AMELI.xls",sheetname=1)


datas= DataFrame(datas,columns=['NOM COURT','Base de remboursement 2008','Base de remboursement 2009','Base de remboursement 2010','Base de remboursement 2011','Base de remboursement 2012','Base de remboursement 2013'])
datas['Non Remboursé'] = datas['Base de remboursement 2013'] == 0
datas['Nouveau Remboursé'] = (datas['Base de remboursement 2013']>0) & (datas['Base de remboursement 2012']<=0)
NewRembourse = datas[(datas['Nouveau Remboursé']==True) ]
NonRembourse = datas[(datas['Non Remboursé']==True) ]

NewRembourse.to_excel("NouveauRemboursements2013.xlsx")
NonRembourse.to_excel("NonRembourse")


#print pandas