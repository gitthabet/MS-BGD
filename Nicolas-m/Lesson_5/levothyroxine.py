# on utilise ici le requests.get

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
#on obtient la zone de texte de notre recherche

names = Series(names)
# str => transforme en string. strip() => vire les espaces
names = names.str.strip()

#sur une expression reguliere, trouver les chiffres
regex_dosage = re.compile(r'\d+')
names.apply(lambda x : regex_dosage.findall(x))

#sur une expression reguliere, trouver unité mg
regex_unite = re.compile(r'(microgrammes|µg|grammes|gL)')
names.apply(lambda x : regex_unite.findall(x))

regex_form = re.compile(r'comprim\xe9 s\xe9cable')
names.apply(lambda x : regex_form.findall(x))

a = names.apply(lambda x : regex_dosage.findall(x))
b = names.apply(lambda x : regex_unite.findall(x))
c = names.apply(lambda x : regex_form.findall(x))

d = {'dosage':a, 'unite':b,'forme':c}
e = DataFrame(d)