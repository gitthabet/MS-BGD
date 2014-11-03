# -*- coding: utf-8 -*-
"""
Created on Sun Nov 02 11:36:39 2014

@author: Paco
"""

import requests as req
from bs4 import BeautifulSoup as bs
import re

'''
Générer un fichier de données sur le prix des Renault Captur sur le marché de l'occasion en Ile de France, PACA et 
Aquitaine. Vous utiliserez leboncoin.fr comme source. Le fichier doit être propre et contenir les infos suivantes:
- version (ok)
- année (ok)
- kilométrage (ok)
- prix (ok)
- téléphone du propriétaire
- professionnel ou particulier? (ok)  
Vous ajouterez une colonne sur le prix de l'Argus du modèle que vous récupérez sur ce site 
http://www.lacentrale.fr/cote-voitures-renault-captur--2013-.html.
Les données quanti (prix, km notamment) devront être manipulables (pas de string, pas d'unité).
Vous ajouterez une colonne si la voiture est plus chere ou moins chere que sa cote moyenne.﻿
'''

##############################################################    
# lacentrale.fr functions
##############################################################

## Get argus
def getArgus(url):
    argugus = []
        
    r = req.get(url)
    soup = bs(r.text)    
    for tda in soup.find_all('td', attrs={'class' : 'tdSD QuotMarque'}):
        rargus = req.get('http://www.lacentrale.fr/'+tda.find('a').get('href'))    
        soupargus = bs(rargus.text)
        argusprice = soupargus.find('span', attrs={'class' : 'Result_Cote arial tx20'})
        temp = tda.find('a').text + " : " + argusprice.text
        argugus.append((str(temp.split(':')[0].lower().strip()),int(temp.split(':')[1][:-1].replace(" ",""))))
    
    print argugus
    return argugus    
    
##############################################################    
# leboncoin.fr functions
##############################################################    

## Get the number of pages for a research 
def getNbPages(url):
    r = req.get(url)
    soup = bs(r.text)

    result = ""    
    
    pages = soup.find('ul', attrs={'id' : 'paging'})
    for pp in pages.find_all('a'):
        if(pp.text.find('>>')!=-1):
            result = re.search('(.*)?o=(.*)&q(.*)', pp.get('href'))
    
    return int(result.group(2))

## Get title of an announce
def getTitle(soup):
    return soup.find('h2',attrs={'id' : 'ad_subject'}).text

## Verify the brand in the title
def verifyBrand(title,brand):
    if(title.lower().find(brand) != -1):
        return True
    else:
        return False   

## Verify empty string
def verifyString(st):
    if st:
        return int(st)
    else:
        return 0

# Verify empty string (v2)
def verifyTitle(st):
    if st:
        return str(st)
    else:
        return 'na'

## Get coordinates for a city
## https://developers.google.com/maps/documentation/geocoding/
def getCoord(city,token_api):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+city+'+France&key='+token_api
    r = req.get(url)
    rep = r.json()

    lat =  rep['results'][0]['geometry']['bounds']['northeast']['lat']
    lng =  rep['results'][0]['geometry']['bounds']['northeast']['lng']
    
    print lat,lng
    return float(lat),float(lng)

## Get parameters for an announce
def getParams(soup,title,token_api):    
    version=""
    year=""
    milage=""
    price=""
    state=""
    city=""
    lat=""
    lng=""
    title = title.lower().replace('renault','')
    version = title.replace('captur','')
    version = verifyTitle(version.strip())    
    print version
            
    # other cara        
    params = soup.find('div',attrs={'class' : 'lbcParams criterias'})
    parath = params.find_all('th')
    paratd = params.find_all('td')
    for argth,argtd in zip(parath,paratd):
        # get year            
        if(argth.text.find("Ann") != -1):
            year=argtd.text.strip()
            year = verifyString(year)
            print year
        # get miles        
        if(argth.text.find("Kilom") != -1):   
            milage = argtd.text[:-2].replace(" ","")
            milage = verifyString(milage)
            print milage    
    
    # get phone number
    descri = soup.find('div', attrs={'class' : 'content'}).text
    pat = re.compile('\d{2}[-\.\s]??\d{2}[-\.\s]??\d{2}[-\.\s]??\d{2}[-\.\s]??\d{2}[-\.\s]??')                                      
    phonenum = pat.findall(descri)
    for i in range(0,len(phonenum)):
        phonenum[i] = str(phonenum[i]).replace(" ","")
     
    # get city   
    paroums = soup.find('div',attrs={'class' : 'lbcParams withborder'})
    parrath = paroums.find_all('th')
    parratd = paroums.find_all('td')        
    for arggth,arggtd in zip(parrath,parratd):   
        if(arggth.text.find("Ville") != -1):   
            city = arggtd.text.strip()
            city = verifyTitle(city)
            print city        
            
    # get price        
    price = soup.find('span',attrs={'class' : 'price'})
    price = price.text[:-1].replace(" ","")
    price = verifyString(price) 
    print price
            
    # get pro or not
    state = ""
    pro = soup.find('div',attrs={'class' : 'upload_by'})
    if(pro.text.find("Pro V") != -1):          
        state = "Professionnel"
    else:
        state = "Particulier" 
    print state

    lat,lng = getCoord(city,token_api)

    return version,year,milage,price,state,city,lat,lng,phonenum

