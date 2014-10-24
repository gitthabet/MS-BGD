import requests
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

python_list_data=[1,2,3,4]

np_converted_data = np.array(python_list_data)

print(np_converted_data.dtype)

np_list2 = np_converted_data  + np_converted_data 

print(np_list2)

test_data = np.random.normal(size=(4,4))

print(test_data)

""" access ligne """

print(test_data[0,:],test_data[:,0])
