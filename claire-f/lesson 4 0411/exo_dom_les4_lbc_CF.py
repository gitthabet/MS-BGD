# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 11:33:16 2014

@author: claire
"""

import requests
from bs4 import BeautifulSoup
import html5lib
import re
from pandas import Series, DataFrame


url_part = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=renault+captur&f=p'
API_KEY = 'AIzaSyCIjnHYw6D1Mn829dC09ep5k8VJKUJ5Iys'


def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text,'html5lib')
	else:
		print 'Request failed with ',url

def get_data_lbc(region,pro_part):
    url = 'http://www.leboncoin.fr/voitures/offres/'+region+'/?q=captur&f='+pro_part
    soup = getSoupFromUrl(url)
    print soup.title

    for link in soup.find_all('a'):
#    print(link.get('href'))
        url_detail = link.get('href')
# on sélectionne les pages qui correspondent à des annonces : en fin d'url apres/voitures/ : on a des chiffres 
#ex annonce : 62   http://www.leboncoin.fr/voitures/726746413.htm?ca=12_s

        if url_detail != None and len(url_detail.split('/')) > 4:
            fin_url= url_detail.split('/')[4]
            pat_annonce = re.compile(r'\d')      
            if pat_annonce.match(fin_url) != None:
#           on conserve le numéro d'annonce pour plus tard
                num_annonce = fin_url.split('.')[0]
#                print num_annonce

                soup = getSoupFromUrl(url_detail)
# <span class="price">18 890 €</span>
#            prix = soup.find('span',class_="price")
#            prix = (str(soup.find('span',class_="price")).split('>')[1]).split('€<')[0]
                print soup.title
                argus=None
                tce_dci = ""
                energy = ""
                chev = ""
                finition = ""
                title=str(soup.title)
                if "energy" in title.lower(): energy = "energy"
#                print "energy : ", energy
                if "tce" in title.lower(): tce_dci = "tce"
                elif "dci" in title.lower(): tce_dci = "dci"
                if "90" in title: chev="90"
                elif "120" in title: chev="120"
                if "arizona" in title.lower(): finition = "arizona"
                elif "intens" in title.lower(): finition = "intens"
                elif "zen" in title.lower(): finition = "zen"
                elif "life" in title.lower() : finition = "life"
                elif "business" in title.lower(): finition = "business"
                modele_fin = tce_dci+" "+chev+" "+energy+" "+finition
                print modele_fin

                str_prix = str(soup.find('span',class_="price")).strip()
                reg_prix = re.compile(r'\d{2} \d{3}')
                prix = 0
                if re.search(reg_prix,str_prix): prix = re.search(reg_prix,str_prix).group()
#                print prix
            
# pour info sert à retirer le regex            print reg_prix.sub(' ',prix).strip()

                data_td = soup.find_all('td')
#            print data_td
                ville = (str(data_td[1]).split('>')[1]).split('<')[0]
#                print ville
            # data_td[3 = <td>Renault</td>]
#            marque = str(data_td[3])
                marque = (str(data_td[3]).split('>')[1]).split('<')[0]
#                print "marque : ", marque
                modele = (str(data_td[4]).split('>')[1]).split('<')[0]
                annee = (str(data_td[5]).split('>')[1]).split('<')[0].strip()
                km_str = (str(data_td[6]).split('>')[1]).split('<')[0]
                km=0
                if re.search(reg_prix,km_str): km=re.search(reg_prix,km_str).group()
#                print km

#           récupérer le n° de tél qui est en gif 
                
                ##<a href='javascript:getPhoneNumberV2("http://www2.leboncoin.fr", 702652723, 1 )'>
                """
                from splinter.browser import Browser
                import os.path
                browser = Browser()
                rowser.visit('file://' + os.path.realpath('test.html'))
                elements = browser.find_by_css("#getPhoneNumberV2("http://www2.leboncoin.fr", num_annonce, 1 )")
                div = elements[0]
                print div.value
                browser.quit()
                """

               
                if marque == "Renault" and modele == "Captur":
                    
                    adresse = ville+', France'
                    url_api_maps="https://maps.googleapis.com/maps/api/geocode/json?address="+adresse+"&key="+API_KEY
                    results_api = requests.get(url_api_maps)
                    johnny = results_api.json()
                    lat = johnny['results'][0]['geometry']['location']['lat']
                    lng = johnny['results'][0]['geometry']['location']['lng']
 #                   print ville,lat,lng

                    ligne_annonce = [prix,annee,ville,km,0,pro_part,argus,'?',lat,lng]
#                    print ligne_annonce
#                    data_captur.loc[len(data_captur)+1]=ligne_annonce
                    data_captur.loc[num_annonce]=ligne_annonce



#Recherche de l'argus
columns = ['annee','cote']
index=['modele']
data_argus = DataFrame(index=index,columns=columns)


url = "http://www.lacentrale.fr/cote-voitures-renault-captur--2013-.html"
soup = getSoupFromUrl(url)
#print soup.title
data_td = soup.find_all('td',class_="tdSD QuotMarque")
#print data_td

for data in data_td:
    for link in data.find_all('a'):
        print link.get('href')
        url_detail = "http://www.lacentrale.fr/"+link.get('href')
        soup_detail = getSoupFromUrl(url_detail)
        titre = str(soup_detail.title)
#        print titre
        annee = titre[28:32]
        modele = titre[37:len(titre)-13]
        #modele=re.sub('$"S&S"', ' ', modele)
        print modele

        str_cote = str(soup_detail.find('span',class_="Result_Cote")).strip()
        reg_cote = re.compile(r'\d{2} \d{3}')
        cote = 0
        if re.search(reg_cote,str_cote): cote = re.search(reg_cote,str_cote).group()
#        print cote
        ligne_cote = [annee,cote]
        data_argus.loc[modele]=ligne_cote
        

print "=== ARGUS des CAPTUR : "
print data_argus




# data frame pour stocker les résultats
columns = ['prix','annee','ville','km','tel','pro_part','argus','pos_argus','lat','long']
data_captur = DataFrame(columns=columns)

#pros url  = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=captur&f=c'
#particuliers url  = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=captur&f=p'

for region in ['ile_de_france','aquitaine','provence_alpes_cote_d_azur']:
    print "region : ", region
    print 'pros'
    pro_part = 'c'
    get_data_lbc(region,pro_part)
    print 'particuliers'
    pro_part = 'p'
    get_data_lbc(region,pro_part)



print data_captur
data_captur.to_csv('data_captur.csv',sep=',')
