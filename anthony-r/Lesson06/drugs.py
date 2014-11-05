import requests
import numpy as np
import pandas as pd
import re

from pandas import DataFrame, Series

from bs4 import BeautifulSoup

payload = {
    'page':1,
    'affliste':0,
    'affNumero':0,
    'isAlphabet':0,
    'inClauseSubst':0,
    'nomSubstances':'',
    'typeRecherche':0,
    'choixRecherche':'medicament',
    'txtCaracteres':'levothyroxine',
    'btnMedic.x':9,
    'btnMedic.y':15,
    'btnMedic':'Rechercher',
    'radLibelle':2,
    'txtCaracteresSub': '',
    'radLibelleSub':4
    }

raw_data = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php#result',data=payload).text
html = BeautifulSoup(raw_data)

drugss = html.findAll('a',class_="standart")

drugs = [drug.text for drug in drugss]

names = Series(drugs)

names.str.strip()

regex_dosage = re.compile(r'\d+')
regex_units = re.compile(r'(microgrammes|µg|grammes)')

names['dosage'] = names.apply(lambda x: regex_dosage.findall(x))
names['units'] = names.apply(lambda x: regex_units.findall(x))
