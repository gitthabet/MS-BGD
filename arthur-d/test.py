# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests, re, unicodedata, StringIO, html5lib
from ghost import Ghost
from bs4 import BeautifulSoup


r = requests.get("http://www.leboncoin.fr/voitures/702652723.htm?ca=12_s")
if r.status_code == 200:
    soup = BeautifulSoup(r.text)
    balise_colRight = soup.find("div",{"class":"colRight"})

    print balise_colRight.find("a").getText()

    crit = balise_colRight.find("div",  {"class":"lbcParams criterias"})
    print crit.getText()

