# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import sys
import json
#import shutil
#import pytesseract
#from PIL import Image


#Fonction de téléchargement
def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text,'html.parser')
    else:
        return None


#Extraction des données de l'annonce
def extract_from_line(soup, regex):
    result = ""
    obj_th = soup.find('th',text=regex)
    if obj_th != None:
        obj_td = obj_th.find_next_sibling("td")
        if obj_td != None:
            result = obj_td.text
    return result


#def tel_img(tel_id):
#    encoded_object = get_page("http://www2.leboncoin.fr/ajapi/get/phone?list_id=" + tel_id)
#    data = json.loads(str(encoded_object))
#    if data != "":
#        response = requests.get(data('phoneUrl'), stream=True)
#        with open('test.gif', 'wb') as out_file:
#            shutil.copyfileobj(response.raw, out_file)
#        out_file.close()
#        result = pytesseract.image_to_string(Image.open('test.gif'))
#    return result


#Géolocalisation
def geo_data(query):
    lng = ""
    lat = ""
    apikey = "AIzaSyDGI9264LWSIWH9LcxbYG_NVHH5Nk66VOU"    
    encoded_object = get_page("https://maps.googleapis.com/maps/api/geocode/json?address="+query+"&key="+apikey)
    data = json.loads(str(encoded_object))
    if len(data['results']) > 0:
        loc = data['results'][0]['geometry']['location']
        lng = loc['lng']
        lat = loc['lat']
    return lng, lat


#Traitement des annonces
def process(region, marque, modele, vendeur):
#   Déclarations    
    regex_ad = re.compile(r'leboncoin.fr/voitures/[\d*]', re.IGNORECASE)
    regex_next_page = re.compile(r'.*PAGE.*SUIVANTE.*', re.IGNORECASE)
    regex_annee = re.compile(r'.*Ann.*e-mod.*le.*', re.IGNORECASE)
    regex_km = re.compile(r'.*Kilom.*trage.*', re.IGNORECASE)
    regex_carbu = re.compile(r'.*Carburant.*', re.IGNORECASE)
    regex_boite = re.compile(r'.*Bo.*te.*vitesse.*', re.IGNORECASE)
#    regex_tel = re.compile(r'.*getphoneNumber.*', re.IGNORECASE)
    regex_tel = re.compile(r'((\+|00)33\s?|0)[1-9](\s?\d{2}){4}')
    regex_ville = re.compile(r'.*Ville.*', re.IGNORECASE)
    regex_cp = re.compile(r'.*Code.*Postal.*', re.IGNORECASE)      
    regex_int = re.compile(r'[^0-9]')
    links = []
    results = []
    result = []
  
#   Construction de l'URL
    url = "http://www.leboncoin.fr/voitures/offres/" + region + "/?q=" + \
          marque + "%20" + modele + "&f=" + vendeur
  
#   Première page de résultats  
    soup = get_page(url)
    while soup != None:
#       Liens vers les annonces          
        links += [link.get('href') for link in soup.findAll('a',href=regex_ad)]
#       Page suivante        
        next_page_a = soup.find('a',text=regex_next_page)
        soup = get_page(next_page_a.get('href')) if next_page_a != None else None
    
    for link in links:
#       Lecture de l'annonce        
        soup = get_page(link)
        result = []
        if soup != None:
#           Marque, modele, particulier/pro, region
            result.append(marque)
            result.append(modele)
            result.append("Pro" if vendeur=="c" else "Particulier")
            result.append(region)  
#           Code postal
            result.append(extract_from_line(soup, regex_cp))  
#           Ville
            result.append(extract_from_line(soup, regex_ville))           
#           Longitude & latitude renseignées après
            result.append("")
            result.append("")
#           Prix            
            price_span = soup.find('span',class_='price')
            if price_span != None:
                price_str = str(price_span.text)
                result.append(int(re.sub(regex_int,'',price_str)))
            else:
                result.append(0)
#           Cote renseignée après
            result.append(0)
            result.append("")                
