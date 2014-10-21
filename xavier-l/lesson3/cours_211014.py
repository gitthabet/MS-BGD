import requests
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import sqlite3
import pandas.io.sql as sql


print "puissance de Numpy"
print "------------------"
pythonlistdata = [1,2,3,4]

npconvertdata = np.array(pythonlistdata)

npconvertdata
pythonlistdata

print "avantage de numpy = objet vecteur sur lequel on peut calculer"
print npconvertdata+npconvertdata
print pythonlistdata+pythonlistdata


testdata = np.random.normal(size=(4,4))

print testdata
print testdata.shape
print testdata.dtype
print testdata[0]
print testdata[:,0]
positif = testdata>0
print testdata[positif]
testdata[positif] = 1
print testdata
testdata[~positif] = 0
print testdata

# retrouver comment distribuer
#people = [['Tom'],['Sara'],['Eric']]
#relation = np.array([0,1],[1,2])
#print people[relation]

print "lire broadcasting pour travailler sur le matrices et vesteurs"

print "la valeur de pandas"
print "--------------------"

walks = pd.DataFrame(np.random.normal(loc=8000,scale=1000, size=(4,4)), index=['lundi','mardi','mercredi','jeudi'], columns=['Alice','Sara','Marc','Paul']
print walks

print walks.ix['lundi']
print walks['Alice']

walks.mean() #colone
walks-walks.mean() #colone

walks.means(axis=1) #ligne
walks.sub(walks.means(axis=1),0) #pour soustraire les lignes sur les colones


myfunc = lambda x: x.max() - x.min()
myfunc(np.array([10,9,32,42]))

walks.apply(myfunc, axis=0)
walks.apply(myfunc, axis=1)

walks.apply(np.mean,axis=1) #identique .mean()

walks.rank()
walks.rank(axis=1,ascending=false)

walks.unstack()
walks.unstack().ix['Alice']
walks.unstack().ix[,:'Lundi']

walks.unstack().reset_index()

.set_index()

sql.read_sql








