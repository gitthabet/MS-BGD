# -*- coding: utf8 -*-

"""
Created on Tue Nov 04 02:52:50 2014

@author: xlioneton
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pandas import Series,DataFrame


#----------------------------- Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None
        
#---------------------------- Retourne un Dataframe avec les liens des annonces
def getlinks(region, vendeur):

    #initialisation des variables
    pageSuivante = True
    if vendeur=="Particulier":
        url = "http://www.leboncoin.fr/voitures/offres/"+region+"/?o=1&q=renault%20captur&it=1&f=p"
    if vendeur=="Pros":
        url = "http://www.leboncoin.fr/voitures/offres/"+region+"/?o=1&q=renault%20captur&it=1&f=c"
    tableau = pd.DataFrame()
    liens = {}
    vente = {}
    reg = {}
    i=0
    
    #récupération des liens et retour du résultat dans un DataFrame
    while pageSuivante:
             
        soup = getSoupFromUrl(url)	
        
        #utilisation d'un regex sur le lien à récupérer    
        if region == "ile_de_france":       
            balises = soup.find_all(href=re.compile(r'(http:\/\/)(www\.leboncoin\.fr\/)(voitures\/)([\d]{9})\.(htm\?ca\=12\_s)$'))
        if region == "aquitaine":
            balises = soup.find_all(href=re.compile(r'(http:\/\/)(www\.leboncoin\.fr\/)(voitures\/)([\d]{9})\.(htm\?ca\=2\_s)$')) 
        if region == "provence_alpes_cote_d_azur":
            balises = soup.find_all(href=re.compile(r'(http:\/\/)(www\.leboncoin\.fr\/)(voitures\/)([\d]{9})\.(htm\?ca\=21\_s)$'))
        
        for lien in balises:
            liens[i]=lien.get('href')
            vente[i]=vendeur
            reg[i]=region
            i=i+1
        
        #vérification s'il y a une page suivante
        nav = soup.find_all("a", text = "Page suivante")
        
        if nav:
            url = nav[0].get('href')
        else:
            pageSuivante = False
            tableau = DataFrame.from_dict(liens,'index')
            tableau.columns = ['Lien']
            Vendeurs = DataFrame.from_dict(vente,'index')
            Vendeurs.columns = ['Vendeur']
            Regions = DataFrame.from_dict(reg,'index')
            Regions.columns = ['Region']
            tableau = pd.merge(tableau, Vendeurs, left_index=True, right_index=True)
            tableau = pd.merge(tableau, Regions, left_index=True, right_index=True)
    
    return tableau

#---------------------------- Retourne un Dataframe avec les caractéristiques de la vente
def getCaracteristiques(Index,url):
    
    caract = {}
    soup = getSoupFromUrl(url)
    
    #récupération du prix à l'aide d'une regex
    balise_prix = soup.find_all("span", class_="price")
    regex_prix = re.compile(r'(\d{2}\s\d{3})')
    prix = balise_prix[0].find(text=regex_prix)
    if prix:
        prix = int(prix[:-2].replace(" ",""))
    else:
        prix = "inconnu"
    caract['Prix'] = prix
    
    balises = soup.find_all("tr")

    #récupération de la ville    
    ville = str(balises[1])
    index1 = ville.find("<td>")+4 
    index2 = ville.find("</td>")
    ville = ville[index1 : index2]
    caract['Ville'] = ville
    
    #récupération du code postal
    codePostal = str(balises[2])
    index1 = codePostal.find("<td>")+4 
    index2 = codePostal.find("</td>")
    codePostal = codePostal[index1 : index2]
    caract['Code postal'] = codePostal
    
    #récupération de la marque
    marque = str(balises[3])
    index1 = marque.find("<td>")+4 
    index2 = marque.find("</td>")
    marque = marque[index1 : index2]
    caract['Marque'] = marque
    
    #récupération du modèle
    modele = str(balises[4])
    index1 = modele.find("<td>")+4 
    index2 = modele.find("</td>")
    modele = modele[index1 : index2]
    caract['Modele'] = modele
    
    #récupération du kilométrage
    km = str(balises[5])
    index1 = km.find("<td>")+4 
    index2 = km.find("</td>")
    km = km[index1 : index2]
    km = km[:-3].replace(" ", "")
    caract['Kilometrage'] = km
    
    
    tableau = DataFrame.from_dict(caract, 'index').T
    tableau.index = [Index]    
    
    return tableau


#----------------------------- Main

region = ["ile_de_france","aquitaine","provence_alpes_cote_d_azur"]
vendeur = ["Particulier","Pros"]

# récupération des liens
# je n'ai pas réussi à faire un boucle pour ajouter les dataframe et redéfinir l'index...
t11 = getlinks("ile_de_france", "Particulier")
t12 = getlinks("ile_de_france", "Pros")
t21 = getlinks("aquitaine", "Particulier")
t22 = getlinks("aquitaine", "Pros")
t31 = getlinks("provence_alpes_cote_d_azur", "Particulier")
t32 = getlinks("provence_alpes_cote_d_azur", "Pros")

t12.index += len(t11)
t21.index += len(t11)+len(t12)
t22.index += len(t11)+len(t12)+len(t21)
t31.index += len(t11)+len(t12)+len(t21)+len(t22)
t32.index += len(t11)+len(t12)+len(t21)+len(t22)+len(t31)

TableauLiens=t11.append(t12).append(t21).append(t22).append(t31).append(t32)


Resultats = pd.DataFrame(columns = ['Lien','Vendeur','Region','Ville','Kilometrage','Code postal','Prix','Marque','Modele'])

# récupération des caractéristiques des voitures pour chaque lien
for ind in TableauLiens.index :
    temp = getCaracteristiques(ind,TableauLiens.loc[ind,'Lien'])
    Ligne = pd.merge(TableauLiens, temp, left_index=True, right_index=True)
    Resultats.loc[ind]=Ligne.loc[ind]

Resultats.to_csv(path_or_buf='Resultats.csv', sep=";")


    
    