import numpy as np
import pandas as pd
from pandas import Series, DataFrame

python_list_data = [1,2,3,4]
np_converted = np.array(python_list_data)

test_data = np.random.normal(size=(4, 4))


data = np.random.normal(size=(7,3))
positives = data > 0
#data[positives] = 1
#data[~positives] = 1
#np.where(data>0, 1,0)



peoples = np.array(['Fred', 'Bob', 'Alice', 'John', 'Gabrielle', 'Sara', 'Sam'])
relationships = np.array([ [0,2],[1,4],[6,5],[3,6]])

couples = peoples[relationships]


arr = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
arr.cumsum(0)
arr.cumsum(1)

data.sort(0)
data.sort(1)

walks = pd.DataFrame(np.random.normal(loc=8000,scale=1000,size=(4,4)), index=['lundi','mardi', 'mercredi','jeudi'],columns=['Alice','Bob','Sara','John'])

walks2 = pd.DataFrame(np.random.normal(loc=8000,scale=1000,size=(4,4)), index=['mardi', 'mercredi','jeudi','dimanche'],columns=['Alice','Bob','Sara','John'])
walks - walks.mean()
walks.sub(walks.mean(axis=1), axis=0)


myfunc = lambda x: x.max() - x.min()

def myfunc2(x):
    return Series([x.min(), x.max()], index=['min', 'max'])

walks.apply(myfunc,laxis=1)
print walks.apply(myfunc2,axis=1)

walks.rank()



# SQL
import sqlite3
import pandas.io.sql as sql
db = sqlite3.connect('mydb')

cursor = db.cursor()
cursor.execute('''
    DROP TABLE walks
''')
cursor.execute('''
    CREATE TABLE walks(id INTEGER PRIMARY KEY, name TEXT,
                       day TEXT, value REAL)
''')
db.commit()

query = "INSERT INTO walks(name,day,value) VALUES( ?, ?, ?)"

tuples = [tuple(v) for v in walks.unstack().reset_index().values]

cursor.executemany(query, tuples)
db.commit()

data_from_db = sql.read_sql('SELECT * FROM walks', db)
