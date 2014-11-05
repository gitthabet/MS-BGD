# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

#Substance recherchee
substance = 'LEVOTHYROXINE'

#Parametres pour requete POST
params = {'txtCaracteres':substance, 
          'page':'1', 
          'affliste':'0',
          'isAlphabet':'0',
          'inClauseSubst':'0',
          'typeRecherche':'0',
          'choixRecherche':'medicament'}
          
#Requete POST
response = requests.post("http://base-donnees-publique.medicaments.gouv.fr/index.php#result", data=params)
soup = BeautifulSoup(response.text,'html.parser')

#Resultats
links = soup.findAll('a',class_='standart')
results = []
for link in links:
    result = []
    texte = link.text.strip()
    splits = texte.split()
    result.append(splits[0])
    result.append(splits[1])
    result.append(splits[2])
    result.append(re.sub(',','',splits[3]))
    result.append(texte.split(',')[1])
    results.append(result)

#DataFrame
df = pd.DataFrame(results)
df.columns=['Substance', 'Laboratoire', 'P', 'Unite', 'Forme galenique']

#Affichage du resultat
print df