#           Année                r = 
            result.append(re.sub(regex_int,'',extract_from_line(soup, regex_annee)))
#           Kilométrage
            result.append(re.sub(regex_int,'',extract_from_line(soup, regex_km)))
#           Carburant
            result.append(extract_from_line(soup, regex_carbu))
#           Boite
            result.append(extract_from_line(soup, regex_boite))
#           Telephone
#            tel_a = soup.find('a',href=regex_tel)
#            if tel_a != None:
#                print tel_img(tel_a.get('href').split(',')[1].strip()) 
            content = soup.find('div',class_='content').text
            tel = re.search(regex_tel,content)
            result.append(tel.group(0) if tel!=None else "")
            results.append(result)
            
#   Resultats
    return results         


#Cote Argus
def argus(base_url,rel_url,version):
    millesime = version.split('+')[0]
    carburant = version.split('+')[1]
    url = base_url + rel_url
    resultat = 0
    regex_cote = re.compile(r'.*C.*te.*'+millesime+'.*', re.IGNORECASE)
    regex_carbu = re.compile(r'.*'+carburant+'.*', re.IGNORECASE)
    regex_int = re.compile(r'[^0-9]')
    regex_res = re.compile(r'.*Result.*C.*te.*', re.IGNORECASE)
    soup = get_page(url)
    link = soup.find('div',class_='CoteListMillesime').find('a',href=regex_cote)
    if link!= None:
        soup = get_page(base_url + str(link.get('href')))
        links = soup.findAll('td',class_="tdSD QuotNrj")
        for link in links:
            l = link.find('a',text=regex_carbu)
            if l!=None:
                soup = get_page(base_url + "/" + str(l.get('href')))
                res_div = soup.find('div',class_=regex_res)
                if res_div != None:
                    resultat = soup.find('div',class_=regex_res).text
                    resultat = int(re.sub(regex_int,'',resultat))
                    break
    return resultat
    

###############################
#PROGRAMME PRINCIPAL
###############################

#Recherche des annonces pro pour Renault Captur en IDF
print "Recherche des annonces"
df = pd.DataFrame(process("ile_de_france","RENAULT","CAPTUR","c"))
df = df.append(process("ile_de_france","RENAULT","CAPTUR","p"))
df = df.append(process("provence_alpes_cote_d_azur","RENAULT","CAPTUR","c"))
df = df.append(process("provence_alpes_cote_d_azur","RENAULT","CAPTUR","p"))
df = df.append(process("aquitaine","RENAULT","CAPTUR","c"))
df = df.append(process("aquitaine","RENAULT","CAPTUR","p"))

df.columns=['Marque', 'Modele', 'Type de vendeur', 'Region', \
            'CP', 'Ville', 'Longitude', 'Latitude', 'Prix', \
            'Cote','Comparaison','Annee','Km','Carburant','Boîte','Telephone']

#Argus
print "Recherche de la cote Argus"
versions = pd.unique((df.Annee+'+'+df.Carburant).values.ravel())
argus_base_url = "http://www.lacentrale.fr"
argus_rel_url = "/cote-voitures-renault-captur---suv_4x4.html"
for version in versions:    
    df.Cote[df.Annee+'+'+df.Carburant==version] = argus(argus_base_url,argus_rel_url,version)

#Comparaison Argus & Prix
df.Comparaison[df.Prix-df.Cote>0] = "Prix eleve"
df.Comparaison[df.Prix-df.Cote<0] = "Prix non eleve"
df.Comparaison[df.Prix-df.Cote==0] = "Prix correct"

#Longitude/Latitude
print "Geolocalisation"
query_list = pd.unique((df.CP+"+"+df.Ville).values.ravel())
for query in query_list:
    lon, lat = geo_data(query)
    df.Longitude[df.CP+"+"+df.Ville==query] = lon
    df.Latitude[df.CP+"+"+df.Ville==query] = lat
    
#Sauvegarde au format CSV  
print "Enregistrement des resultats"
df.to_csv('resultats.csv',sep=';',header=True,index=False)
