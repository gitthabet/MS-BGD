import requests

import numpy

import numpy as np

import pandas as pd

from pandas import DataFrame, Series



test_data = np.random.normal(size=(4,4))
positives = test_data>0
test_data[positives]
test_data[~positives] = 0
test_data

data = np.random.normal(size=(7,3))

peoples = (['Tom'],['Sara'],['etc'],['John'],['Tim'],['jane'])