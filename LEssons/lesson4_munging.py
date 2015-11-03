# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re

csv = ' John,     47 rue Barrault, 36 ans  '

credits_cards = ' Thanks for paying with 1098-1203-1233-2354'
cred = re.compile(r'\d{4}-\d{4}$')
cred.sub('XXXX-XXXX',credits_cards)



email = '''
Voici le fichier complété et le calendrier et la liste des adresses des élèves (elles ne seront opérationnelles que la semaine prochaine).








 pierre.arbelet@telecom-paristech.fr francois.blas@telecom-paristech.fr geoffray.bories@telecom-paristech.fr claire.chazelas@telecom-paristech.fr dutertre@telecom-paristech.fr nde.fokou@telecom-paristech.fr wei.he@telecom-paristech.fr anthony.hayot@telecom-paristech.fr frederic.hohner@telecom-paristech.fr yoann.janvier@telecom-paristech.fr mimoune.louarradi@telecom-paristech.fr david.luz@telecom-paristech.fr nicolas.marsallon@telecom-paristech.fr paul.mochkovitch@telecom-paristech.fr martin.prillard@telecom-paristech.fr christian.penon@telecom-paristech.fr gperrin@telecom-paristech.fr anthony.reinette@telecom-paristech.fr florian.riche@telecom-paristech.fr romain.savidan@telecom-paristech.fr yse.wanono@telecom-paristech.fr ismail.arkhouch@telecom-paristech.fr philippe.cayeux@telecom-paristech.fr hicham.hallak@telecom-paristech.fr arthur.dupont@telecom-paristech.fr dabale.kassim@telecom-paristech.fr xavier.lioneton@telecom-paristech.fr sarra.mouas@telecom-paristech.fr jonathan.ohayon@telecom-paristech.fr alix.saas-monier@telecom-paristech.fr thabet.chelligue@telecom-paristech.fr amoussou@telecom-paristech.fr pierre.arbelet@telecom-paristech.fr
'''


pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex_email = re.compile(pattern, flags=re.IGNORECASE)

pattern = r'([A-Z0-9_%+-]+)\.?([A-Z0-9_%+-]*)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex_email = re.compile(pattern, flags=re.IGNORECASE)


#regex_video = re.compile(r'watch\?v=([A-Za-z0-9_\.-]+)')
#map(lambda x : video.findall(x), rihanna)



matches = regex_email.findall(email)

ores_paris_not_null = res_paris.dropna()




## Rename
df = DataFrame(matches)

df = df.rename(columns = {0:'firstname', 1:'lastname', 2:'ecole',3:'domain'} )
df.index = df.index.map(lambda x: 'Eleve ' +str(x))

#df.duplicated(['firstname'])
#df.drop_duplicates()


## MERGE

def strip_corse(val):
    if type(val) == int:
        return val
    if val == 'nan':
        return -1
    return int(re.sub('(A|B)', '0',val))

insee1 = pd.read_csv('base-cc-evol-struct-pop-2011.csv')
insee2 = pd.read_csv('base-cc-rev-fisc-loc-menage-10.csv')

insee1 = insee1.set_index('CODGEO')
insee2 = insee2.set_index('CODGEO')

insee2.index = insee2.index.map(strip_corse)
insee1.index = insee1.index.map(strip_corse)

insee_merge = pd.merge(insee1, insee2, left_index=True, right_index=True)

cams = pd.read_csv('Camera.csv',delimiter=';')
cams= cams[['Model','Max resolution','Release date']]


aliments = pd.read_csv('aliments.csv', sep='\t')

#combine first
df1 = DataFrame([[np.nan, 3., 5.], [-4.6, np.nan, np.nan], [np.nan, 7., np.nan]])
df2 = DataFrame([[-42.6, np.nan, -8.2], [-5., 1.6, 4]], index=[1, 2])
df1.combine_first(df2)


# FILTER OUT
traces = aliments['traces'].dropna()


## MAP

mapping ={'France':'UE', 'Turquie':'Asie'}

aliments.countries.map(mapping)
aliments[u'energy_100g'].dropna().map(lambda x: max(x,1500))


### Pivot
cities = [
         ['lundi','temperature',28]
         ,['lundi','ensoleillement',4]
         ,['lundi','pollution',5]
         ,['lundi','pluie',100]
         ,['mardi','temperature',28]
         ,['mardi','ensoleillement',4]
         ,['mardi','pollution',5]
         ,['mardi','pluie',100]
         ,['mercredi','temperature',28]
         ,['mercredi','ensoleillement',4]
         ,['mercredi','pollution',5]
         ,['mercredi','pluie',100]
         ,['jeudi','temperature',28]
         ,['jeudi','ensoleillement',4]
         ,['jeudi','pollution',5]
         ,['jeudi','pluie',100]
         ,['vendredi','temperature',28]
         ,['vendredi','ensoleillement',4]
         ,['vendredi','pollution',5]
         ,['vendredi','pluie',100]
         ]
cities_data = DataFrame(cities, columns=['jour','attribute','value'])

cities_data.pivot('jour','attribute','value')


## DESCRIPTIVE

aliments[u'origins'].value_counts()


## DUMMIES

aliments_with_traces = aliments.ix[aliments.traces.dropna().index]
traces_iter = (set(x.split(',')) for x in aliments_with_traces['traces'])
traces = set.union(*traces_iter)
dummies = DataFrame(np.zeros((len(aliments_with_traces), len(traces))), columns=traces)
for i, tr in enumerate(aliments_with_traces.traces):
     dummies.ix[i, tr.split(',')] = 1

dummies_nutrition = pd.get_dummies(aliments['nutrition_grade_fr'])


## QUantization

pd.value_counts(pd.qcut(aliments[u'energy_100g'].dropna(),5))
pd.value_counts(pd.cut(aliments[u'energy_100g'].dropna(),5))
