# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 18:58:06 2014

@author: louarradi
"""

import requests
from bs4 import BeautifulSoup
import html5lib
import os, sys
import json


def ResulltFromUrl(url):
    result = requests.get(url)
    if result.status_code !=200:
        return None
    else:
        return BeautifulSoup(result.text, "html5lib")
        
   

def NbMoyContributeur(Id,motDePasse,contributeurGithub) :
    url = "https://api.github.com/users/" + contributeurGithub + "/starred/owner"
    requete = requests.get(url, auth=(Id,motDePasse))
    if requete.status_code != 200:
        return 0.
    else:
        ResultatRequeteJson = json.loads(requete.content)
        NbDepots = 0.
        NbEtoiles = 0.
    for element in ResultatRequeteJson:
        NbEtoiles = NbEtoiles + element.get("stargazers_count",0.)
        NbDepots =  NbDepots + 1
        if NbDepots == 0.:
            return 0.
        else:
            return NbEtoiles/NbDepots         
            
            
def main():
  
    if len(sys.argv) != 3:
        print "Erreur : l'identifiant et le mot de passe github sont attendus en entrée"
    else:
        IDgit = sys.argv[1]
        MDPgit = sys.argv[2]
        soupePage = ResulltFromUrl("https://gist.github.com/paulmillr/2657075")
        balisesCont = soupePage.find(class_="markdown-body js-file ").find("table").find("tbody").find_all("tr")
        tableCont = [];
        indice = 0
    for balise in balisesCont:
        indice += 1
        Cont = {}
        Cont["rang"] = indice
        Cont["id"] = balise.select("td:nth-of-type(1) > a")[0].string
        Cont["lien"] = balise.select("td:nth-of-type(1) > a")[0].get("href")
        Cont["etoiles"] = NbMoyContributeur(IDgit,  MDPgit,Cont["id"])
        tableCont.append(Cont)
        triContributeurs = sorted(tableCont, key=lambda contrib: contrib["etoiles"])
        print "Classement des contributeurs de github par étoiles (moyenne sur les dépots):"
    for Contributeur in triContributeurs:
        print " " + str(Contributeur["id"]) + " : " + str(Contributeur["etoiles"]) + " étoiles"
    

if __name__ == '__main__':

    print(ResulltFromUrl('https://gist.github.com/paulmillr/2657075'))
    