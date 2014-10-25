import requests
import numpy as np
import pandas as pd
from pandas import DataFrame,Series

#--------------------DECOUVERTE NUMPY

python_list_data=[1,2,3,4]
np_converted_data=np.array(python_list_data)


#concatene les deux listes
python_list_data+python_list_data
#effectue la somme
np_converted_data+np_converted_data
#Multiplication
4*np_converted_data

#generation de nombres aleatoires taille matrice 4 lignes et 4 colonnes
test_data=np.random.normal(size=(4,4))

#Acceder aux elements
test_data[0]
test_data[:,0]
test_dat[:,-1]

rand_data=np.random.normal(size=(4,4))
rand_data>0
np.where(data>0, 10, data)

test_data.mean(axis=1)
rddrdv