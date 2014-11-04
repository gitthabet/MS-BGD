# -*- coding: utf8 -*-

#cours du 28/10
import pandas as pd
from pandas import Series,DataFrame
import numpy as np

# ----------------------------------------manipulation de string

csv = 'Charles Miglietti,     47 ru Barult,  Homme    '
csv.split(',')
phone_number = '1-888-2343-2334'
phone_number.split('-')

# strip enlève les espaces
csv.split(',')[2].strip()

# remplace un caractère
csv.split(',')[2].replace('m','n')

# change la case
csv.split(',')[2].strip().lower()

# pour avoir un slogg de la chaine de cractère
csv.split(',')[1].strip().lower().replace(' ','-')

# index de caractère
csv.split(',')[1].strip().lower().replace(' ','-').index('b')

# -----------------------------les expressions regulières permettent de formater le texte

import re

credits_cards = 'Thanks for paying with 1089-1209-0323-0921'

# trouver la séquence d'un carte de crédit
cred = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')
cred.findall(credits_cards)

credits_cards = 'Thanks for paying with 1089-1209-0323-0921 and with 1234-1413-1231-1231'
cred.findall(credits_cards)

# remplace la fin du numéro de carte par XXXX-XXXX (attention $ ne transforme que si c'est la fin de la phrase)
cred = re.compile(r'\d{4}-\d{4}$')
cred.sub('XXXX-XXXX', credit_cards)

# pour trouver de l'aide taper sous Google regex email python

# pour extraire des adresses email
pattern = r'^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$'
regex_email = re.compile(pattern, flags=re.IGNORECASE)

match = regex_email.findall(email)


df = DataFrame(match)

# ----------------------------------------cours sur pandas

# df tableau des élèves avec @mail
# Dataframe.rename pour renommer les colonnes d'un DF
df = df.rename (columns = {'ancien' : 'nouveau', 'ancien' : 'nouveau'})

# on peut aussi faire un lambda pour changer les index de lignes
df.index = df.index.map(lambda x: 'Eleve ' + str(x))

# on peut supprimer les doublons
df.duplicated() #pour voir s'il y a des doublons
df.drop_duplicate() # pour les supprimer

# -------------------------- traiter le fichier aliments.csv
aliments = pd.read_csv('aliments.csv')

# realiser une matrice d'aliments x traces contenues
aliments['traces]'].isnull()
aliments_with_traces = aliments['traces'].dropna()

traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])
traces = set.union(traces_iter)

DataFrame(np.zeros((len(aliments_with_traces), len(traces))), columns= traces)
for i, tr in enumerate(aliments_with_traces.traces):
	dummies.ix[i, tr.split(',')] = 1

# autre méthode sur des colonnes plus simple
aliments_nutrition= aliment['nutrition_grade-fr'].dropna()
aliment['nutrition_grade-fr'].unique()
aliment['nutrition_grade-fr'].value_counts()
pd.get_dummies(aliments['nutrition_grade_fr'], 1)

# pandas gère bien les NAN ex:
aliments[u'energy_100g'].mean()

# quantisation
aliments[u'energy_100g'].dropna()
aliments[u'energy_100g'].value_counts()
# trop de valeurs => on a envie de créer des catégories ex: 5 catégories uniformément réparties ou par quantiles
pd.qcut(aliments[u'energy_100g'].dropna(), 5) # par quantile (même nombre par intervales)
pd.qcut(aliments[u'energy_100g'].dropna(), 5).levels

pd.cut(aliments[u'energy_100g'].dropna(), 5) # intevales égaux 

# ------------------------------------merger 2 jeux de données ex: evolution population avec revenu fiscaux (fichier xls recupérés sur l'insee)
insee1 = 
insee2 = 

# join 
pd.merge(insee1, insee2, on='CODGEO') # merge = logique des join comme en sql
pd.merge(insee1, insee2, right_on='CODGEO', left_on='dfpej')
insee1 = insee1.set_index('CODEGEO')
insee2 = insee2.set_index('CODEGO')

# normallisation de l'index car l'index n'était finalement pas tout à fait le même
fonction strip_corse qui remplace 2A et 2b par 20
insee1.index = insee1.index.map(strip_corse)
insee2.index = insee2.index.map(strip_corse)

all_insee_data = pd.merge(insee2, insee1, left_index = true, right_index = ture) # et là on a tout


# pour debugger en python on tape debug et on peut naviguer dans le code super pratique !