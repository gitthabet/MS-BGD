# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests, re, StringIO, html5lib, csv
import pandas as pd
from pandas import Series


def main():
    url = "http://base-donnees-publique.medicaments.gouv.fr/"
    payload = {
        'page':
        'affliste':
        'affNumero':
        'isAlphabet':
        'inClauseSubst':
        'nomSubstances':
        'typeRecherche':
        'choixRecherche':
        'Rechercher':
        'radLibelle':
        'txtCaracteresSub':
        'btnSubst':
        'radLibelleSub1':
        'radLibelleSub':
    }
    r = requests.post(url, params=payload)
    names = []
    names = Series(names)

if __name__ == "__main__":
    main()