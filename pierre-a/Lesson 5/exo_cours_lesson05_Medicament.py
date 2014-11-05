# -*- coding: utf8 -*-

import requests
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import re


substance = 'levothyroxine'
page = 1

payload = { 'page':1
    ,'affliste':0
    ,'affNumero':0
    ,'isAlphabet':0
    ,'inClauseSubst':'("00382","00382")'
    ,'nomSubstances':'(unable to decode value)'
    ,'typeRecherche':0
    ,'choixRecherche':'medicament'
    ,'txtCaracteres':'levothyroxine'
    ,'btnMedic.x':14
    ,'btnMedic.y':17
    ,'btnMedic': 'Rechercher'
    ,'radLibelle':2
    ,'txtCaracteresSub': ''
    ,'radLibelleSub':4
    }

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'

result = requests.post(url, data=payload)
soup = BeautifulSoup(result.text)
names = [ x.text for x in soup.find_all(class_="standart")]
names = Series(names)
names = names.str.strip()

l = [x.split(',')[0] for x in names]
medicament = Series([x.split(' ')[0] for x in l])
labo = Series([x.split(' ')[1] for x in l])
regex_dosage = re.compile(r'\d+')
regex_unite = re.compile(u'(microgrammes|µg|grammes|gL)')
dosage = []
unite = []
form = []
unite = [re.findall(regex_unite, x) for x in names]
unite = Series([item.encode('utf-8)') for sublist in unite for item in sublist])
dosage = [re.findall(regex_dosage, x) for x in names]
dosage = Series([item.encode('utf-8)') for sublist in dosage for item in sublist])
form = Series([x.split(',')[1] for x in names])


balise = soup.select('tr td + td a img')
remboursement = []
i=0
for b in balise:
    if b.get('alt') == 'Information importante':
        if balise[i+1].get('alt') == u'Information importante':
            remboursement.insert(i, u'Information importante')
            i += 1
        if balise[i+1].get('alt') == u'Retiré ou prochainement retiré du marché':
            remboursement.insert(i, u'Information importante : Retiré ou prochainement retiré du marché')
            i += 2
remboursement = Series(remboursement)

df = pd.concat([medicament, labo, dosage, unite, form, remboursement], axis = 1)
df.columns = ['medicament', 'laboratoire', 'dosage', 'unite', 'forme', 'remboursement']

df.to_csv('Medicaments.csv')

