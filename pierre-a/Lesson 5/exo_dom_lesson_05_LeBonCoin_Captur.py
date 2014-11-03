# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
from pandas import Series, DataFrame
import numpy as np
import pandas as pd
import csv
from pygeocoder import Geocoder
import unicodedata

############################################################
# Normalize strings

def normalize(string):
    return unicodedata.normalize('NFKD',string).encode('ascii','ignore')

############################################################
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request successful'
        return BeautifulSoup(result.text, 'html.parser')
    else:
        print 'Request failed', url
        return None

############################################################
# return the links on LeBonCoin to announcements

def getLBC_Captur_links(region):

    soupLBC = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/' + region + '/?f=a&th=1&q=Renault+captur&it=1')

    # get number of announcements
    num_announcements = int(soupLBC.select('nav ul li span + span b')[0].text)

    # get number of pages
    num_pages = num_announcements / 35 + 1

    # get links to announcements
    links = []
    for page in range(0,num_pages):
        soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+ str(page+1) + '&q=Renault+captur')
        balises = soup.find_all('div', class_="list-lbc")[0].find_all('a')
        links += [balise.get('href').encode('utf-8') for balise in balises]

    return links

#############################################################################
# returns infos on announcements (pb with année-modèle)
# téléphone : m = re.search(r'(?<=0)[0-9]{10}', str(soup.text.encode('utf-8')))

def getInfosLBC(link):

    soup = getSoupFromUrl(link)
    infos = {}
    infos_list = ()
    # model
    model = soup.select('div h2')[0].text.upper()

    if 'CAPTUR' in model:
        model = re.sub('RENAULT', '', model)
        model = re.sub('CAPTUR', '', model)
        model = re.sub(';', '', model)
        infos ['Model'] = normalize(model)
        #infos product
        balises = soup.select('th')
        balises_clean = [balise.parent.text.replace('\t','').replace(' ','').replace('\n','') for balise in balises]
        for i in range(0,len(balises_clean)):
            split = balises_clean[i].split(':')
            # remove non digits elements
            if (split[0] == 'Prix' or split[0] == u'Kilométrage' or split[0] == 'Année-modèle'):
                infos[split[0]] = re.sub(r'\D', '', split[1])
            else :
                infos[split[0]] = split[1]


        # infos seller
        balise_seller = soup.find_all('div', 'upload_by')[0]
        if bool(balise_seller.text.encode('utf-8').find('Pro Véhicules')):
            infos['Vendeur'] = u'pro'
        else:
            infos['Vendeur'] = u'particulier'

        # Coordinates
        results = Geocoder.geocode(infos['Ville'])
        infos['Lat'] = results[0].coordinates[0]
        infos['Long'] = results[0].coordinates[1]

        # results on a list form
        #infos_list = pd.Series([infos['Model'], infos['Carburant'], infos['Kilométrage'], infos['Prix'], infos['Vendeur'], infos['Ville'], infos['Lat'], infos['Long']])
        infos_list = [normalize(unicode(infos['Model'])), normalize(unicode(infos['Carburant'])), normalize(unicode(infos[u'Kilométrage'])), infos['Prix'], normalize(unicode(infos['Vendeur'])), normalize(unicode(infos['Ville'])), infos['Lat'], infos['Long']]
        return infos_list
    else:
        return None


#############################################################################
# get infos from LaCentrale

# get links
def getLaCentrale_Captur_links():
    url = 'http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html'
    soupLC = getSoupFromUrl(url)
    balises = soupLC.select('tr td a')
    links = []
    for balise in balises:
        url0 = balise.get('href')
        if 'cote-auto-renault-captur' in url0:
            link = 'http://www.lacentrale.fr/' + url0
            links.append(link)
    links = list(set(links))  # remove duplicates
    return links

# get the price for each model
def getPrice_LC(links):
    Price_model = {}
    for link in links:
        soupPrice = getSoupFromUrl(link)
        model = soupPrice.select('div div div div h1')[0].text
        model = re.sub('Cote Renault CAPTUR - 2013 - ', '', model)
        model = re.sub(';', '', model)
        Price = soupPrice.find_all('span', class_ = "Result_Cote arial tx20")[0].text
        Price = re.sub(r'\D', '', Price)
        Price_model[model] = Price
    return Price_model

# compare prices between leboncoin and lacentrale
# return + if Price in Leboncoin > Price in Lacentrale
# LBC_Infos: List from getInfos_LBC(), Price_Model : dict from getPrice_LC()
def ComparePrices(LBC_Infos, Price_Model):
    Model_LBC = LBC_Infos[1]
    res = u'N/A'
    matches = []
    if Model_LBC.strip() != '':
        for key in Price_Model.keys():
            matches.append(find_ressemblance(key, Model_LBC))
        if len(matches) < 3:
            res = u'N/A'
        else:
            max_index = matches.index(max(matches))
            key_match = Price_Model.keys()[max_index]
            print key_match + '  ' + Model_LBC
            if Price_Model[key_match] < Model_LBC[4]:
                res = u'+'
            else:
                res = u'-'
    return res

# find number of matches between two sentences
def find_ressemblance(A, B):
    all_wordsA = re.findall(r'\w+', A)
    all_wordsB = re.findall(r'\w+', B)

    matches = set(all_wordsA) & set(all_wordsB)
    return len(matches)


#############################################################################
# MAIN

# La Centrale infos:
Links = getLaCentrale_Captur_links()
Price_Model = getPrice_LC(Links)

# Le Bon Coin infos
regions = [u'provence_alpes_cote_d_azur', u'ile_de_france', u'aquitaine']
infos = pd.DataFrame(columns = ('Région', 'Modèle', 'Carburant', 'Kilométrage', 'Prix', 'Vendeur', 'Ville', 'Latitude', 'Longitude', 'ArgusComparison'))

# get results and write to CSV
with open('Comparatif_Renault_Captur.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    l = 0
    for region in regions:
        links = getLBC_Captur_links(region)
        for link in links:
            inf = getInfosLBC(link)
            if inf:
                inf.insert(0, region)
                res = ComparePrices(inf, Price_Model)
                inf.insert(len(inf), res)
                infos.loc[l] = inf
                infos.to_csv('Infos_Renault_Captur.csv')
                l += 1





