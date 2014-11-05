# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 08:58:11 2014

@author: wei he
"""

import requests
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import re
import html5lib


#levothyroxine = 'LEVOTHYROXINE'

#linkHidden = 'http://base-donnees-publique.medicaments.gouv.fr/index.php?txtCaracteres='
link = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'

substance='levoth'
pageLoad = {'page':1,
            'affliste':0,
            'affNumero':0,
            'isAlphabet':0,
            'inClauseSubst':0,
            'nomSubstances':'',
            'typeRecherche':0,
            'choixRecherche':'medicament',
            'txtCaracteres':'LEVOTHYROXINE',
            'radLibelle':2,
            'txtCaracteresSub':'',
            'radLibelleSub':4}

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html.parser")
    else:
        print 'Request failed', url
        return None


result = requests.post(link, data=pageLoad)
soupMed = BeautifulSoup(result.text, "html.parser")
#soupMed = BeautifulSoup(result.text)
#print soupMed

#print soupMed.find("a", {"class": "standart"})
#print soupMed.find("tr td + a")
names = [ x.text for x in soupMed.find_all(class_="standart")]

#print names
#names = [ x.text for x in soupMed.find_all("a", {'clasx_': 'standart'})
names = Series(names)
print names.str.strip()

#regex_dosage = re.compile(r'\d+')
#regex_


"""
names.str.strip()
names.apply(lambda x : regex.findall(x))
"""