# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:33:26 2014

@author: christian
"""

import requests
from bs4 import BeautifulSoup
import urlparse
import urllib
import re
from collections import OrderedDict
import json

# Constantes

regions = ['ile_de_france', 'provence_alpes_cote_d_azur', 'aquitaine']
#regions = ['aquitaine']

# Renault Captur
versions = ['life', 'zen', 'intens', 'business', 'helly hansen' 'arizona' ]
moteurs  = ['tce', 'dci']
dins     = ['90', '120']
cyls     = ['0.9', '1.2', '1.5']

# Pattern d'un numéro de téléphone inclus dans un texte
# On considère juste une suite de 10 chiffres

phonePattern = re.compile(r'.*(?:(?<!\d)(\d{10})(?!\d)).*')

def getSoupFromUrl(url):
    result =requests.get(url)
    if result.status_code == 200:
        return BeautifulSoup(result.text)
    else:
        print "Request failed : ", result.status_code

# Recherche de la liste des liens par region, ainsi que si c'est un pro

def getAnnonces(region) : 

    links = []
    pros = []
    
    url = 'http://www.leboncoin.fr/voitures/offres/'+region+'/?f=a&th=1&q=renault+captur&it=1'
    soup=getSoupFromUrl(url)
    
    next_pg = soup.find(text="Page suivante")
    
    pg = 0
    
    # On parcourt toutes les pages
    
    while (pg < 1) or next_pg:  
        
        pg += 1 
        mydivs = soup.findAll("div", class_="lbc")

        for line in mydivs:
            link = line.find_parents("a")[0]
            link = urlparse.urljoin(url, link['href'])
            links.append(link)
            pro = line.find('div', class_='category').text.strip()
            if pro == '(pro)':
                pros.append(link)
        
        next_pg = soup.find(text="Page suivante")
        if next_pg:
            next_url = next_pg.find_parent("a")['href']
            webpage = urllib.urlopen(next_url).read()
            soup = BeautifulSoup(webpage)
            
    return links, pros


# On enlève le symbole € et les KM

def formatPriceorKm(val):
    return val[:-2].strip().replace(" ", "")

# On cherche la version dans le titre de l'annonce

def checkVersion(text):
    
    for version in versions:
        ver = re.compile(version)
        if re.search(ver, text.lower()):
            return version
    
    return ""

# Appel Google pour trouver les coordonnées de la ville

def geocodeFromGoogle(addr):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" %   (urllib.quote(addr.replace(' ', '+')))
    try:
        data = urllib.urlopen(url).read()    
        info = json.loads(data).get("results")[0].get("geometry").get("location")  
        return str(info['lat']), str(info['lng'])
    except:
        return "", ""
        
# On va chercher tous les renseignements sur le véhicule de l'annonce

def getVehicle(link, pro):
    
    vehicule = {}
    
    # Les données des véhicules sont quasi toutes dans un td suivant le texte    
    
    liste = ['Prix :', 'Ville :', 'Code postal :', 'Marque :', 'Modèle :',\
             'Année-modèle :', 'Kilométrage :',\
             'Carburant :', 'Boîte de vitesse :']

    soup = getSoupFromUrl(link)
    
    # On va chercher le header pour la version
    
    head = soup.find('h2').text.strip()
    vehicule['Version :'] = checkVersion(head)
   
    # Pour les autres données on va les chercher dans la page   
   
    for item in liste:
        if item == 'Prix :':
            vehicule[item] = formatPriceorKm(soup.find('span', class_='price').text.strip())
        elif item == 'Kilométrage :':
            vehicule[item] = formatPriceorKm(soup.find(text=item).find_next('td').text.strip())
        else:
            try:
                vehicule[item] = soup.find(text=item).find_next('td').text.strip()
            except:
                vehicule[item] = ""
    
    # On va chercher le téléphone dans le texte de l'annonce
    # Il faudrait le chercher aussi dans le gif sous le "Voir le numéro" 
    # Trop compliqué pour moi
                
    text_ann = soup.find('div', class_='content').text.lower()
    phone = re.search(phonePattern, text_ann)
    if phone:
        vehicule['Phone :'] = phone.group(1)
    else:
        vehicule['Phone :'] = ""    
    
    # On cherche les chevaux DIN
    
    din   = '120' if text_ann.find('120') != -1 \
       else '90'  if text_ann.find('90') != -1 else "0"
    vehicule['DIN :'] = din
    
    # On cherche la cylindree
    
    cyl = '0.9' if text_ann.find('0.9') != -1 else '1.2'  if text_ann.find('1.2') != -1\
            else '1.5'  if text_ann.find('1.5') != -1 else ""
    vehicule['cyl :'] = cyl
    
    # On cherche le moteur
    
    moteur = 'tce' if text_ann.find('tce') != -1\
              else 'dci'  if text_ann.find('dci') != -1 else ""
    vehicule['Moteur :'] = moteur
    
    # Si c'est un dci la cylindree est forcement 1.5
    
    if vehicule['cyl :'] == "" and vehicule['Moteur :'] == "dci":
        vehicule['cyl :'] = "1.5"

    # On récupère la donnée pro de la liste
    
    if pro:
        vehicule['Pro :'] = "O"
    else:
        vehicule['Pro :'] = "N"

    # On initialise quote pour faciliter la comparaison avec les cotes en
    # mettant la cylindrée+dci ou tce+chevaux+version en clé

    vehicule['Cote :'] =   vehicule['cyl :']+'+'+vehicule['Moteur :']+'+' \
                         + vehicule['DIN :']+'+'+vehicule['Version :']
    
    vehicule['lat :'], vehicule['lng :'] = \
            geocodeFromGoogle(vehicule['Ville :']+',FR')
    
    return vehicule    

# Fonction uniq pour enlever les doublons d'une liste

def uniq(input):

    return list(OrderedDict.fromkeys(input))
 
# On va chercher les cotes de la Centrale concernant les Captur
           
def getQuotesFromLaCentrale():
    
    quotes = {}
    
    url = "http://www.lacentrale.fr/cote-voitures-renault-captur--2013-.html"
    soup=getSoupFromUrl(url)
    
    txt = "cote-auto-renault-captur" 
     
    urls = []
    
    # On recupere les liens des différentes cotes des captur    
    
    for a in soup.find_all("a", href = True):
        if a['href'].find(txt) != -1:
            urls.append("http://www.lacentrale.fr/"+a['href'])
            
    # Pour chaque version on va chercher la cote
    # Oblige de faire un uniq(urls) sinon doublons partout ??????
            
    for url2 in uniq(urls):
            soup2 = getSoupFromUrl(url2)
            
            for cyl in cyls:
                for moteur in moteurs:
                    for din in dins:
                        for version in versions:
                            if  (url2.find (cyl+'+'+moteur+'+'+din) != -1\
                            and url2.find (version) != -1):
                                quotes[cyl+'+'+moteur+'+'+din+'+'+version]\
                                     = formatPriceorKm(soup2.find("span", class_="Result_Cote arial tx20").text)
                                 
    
    return quotes
   
def main():    

    allVehicules = {}

    # On va chercher les cotes de la centrale    
    
    quotes = getQuotesFromLaCentrale()
    
    # On écrit les resultats dans un fichier .csv
    
    f = open('captur.csv', 'w')    

    f.write('Région,Version,Année-modèle,Kilométrage,Prix,Phone,Pro,Latitude,Longitude,Cote,+/- cher\n')

    for region in regions:
        
        allVehicules[region] = []   
        
        # On va chercher les annonces par région
        
        links, pros = getAnnonces(region)

        # On va chercher le détail de chaque annonce

        for link in links:
            allVehicules[region].append(getVehicle(link, link in pros))

        # On écrit (à la mano) le fichier .csv

        for vehicule in allVehicules[region]:

            f.write(region+',')
                    
            for val in ['Version :', 'Année-modèle :', 'Kilométrage :',\
                        'Prix :', 'Phone :', 'Pro :', 'lat :', 'lng :']:  
                f.write(vehicule[val]+',')

            # Si on n'a pas de cote on écrit ?,? pour les colonnes cote et +/- cher
            try:
                cote = float(quotes[vehicule['Cote :']])
                f.write(str(cote)+',')
                if   float(vehicule['Prix :']) > cote:
                        f.write('+') 
                elif float(vehicule['Prix :']) < cote:
                        f.write('-')
                elif float(vehicule['Prix :']) == cote:
                        f.write('=')
            except KeyError:
                f.write('?,?')
            f.write('\n')

    f.close()
    
if __name__ == "__main__":
    main()