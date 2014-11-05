# coding: utf-8
#!/usr/bin/env python

__author__ = 'MP'


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import json
from pandas import DataFrame, Series
import slugify

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

class Drug:

    name = "Nan"
    dosage = "Nan"
    unit = "Nan"
    shape = "Nan"

    def parseDesc(self, desc):
        parts = desc.strip().split(' ')
        self.name = parts[0]
        self.dosage = parts[1]
        self.unit = parts[2]
        self.shape = parts[3]
        self.to_string()

    def get_drug(self, link, desc):
        print link
        self.parseDesc(desc)

    def to_string(self):
        print self.name + "_"+ self.dosage + "_"+ self.unit + "_"+ self.shape

        """
        regex_dosage = re.compile(r'\d+')
        regex_unite = re.compile(r'(microgrammes|g|grammes|gL)')
        phoneNumberPattern = re.compile(phoneNumberRegex)
        """

#"""""""""""""""""""""""""""""""""""""""""""""""" GET url list of drugs """"""""""""""""""""""""""""""""""""""""""""""""
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

url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"
r = requests.post(url, data=payload)
urlSoup = BeautifulSoup(r.text)

# for each medics
balise_table = urlSoup.find(class_=('result'))
balise_tr = balise_table.find_all('tr')

for tr in balise_tr:
    link = tr.find('a', {"class":'standart'})
    if link != None:
        drug = Drug()
        drug.get_drug(url + link.get('href'), link.text)

#urls = [ tr.find('a', {"class":'standart'}).get('href') for tr in balise_tr]
#print urls


"""
# avec Panda
names = Series(names)

# data cleaning
names.str.replace('\t', '')
names.str.strip() # enleve les espaces

# regex
regex_dosage = re.compile(r'\d+')
regex_unite = re.compile(r'(microgrammes|g|grammes|gL)')

names['dosage'] = names.apply(lambda x : regex_dosage.findall(x))
names['unite'] = names.apply(lambda x : regex_unite.findall(x)))


print names['dosage']
print names['unite']

"""


