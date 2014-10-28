import numpy as np
import pandas as pd
import requests
from pandas import Dataframes, Series

python_list_data=[1,2,3,4]
type(python_list_data)

np_converted_data=np.array(python_list_data)
type (np_converted_data)

np_converted_data.shape
np_converted_data.type
np_converted_data.dtype
np_converted_data+np_converted_data
4*np_converted_data

test_data=np.random.normal(size(4,4))
test_data[0]
test_data[:,0]
test_data[:,0]
test_data[-1]

np.where(data>0,10,data)

test_data.sum() ou &)np.sum(test_data)
test_data.sum(axis=1)
test_data.mean(axis=0)
test_data.cumsum(axis=0)
test_data.sort(1)
test_data.dot(test_data) #produit matriciel
test_data.transpose

#########Pandas##############

walks=pd.DataFrame(np.random.normal(loc=8000,scale=1000,size(4,4)), index=['Lundi','Mardi','Mercredi'],columns=['Alice','Bob','Jason','Kelly'])
walks.apply(myFunction,axis=1)
walks.rank()
pd.readc_csv(fichier.csv;sep=";")
walks.unstack 