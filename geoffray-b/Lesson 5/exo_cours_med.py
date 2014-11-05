# -*- coding: utf8 -*-
import requests
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import re


substance = 'levoth'

payload =  { 'page':1
   , 'affliste':0
   , 'affNumero':0
   , 'isAlphabet':0
   , 'inClauseSubst':0
   , 'nomSubstances':''
   , 'typeRecherche':0
   , 'choixRecherche':'medicament'
   , 'txtCaracteres': substance
   , 'radLibelle':2
   , 'txtCaracteresSub': ''
   , 'radLibelleSub':4
    }

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'

result = requests.post(url, data=payload)
soup = BeautifulSoup(result.text)
names = [ x.text for x in soup.find_all(class_="standart")]
names = Series(names)
names = names.str.strip()
print names
regex_dosage = re.compile(r'\d+')
regex_unite = re.compile(r'(microgrammes|µg|grammes|gL)')