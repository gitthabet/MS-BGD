import requests
# html5lib parser de meilleur qualite
import html5lib
import unicodedata
from bs4 import BeautifulSoup
import json
import pandas as pd
from pandas import Series, DataFrame
import re

###############################################################################

""" 								Strings									"""

###############################################################################


csv = ' Jonathan Ohayon,         24 rue du code,        Homme  ,  ,  2'

""" separe par les lignes """
csv.split(',')

""" enlever les espaces """
csv.split(',')[1].strip()

""" voir la doc python sur les Strings """


###############################################################################

""" 							Regular Expression 							"""

###############################################################################


""" 		expression reguliere : Voir Cheat Sheet regular expression 		"""

credits_cards = 'Thanks for using 1234-5678-9101-1213'

cred = re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')

print cred.findall(credits_cards) # find compiler inside file

cred = re.compile(r'\d{4}-\d{4}$')

print cred.sub('XXXX-XXXX',credits_cards) # replace compiler for a patern

# regex "specific choice" in google
# regex101 to transform text into regular expression

# flags pour manipuler les caracteres 

###############################################################################

""" 								Dataframe 								"""

###############################################################################

df=DataFrame(csv.split(',')
)

df.index = df.index.map(lambda x : 'donnees '+ str(x))  #renome les indexs

print df

#df.columns.rename  renome les colonnes