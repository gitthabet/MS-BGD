# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 10:27:14 2014

@author: Florian
"""
import pandas as pd
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse

death_data = pd.read_csv('CausesOfDeath_France_2001-2008.csv')