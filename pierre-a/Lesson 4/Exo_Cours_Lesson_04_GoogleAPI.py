from google.directions import GoogleDirections
import pandas as pd
from pandas import DataFrame

gd = GoogleDirections('AIzaSyBGrDxPZz6WuOkZXgJSATpvAkjHhhwd_UU')

Villes = ['caen', 'paris', 'marseille', 'lyon', 'lille']


Dist = pd.DataFrame([[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]] ,
index = Villes,
columns = Villes)


for ville1 in Villes:
    for ville2 in Villes:
        if ville1 != ville2:
            res = gd.query(ville1,ville2)
            Dist.at[ville1, ville2] = res.distance
        else:
            Dist.at[ville1, ville2] = 0

print Dist



