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
                    ligne_annonce = [prix,annee,ville,km,0,pro_part,0,'?',0,0]
#                    print ligne_annonce
#                    data_captur.loc[len(data_captur)+1]=ligne_annonce
                    data_captur.loc[num_annonce]=ligne_annonce








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


#            print(soup.prettify())

print data_captur
data_captur.to_csv('data_captur.csv',sep=',')
