# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 08:52:40 2014

@author: roms
"""

import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
import re

###############################################################################
# part 1
###############################################################################

# creates payload dict from url
url = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
payloadText = 'page=1&affliste=0&affNumero=0&isAlphabet=0&inClauseSubst=0&nomSubstances=&typeRecherche=0&choixRecherche=medicament&txtCaracteres=levothyroxine&radLibelle=2&txtCaracteresSub=&radLibelleSub=4'
payloadList = payloadText.split('&')
payloadDict = {}
for element in payloadList:
    payloadDict[element.split('=')[0]]=element.split('=')[1]
for element in payloadDict.keys():
    if(element not in ['nomSubstances','txtCaracteres','choixRecherche','txtCaracteresSub']):
        payloadDict[element]=int(payloadDict[element])
        
medics = requests.post(url, data = payloadDict)
medicsSoup = BeautifulSoup(medics.text, 'html.parser') # html-parser needed here!

# put all into a Series
names = [ x.text for x in medicsSoup.find_all(class_='standart') ]
names = Series(names)
names = names.str.strip() 


# finds 'dosage'
redosage = re.compile(r'\d+')
dosage = [int(redosage.findall(name)[0]) for name in names]

# finds 'unite'
reunite = re.compile(r'microgrammes|µg|mg|c|g')
unite = [reunite.findall(name)[0] for name in names]

# finds 'forme'
reforme = re.compile(r'comprimé sécable')
forme = [reforme.findall(name)[0] for name in names]

###############################################################################
# part 2
###############################################################################

# load base
base=DataFrame.from_csv('/home/roms/Telecom/P1/Kit big data/Work/MEDICAM 2008-2013-AMELI clean.csv',header=0,sep=',')

# medicaments derembourses en 2013
derembourse = base[(base['Montant remboursé 2012'] != "0") & (base['Montant remboursé 2013'] == "0")]['NOM COURT']
derembourse.to_csv('derembourse2013.csv')

# medicaments rembourses en 2013
rembourse = base[(base['Montant remboursé 2012'] == "0") & (base['Montant remboursé 2013'] != "0")]['NOM COURT']
rembourse.to_csv('rembourse2013.csv')


