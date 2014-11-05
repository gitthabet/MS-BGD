__author__ = 'martin-prillard'

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json
from pandas import DataFrame, Series

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

payload = {
    'page':1
    ,'affliste':0
    ,'affNumero':0
    ,'isAlphabet':0
    ,'inClauseSubst':0
    ,'nomSubstances':''
    ,'typeRecherche':0
    ,'choixRecherche':'medicament'
    ,'txtCaracteres':'levoth'
    ,'radLibelle':2
    ,'txtCaracteresSub': 2
    ,'radLibelleSub':4}

r = requests.post("http://base-donnees-publique.medicaments.gouv.fr/index.php#result", data=payload)
urlSoup = BeautifulSoup(r.text)
names = [ x.text for x in urlSoup.find_all(class_='standart')]
# Avec Panda
names = Series(names)
# Data cleaning
names.str.replace('\t', '')
names.str.strip() # enleve les espaces

regex_dosage = re.compile(r'\d+')
regex_unite = re.compile(r'(microgrammes|g|grammes|gL)')

names['dosage'] = names.apply(lambda x : regex_dosage.findall(x))
names['unite'] = names.apply(lambda x : regex_unite.findall(x))

print names['dosage']
print names['unite']

# for each
"""
for name in names:
    print name

    pattern = name.compile(pattern)
    print pattern;
"""
    #phoneNumbersTags = list(set(phoneNumberPattern.findall(unicode(adsTag.string))))
    #if phoneNumbersTags:
    #    phoneNumbersList = phoneNumbersList + phoneNumbersTags

    #adsUrlSoup = getSoupFromUrl(urlAds)
    #price = int(re.sub(r'\D', "", adsUrlSoup.find(class_ = "price").select('span')[0].string))
    #year = re.sub(r'\D', "", adsUrlSoup.find(class_ = "lbcParams criterias").select('tr + tr + tr td')[0].string)
    #price = int(re.sub(r'\D', "", adsUrlSoup.find(class_ = "price").select('span')[0].string))
    #year = re.sub(r'\D', "", adsUrlSoup.find(class_ = "lbcParams criterias").select('tr + tr + tr td')[0].string)

    # a_balises = urlSoup.find_all('a', class_='standart')
    #return [balise.get('href') for balise in a_balises]

# write into csv file
#.to_csv('exo_cc_lesson4.csv')
