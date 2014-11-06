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
import statsmodels.api as sm


#TS
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

wiki_data.groupby(lambda x: x.year).mean()


# Viz


x = np.random.normal(size=100)
y = np.random.normal(size=100)
#figure = plt.figure()


#fig, axes = plt.subplots(2, 2)

#plt.close()
#figure = plt.figure()
#plt.plot(np.random.normal(size=100), linestyle='--', color='g', marker='o')


# labels
#fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
#ax.plot(randn(1000).cumsum())
#ax.set_xticks([0, 250, 500, 750, 1000])
#ax.set_xticklabels(['one', 'two', 'three', 'four', 'five'], rotation=30, fontsize='small')



#fig = plt.figure(); ax = fig.add_subplot(1, 1, 1)
#ax.plot(randn(1000).cumsum(), 'k', label='one')
#ax.plot(randn(1000).cumsum(), 'k--', label='two')
#ax.plot(randn(1000).cumsum(), 'k.', label='three')
#ax.legend(loc='best')

plt.savefig('test.svg')

#wiki_data.resample('M').plot()


death_data = pd.read_csv('CausesOfDeath_France_2001-2008.csv')
death_data['Value'] = death_data['Value'].str.replace(' ','')
death_data['Value'] = death_data['Value'].apply(lambda x : int(re.compile(r'[^0-9]').sub('0',x)))
death_data = death_data[['ICD10','Value','SEX','TIME']]

causes = death_data.groupby('ICD10')['Value'].sum().order(ascending=False)[0:5].index.values

#filtered = death_data[death_data['ICD10'].isin(causes)]
#filtered_agg = filtered.groupby(['ICD10','TIME']).sum()
#filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot()
#filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot(kind="bar")
#filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot(kind="barh")
#filtered_agg.reset_index().pivot('TIME', 'ICD10','Value').plot(kind="barh", stacked=True)


deases = death_data.groupby('ICD10')['Value'].sum().order(ascending=False)[0:10]

#deases.plot(kind='bar')

#cameras['Weight'].hist(bins=20)
#cameras['Weight'].plot(kind='kde')

#plt.scatter(cameras['Weight'], cameras['Price'])

cars = pd.read_csv('cars.csv',sep=';',index_col=0).drop('STRING')
cars['MPG'] = cars['MPG'].astype(float)
cars['Cylinders'] = cars['Cylinders'].astype(float)
cars['Weight'] = cars['Weight'].astype(float)
cars['Acceleration'] = cars['Acceleration'].astype(float)
cars['Horsepower'] = cars['Horsepower'].astype(float)
pd.scatter_matrix(cars, diagonal='kde', color='k', alpha=0.3)
