# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 10:05:33 2014

@author: christian
"""

import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import requests
import json
from bs4 import BeautifulSoup
import re

mol = "levothyroxine"



def postSoupFromUrl(url, payload):
    result =requests.post(url, data = payload)
    if result.status_code == 200:
        return BeautifulSoup(result.text)
    else:
        print "Request failed : ", result.status_code

def main():
    
    substance = 'levoth'    
    
    payload = {'txtCaracteres': substance,
    'page' :"1",
    'affliste' :"0",
    'affNumero' :"0",
    'isAlphabet' :"0",
    'inClauseSubst' :"0",
    'nomSubstances' :"",
    'typeRecherche' :"0",
    'choixRecherche' :"medicament",
    'btnMedic.x' :"11",
    'btnMedic.y' :"14",
    'radLibelle' :"2",
    'txtCaracteresSub' :"",
    'radLibelleSub' :"4"}
    
    url = "http://base-donnees-publique.medicaments.gouv.fr/index.php#result"
    
    soup = postSoupFromUrl(url, payload) ;
        
    names = [ x.text for x in soup.find_all(class_="standart")]
    
    names = Series(names).str.strip()

    regex_dosage = re.compile(r'\d+')
    regex_unite = re.compile(r'(microgrammes|µg|grammes|gL)')
    
    
        
if __name__ == "__main__":
    main()
    
    