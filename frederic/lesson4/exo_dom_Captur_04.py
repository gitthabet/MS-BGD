# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import unicodedata as uni
#from pandas import Series, DataFrame

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


def getLongLat(city,cp):
   
   link = ('https://maps.googleapis.com/maps/api/geocode/json?address='+city+'+'+cp+'&key=AIzaSyDZsaD7vuuFVqQ3kYLV9nefQTvmm0jGLKo')
   
   print link
   r = requests.get(link)
   print r.status_code
   if(r.ok):
        repoItem = json.loads(r.text)
   latitude= repoItem['results'][0].get('geometry').get('location').get('lat')
   longitude= repoItem['results'][0].get('geometry').get('location').get('lng')
 
   return longitude,latitude


def getAllCars(region,modele):
#    region='ile_de_france'
#    modele='captur'
    url='http://www.leboncoin.fr/voitures/offres/'+region+'/?o=1&q=renault%20'+modele+'&f=c'
    print 'a url' , url
    soup=getSoupFromUrl(url)
    b_nb = normalize(soup.select('ul li span + span')[0].text)
    nbPages=1
    if re.match(r'(?P<nbA>[0-9]+)([ a-zA-Z]*)',b_nb):
               nbPages=(int(re.sub(r'(?P<nbA>[0-9]+)([ a-zA-Z]*)',r'\g<nbA>',b_nb))/35)+1

    links=[]
    for i in range(0,nbPages):
       
        url= 'http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+ str(i+1) +'&q=renault%20'+modele+'&f=c'
        print 'b url' , url
        soup = getSoupFromUrl(url)
#        print soup

        balises_a = soup.select('a')
#        print balises_a
        links = [balise.get('href') for balise in balises_a]
#        print links
        
    OkLinks=[]
    link=[]
    for link in links:
        print 'c link' , link
        if link is not None:
            if re.match(r'^(http://|https://)?(www.leboncoin.fr/voitures/)[0-9]+(.htm)',link):
                OkLinks.append(link)

#    print 'OkLinks ', OkLinks
    return OkLinks                    


def InfoCar(lien):
#    for lien in LinkCars :
        print 'lien ', lien
        soupCar = getSoupFromUrl(lien)
        
        balInfVeh=soupCar.select('tr th + td')
        infVeh=[normalize(bInfVeh.text).strip() for bInfVeh in balInfVeh]
        prix=infVeh[0].replace(' ','')
        ville=infVeh[1]
        cp=infVeh[2]

        longitude,latitude=getLongLat(ville,cp)

        km=infVeh[5].replace(' ','').lower().replace('km','')


        balInfVersion=soupCar.select('div[class=header_adview] h2[id=ad_subject]')
        infVersion=[normalize(bInfVersion.text).strip() for bInfVersion in balInfVersion]
        version=infVersion[0]

        balInfDiv=soupCar.select('div[class=content]')
        infDiv=[normalize(bInfDiv.text).strip() for bInfDiv in balInfDiv]
        words=infDiv[0].split("\n")
        numtel=''
        for w in words :
            if re.match(r'(^(.)*(?P<tel>(0[0-9]([ .-]?[0-9]{2}){4})))',w):
               numtel=re.sub(r'(^(.)*(?P<tel>(0[0-9]([ .-]?[0-9]{2}){4}))(.)*)',r'\g<tel>',w)

        return version,km,prix,ville,cp,longitude,latitude,numtel


  

#################################################################################################
#                                                                                               #
"""                                         MAIN                                              """
#                                                                                               #
#################################################################################################

links=[]
balises_a=[]
#region='ile_de_france'
#modele='captur'
LinkCars=[]
print 'a'
LinkCars=getAllCars('ile_de_france','captur')
print 'b'
LinkCars+=getAllCars('provence_alpes_cote_d_azur','captur')
LinkCars+=getAllCars('aquitaine','captur')

Cars=[]

for lien in LinkCars:
    TabCar={}
    version,km,prix,ville,cp,longitude,latitude,numtel=InfoCar(lien)
    TabCar["version"]=version
    TabCar["km"]=km
    TabCar["prix"]=prix
    TabCar["ville"]=ville
    TabCar["cp"]=cp
    TabCar["longitude"]=latitude
    TabCar["latitude"]=cp
    TabCar["numtel"]=numtel
    Cars.append(TabCar)

