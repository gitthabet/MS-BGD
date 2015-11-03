# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse
import matplotlib.pyplot as plt
from numpy.random import randn



ameli = pd.ExcelFile('MEDICAM 2008-2013-AMELI.xls')
medics = ameli.parse(ameli.sheet_names[1])
names = medics['NOM COURT']
reg = re.compile(r'([A-Z\s]+)(\d+,?\d+)\s(\w+)\s([A-Z\sé]+)\s(\d+)')


def extract(x):
    matches = reg.findall(x)
    return Series(*matches)

ext=names.dropna().apply(extract)
