# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 08:41:35 2014

@author: Paco
"""

'''
Pour Levothyroxine
Liste des medicaments rembourses
Dosage + Unite + Forme
'''

import requests as req
from bs4 import BeautifulSoup as bs
import re

res = []

## post
payload = {'page': '1', 'btnMedic.x': '12', 'btnMedic.y': '7', 'choixRecherche': 'medicament', 'txtCaracteres': 'Levothyroxine', 'btnMedic': 'Rechercher'}
r = req.post("http://base-donnees-publique.medicaments.gouv.fr/index.php", data=payload)
soup = bs(r.text)

## get links
for link in soup.find_all('a', attrs={'class' : 'standart'}):
    
    title = link.get('title').split(':')[1].strip()
    # get name    
    name = title.split(',')[0]
    name1 = str(name.split()[0])
    name2 = str(name.split()[1])    
    dosage = int(name.split()[2])
    unite = str(name.split()[3])
    # get forme    
    galetruc = str(title.split(',')[1].strip()) 
        
    # link for infos    
    url = "http://base-donnees-publique.medicaments.gouv.fr/"+link.get('href')
    
    rr = req.get(url)
    soupp = bs(rr.text)

    # get price and re        
    remboursement = soupp.find('div', attrs={'class' : 'infosCnam'})  
    rembou = remboursement.text.split()    
    prix = str(rembou[2])   
    tauxrembou = str(rembou[8])    
    
    # get autorization
    autorization = soupp.find('div', attrs={'class' : 'alignright'})   
    auto = autorization.text.split()[4]

    # get comm
    comm = re.search('(.*)de commercialisation(.*)/', rr.text)   
    comm2 = comm.group(2).split('<br/>')[0].replace(":","").strip()
    
    res.append((name1+" "+name2,dosage,unite,galetruc,prix,tauxrembou+" %",str(auto),str(comm2)))
    
    #print res