# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb
from datetime import datetime
from dateutil.parser import parse

death_data = pd.read_csv('CausesOfDeath_France_2001-2008.csv')
death_data['Value'] = death_data['Value'].str.replace(' ','')

#death_data['Value'].astype(int)

death_data['Value'] = death_data['Value'].apply(lambda x : int(re.compile(r'[^0-9]').sub('0',x)))

death_data.groupby(['SEX','TIME']).size()
death_data.groupby(['SEX','TIME']).size()


for name, group in death_data.groupby('TIME'):
    group.to_csv('death_year_'+str(name)+'.csv')


#select coloumn
death_data.groupby('SEX')['Value'].sum()
# death_data['Value'].groupby(death_data['SEX'])


dem_dep_all = pd.ExcelFile('DEMANDE_DEPT.xlsx')
dem_dep = []
for spe in dem_dep_all.sheet_names:
    dem_dep_spe = dem_dep_all.parse(spe)
    dem_dep_spe.columns = dem_dep_spe.ix[1].values
    dem_dep_spe = dem_dep_spe.drop([0,1])
    ss = Series(dem_dep_spe['nb_rech'].values, name=dem_dep_spe[u'Activité'].iloc[0], index=dem_dep_spe['dept'].values)
    ss = ss.drop_duplicates()
    dem_dep.append(ss)

dem_dep_concat = pd.concat(dem_dep ,axis=1)
mapping = { u'Allergologue': u'med_spe'
        , u'Dermatologue' : u'med_spe'
        , 'Gynécologue' : u'premier_sec'
        , u'Dentiste' : u'dentiste'
        , 'Kiné' : u'prof_para'
        , 'Médecin généraliste' : u'premier_sec'
        , u'Ophtalmo' : u'med_spe'
        , 'Ostéopathe' : u'prof_para'
        , 'Pédiatre' : u'premier_sec'
        , u'Aide_personnes_agees' : u'prof_para'
        , u'Infirmier' : u'prof_para'
        , u'Sage-femme' :u'naissance'
        , 'Maternité' : u'naissance'
        , u'Hopital' : u'med_para'
        , u'Clinique' :u'med_para'
        , u'Pharmacie' : u'pharmacie'
        , u'Cardiologue' : u'med_spe'
        , u'Chirurgien plasticien' : u'med_spe'
        , 'Diététiciens' : u'prof_para'
        , u'ORL' : u'med_spe'
        , 'Gastro-entérologue' : u'med_spe'
        , u'Orthophoniste' : u'prof_para'
        , u'Orthoptiste' : u'prof_para'
        , u'Podologue' : u'prof_para'
        , u'Radiologue': u'med_spe'
         }
demand_agg = dem_dep_concat.groupby(mapping,axis=1).sum()

cameras = pd.read_csv('Camera.csv',sep=';',index_col=0).drop('STRING')
cameras.rename(columns={'Weight (inc. batteries)':'Weight'},inplace=True)
cameras['Max resolution'] = cameras['Max resolution'].astype(float).astype(int)
cameras['Weight'] = cameras['Weight'].astype(float)


cameras.groupby(lambda x : x.split(' ')[0])['Max resolution'].mean()
price_groups = pd.cut(cameras['Price'].astype(float), 4)
cameras.groupby(price_groups).mean()

death_data.set_index('TIME').groupby(level=0)['Value'].sum()

def spread(arr):
    #pdb.set_trace()
    return arr.max() - arr.min()


cameras.groupby(lambda x : x.split(' ')[0])['Max resolution'].agg(spread)

cameras.groupby(lambda x : x.split(' ')[0])['Max resolution'].agg([spread, 'mean'])

cameras.groupby(lambda x : x.split(' ')[0]).agg({'Max resolution' : spread, 'Weight' : 'mean'})

cameras.groupby(lambda x : x.split(' ')[0])['Max resolution'].describe()


def remove_mean(arr):
    #pdb.set_trace()
    return arr - arr.mean()

cameras.groupby(lambda x : x.split(' ')[0]).transform(remove_mean)

def top_n(df, n=5, column="Max resolution"):
    return df.sort(column,ascending=False)[:n]

print cameras.groupby(lambda x : x.split(' ')[0]).apply(top_n,1)



time = '08-10-1998'
datetime.strptime(time, '%d-%m-%Y')
datetime.strptime(time, '%d-%m-%Y').year
parse(time)
parse(time, dayfirst=True)

nursing = pd.read_csv('Nursing_data_11_29_2012.csv', sep='\t')
nursing = nursing.set_index('Date')
nursing.index = nursing.index.map(lambda x : parse(x))


wiki_data  = pd.read_csv('smallwikipedia.csv', sep=';')
wiki_data = wiki_data.drop(0)
wiki_data = wiki_data.set_index('Date')
wiki_data.index = wiki_data.index.map(lambda x : parse(x))
wiki_data['changes'] = wiki_data['changes'].astype(int)
wiki_data['2004']
wiki_data['2004':'2006']
wiki_data.resample('M')
wiki_data.resample('W')

pd.date_range('4/1/2012', '6/1/2012')
pd.date_range('1/1/2000', periods=10, freq='1h30min')
wiki_data.resample('M').shift(1) - wiki_data.resample('M')

wiki_data.resample('D', fill_method='ffill')

# time zones
print wiki_data.groupby(lambda x: x.year).mean()
