# -*- coding: utf-8 -*-
"""
Created on Tue Nov 04 08:42:11 2014

@author: Florian
"""

import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re

name_medicament = "Levoth"
data_post = {
'page': 1,
'affliste':0,
'affNumero':0,
'isAlphabet':0,
'inClauseSubst':0,
'nomSubstances':'',
'typeRecherche':0,
'choixRecherche':'medicament',
'txtCaracteres':'A',
'btnMedic':'Rechercher',
'btnMedic.x':0,
'btnMedic.y':0,
'radLibelle':2,
'txtCaracteresSub':'',
'radLibelleSub':4
}



def parsage(Intitule):
    Splits= Intitule.split(',')
    dictionnaire = {}
    print Splits
    gal = Splits[-1]
    num = re.compile(r'\d+')
    results = num.search(Intitule)
    if results:
        results= results.group(0)
    unite = re.compile(r'(microgrammes|µg|grammes|gL)')
    unite = unite.search(Intitule)
    if unite:
        unite = unite.group(0)
    dictionnaire['unite'] = unite
    dictionnaire['gal'] = gal
    dictionnaire['num']= results
    return dictionnaire
    
def getPageFromUrl(url):
    page= requests.get(url)
    prettypage= BeautifulSoup(page.text)
    return prettypage

def getFicheCIP(CIP):
    url = 'http://www.codage.ext.cnamts.fr/codif/bdm_it//fiche/index_fic_medisoc.php?p_code_cip='+CIP+'&p_site=AMELI'
#    print url
    page = getPageFromUrl(url)
    rex = re.compile(r"NON Remboursable\n")
    results =  rex.search(page.text)
#    print results
    if results:
#        print results.group(0)
        return "Non Remboursable"
    return 'lal'
    
car ='A'
while(ord(car)<=ord('Z')):
    print car
    data_post['txtCaracteres'] = car
    Results = requests.post('http://base-donnees-publique.medicaments.gouv.fr/index.php',data = data_post )
    links = [(x.text,x.get("href")) for x in BeautifulSoup(Results.text).select('table.result a.standart')]
    car =chr(ord(car)+1)
    for x in links:
        print x[1]
        page = getPageFromUrl('http://base-donnees-publique.medicaments.gouv.fr/'+x[1])
        rex = re.compile(r'Code\sCIP((\d|\s|ou|:|-)+)')
#        print('"Code CIP.*"')
#        print page.text
        Codes = rex.findall(page.text)
        extract_codes = [x[0] for x in Codes]
        for code in extract_codes:
            splits = code.split("ou")
            CIP = splits[1].replace(' ','')
            Remboursable = getFicheCIP(CIP)
            print 'Remboursable >>> ' , Remboursable
            print 'CIP >>>' , CIP
            
#            print splits
#        print extract_codes
#        print Code
#        print Code
#liens = [x.text for x in liens]
#noms  = []
    print links[0]
#liste = []
print 'end'

#for link in links : 
#    print link.text
#    liste.append(parsage(link.text))
#df = DataFrame(liste)
#print df

#print links