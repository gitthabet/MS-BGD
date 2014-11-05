# -*- coding: utf8 -*-
import requests
import pandas as pd
import numpy as np
import html5lib
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import re

substance = 'levoth'

payload =  { 'page':1
   , 'affliste':0
   , 'affNumero':0
   , 'isAlphabet':0
   , 'inClauseSubst':0
   , 'nomSubstances':''
   , 'typeRecherche':0
   , 'choixRecherche':'medicament'
   , 'txtCaracteres':substance
   , 'radLibelle':2
   , 'txtCaracteresSub': ''
   , 'radLibelleSub':4
    }

url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
regex_CIP = re.compile(r'\d{5}\s\d{3}\s\d{3}\s\d\s\d')
regex_dosage = re.compile(r'\d+')
regex_unite = re.compile(r'(microgrammes|µg|grammes|gL)')

result = requests.post(url, data=payload)
# print result.text
soup = BeautifulSoup(result.text)
#print type(soup)
test = soup.find('table',class_="result").text
print test
# links = [(link.text,link.get("href")) for link in soup.find('table',class_='result').findall('a',class_='href')]
# print links

# for link in links:
#    page = requests.get('http://base-donnees-publique.medicaments.gouv.fr/'+link[1])
#    pagesoup= BeautifulSoup(page.text,"html5lib")
#    print pagesoup
#    Codes = regex_CIP.findall(pagesoup.text)
   #print Codes[0]
   # CIP = [code[0] for code in Codes]

# names = Series(names)
# names = names.str.strip()
# print names
