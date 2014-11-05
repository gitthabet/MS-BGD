# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 14:39:15 2014

@author: fhohner
"""

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse
import xlrd




xl = pd.ExcelFile('/home/frederic/MEDICAM 2008-2013-AMELI.xls')
xl.sheet_names
df = xl.parse("MedicAM 0813")
df.head()
type(df)
df.axes
df.shape
df.ix

m=df["NOM COURT"]
i=0
#while i< df["NOM COURT"].count:
  if re.search(r'MG|FL',m[1]):
    unite=re.search(r'MG|FL',m[1]).group(0)
  else:
    unite=""  
#  i+=1
  
#s=Series(unite,index=df.index) 
df["unite"]=unite