##############################################################        
# leboncoin.fr VS lacentrale.fr
##############################################################

def testCateg(boncoin,argus):
    test1 = ['tce','dci']
    test2 = ['90','120']
    test3 = 'energy'
    test4 = ['arizona', 'intens', 'zen', 'life', 'business']         
    truc1 = ''
    truc2 = ''          
    truc3 = ''          
    truc4 = ''
           
    for t4 in range(0,len(test4)):
        if boncoin[0].find(test4[t4]) != -1:
            truc4 = test4[t4]      
                
    for t2 in range(0,len(test2)):
        if boncoin[0].find(test2[t2]) != -1:
            truc2 = test2[t2] 
                      
    for t1 in range(0,len(test1)):
        if boncoin[0].find(test1[t1]) != -1:
            truc1 = test1[t1]                    
         
    if boncoin[0].find(test3) != -1:
        truc3 = test3              
    
    for aa in range(0,len(argus)):
        if argus[aa][0].find(truc1)!=-1 and argus[aa][0].find(truc2)!=-1 and argus[aa][0].find(truc3)!=-1 and argus[aa][0].find(truc4)!=-1:    
            # print argus[aa][1],boncoin[3]  
            if boncoin[3] > argus[aa][1]:  
                return 'Superieur_a_Argus'
            elif boncoin[3] == argus[aa][1]:
                return 'Egal_a_Argus'
            else:
                return 'Inferieur_a_Argus'
        
##############################################################        
### MAIN
##############################################################

argus = getArgus('http://www.lacentrale.fr/cote-voitures-renault-captur--2013-.html')
regions=['ile_de_france','provence_alpes_cote_d_azur','aquitaine']
leboncoin = []
compare = []
token_google = 'AIzaSyBhhoOIKEQRxakb1CocIKZBuqeSbbLEoUQ'

for reg in range(0,len(regions)):

    url = 'http://www.leboncoin.fr/voitures/offres/'+regions[reg]+'/?o=1&q=Renault+Captur&th=0'
    maxpages = int(getNbPages(url))

    for p in range(0,maxpages):
        
        url2 = 'http://www.leboncoin.fr/voitures/offres/'+regions[reg]+'/?o='+str(p)+'&q=Renault+Captur&th=0'
        r = req.get(url2)
        soup = bs(r.text)
        
        for link in soup.find_all('a'):
            # get announces
            if link.get('href') is not None and link.get('href').find("htm?") != -1 and link.get('href').startswith('http://www.leboncoin.fr/voitures/'): 
                aa = link.get('href')
                rr = req.get(aa)
                soupp = bs(rr.text)
                
                # get params 
                title = getTitle(soupp)
                if(verifyBrand(title,'renault')):        
                    leboncoin.append(getParams(soupp,title,token_google))

for i in range(0,len(leboncoin)):
    compare.append(testCateg(leboncoin[i],argus))

lbc0 = [row[0] for row in leboncoin]
lbc1 = [row[1] for row in leboncoin]
lbc2 = [row[2] for row in leboncoin]
lbc3 = [row[3] for row in leboncoin]
lbc4 = [row[4] for row in leboncoin]
lbc5 = [row[5] for row in leboncoin]
lbc6 = [row[6] for row in leboncoin]
lbc7 = [row[7] for row in leboncoin]
lbc8 = [row[8] for row in leboncoin]
arg1 = [row[1] for row in argus]
final_table = [lbc0,lbc1,lbc2,lbc3,lbc4,lbc5,lbc6,lbc7,lbc8,compare]  

'''
for i in range(0,len(final_table[8])):
    final_table[8][i] = ''.join(final_table[8][i])
with open('list_renault.csv', 'w') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(numpy.asarray(final_table).T.tolist())    
'''