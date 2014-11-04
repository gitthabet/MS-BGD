# -*- coding: utf-8 -*-
import urllib2
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
#from splinter import Browser
import numpy as np
#from selenium import webdriver
import unicodedata
import json
from lxml.cssselect import CSSSelector as css


# RESTE A FAIRE
# récupérer les numéros de téléphone des vendeurs (vis JS ?)
# affiner l'estimation argus (en fonction de l'année et du modèle plus précis)
# fiabiliser la collecte des data pour les quelques fiches qui ne collent pas au modèle (données non-présentes)


# Returns the soup content from the HTML content (corresponding to a given Url)
## //// Parameter : encoding should be 'utf-8', to convert the request result into this encoding format
def getSoupFromUrl(url, encoding):

    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        if encoding == 'utf-8':
        	result.encoding = 'utf-8'
        result_text = BeautifulSoup(result.text,"html.parser")
        #print result_text
        return result_text
    else:
        print 'Request failed', url
        return None

# Récupère les liens des résultats, à partir de l'url de la requête sur Le Bon Coin
def GetResultsLinks(request_url): 

    # récupère le soup de la page correspondant à la requête
    soup=getSoupFromUrl(request_url, None)
    #print soup

    #Récupère la partie qui contient le résultat des produits recherchés
    Balise = soup.find('div', attrs={"class":u"list-lbc"}).select('a')

    # récupère le lien associé à chaque résultat de la requête
    links = [balise.get('href') for balise in Balise] 

    # Print des résultats
    #print "il y a "+ str(len(links)) + " résultats à la requête"
    # for link in links:
    #     print (str(link)+"\n") 

    return links

def Getgeocode (postcode):
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+str(postcode)+'+France'

    request = requests.get(url);  
    json_data = json.loads(request.text);

    if json_data['status'] == u'OVER_QUERY_LIMIT':
        return ['NA(OVER_QUERY_LIMIT)','NA (OVER_QUERY_LIMIT)']
    else :
        longitude = json_data ['results'][0]['geometry']['location']['lng']
        latitude = json_data ['results'][0]['geometry']['location']['lat']

    return [longitude, latitude]


def GetResultdetails(result_url, Columns): 
    # récupère le soup de la page au résultat 
    soup=getSoupFromUrl(result_url, None) 

    # A FAIRE : Approfondir la différence entre le "Find" et le "Select" de Beautiful Soup

    #Récupère le titre de l'annonce (qui contient le nom du modèle)
    Title = soup.find('div', attrs={"class":u"header_adview"}).select('h2')[0].text
    #print Title
    isCAPTUR = checkCAPTUR(Title)

    #Récupère la partie qui contient le caractéristiques du produit
    Prix = soup.find('div', attrs={"class":u"lbcParams withborder"}).select('span')[0].text

#### Récupère la partie qui contient le résultat des produits recherchés
    # Marque
    Marque = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('td:nth-of-type(1)')[0].text
    
    # Version

    # getModelTitle = getModele(Title)
    # if getModelTitle==None:
    #     Modele = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('td:nth-of-type(2)')[0].text
    # else:
    #     Modele = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('td:nth-of-type(2)')[0].text+str(getModelTitle)

    th_balise = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('th')
    i = 1
    for th in th_balise :
        #print "i="+str(i)
        if th.text==u'Modèle :':
            Modele = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('th:nth-of-type('+str(i)+') + td')[0].text
        else:
            Modele = " "
        i=i+1


    # Année-modèle : Manip à factoriser avec une fonction
    th_balise = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('th')
    i = 1
    for th in th_balise :
        #print "i="+str(i)
        if th.text==u'Année-modèle :':
                Annee = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('th:nth-of-type('+str(i)+') + td')[0].text.strip()
        i=i+1

    # Kilométrage : Manip à factoriser avec une fonction
    th_balise = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('th')
    i = 1
    for th in th_balise :
        if th.text==u'Kilométrage :':
            Kilometrage = soup.find('div', attrs={"class":u"lbcParams criterias"}).select('th:nth-of-type('+str(i)+') + td')[0].text[:-3]
        else:
            Kilometrage=" "
        i=i+1

#### INFO ON THE SELLER
    Ville = soup.find('div', attrs={"class":u"floatLeft"}).select('td:nth-of-type(2)')[0].text
    Postcode = soup.find('div', attrs={"class":u"floatLeft"}).select('td:nth-of-type(3)')[0].text    

#### Prepare the output to insert in the table
    #### INFO ON THE CAR
    s = pd.Series(np.zeros(11), index=Columns)
    s['Titre']= Title
    
    if Prix[1:2]==" ":
        s['prix']=int(Prix[0:1]+Prix[2:5]) # to adress the situations with a price <10K€
    else:
        s['prix']=int(Prix[0:2]+Prix[3:6]) # on retire les "€"" // -> A FAIRE : VOIR SI ON PEUT TROUVER QQCHOSE DE PLUS ELEGANT
    
    s['Marque']=Marque
    
    s['version']= Modele
    if getModele(Title)==None:
        s['version identifiee']=False
    else:
        s['version identifiee']=True
    
    # Annee
    s['annee']=Annee

    # les KM
    s['km']= Kilometrage

    s['isCAPTUR']= isCAPTUR

    # Géographie Seller
    s['ville'] = Ville
    s['Code Postal'] = Postcode
    s['longitude']= Getgeocode(Postcode)[0]
    s['latitude']= Getgeocode(Postcode)[1]

    return s


def getModele(Title): # à rendre plus propre (en utilisant upper or lower)
    if (Title.upper().count("ZEN")>0):
        return ' Zen'
    elif (Title.upper().count("INTENS")>0):
        return ' Intens'
    elif (Title.upper().count("LIFE")>0):
        return ' Life'
    elif (Title.upper().count("BUSINESS")>0):
        return ' Business'
    elif (Title.upper().count("ARIZONA")>0):
        return ' Arizona'
    else:  
        return None

def checkCAPTUR(Title):
    if ('Captur'in Title) or ('captur'in Title) or ('CAPTUR'in Title): #TO DO : A faire plus proprement (avec .upper ?)
        return True
    else:  
        return 'cette voiture n_est pas une Captur'

#def getURLproprio(Title):
    # #Récupère le lien vers la page du propriétaire
    # BaliseProprio = soup.find('div', attrs={"class":u"upload_by"}).find('a')
    # LinkProprio = BaliseProprio.get('href') 

    # url_proprio = 'http://www2.leboncoin.fr/ar?ca=12_s&id=717377389'

# def GetProprioInfo(url_proprio):
#     # pas easy car le numéro apparait après exécution d'un code java script
#     soup=getSoupFromUrl(url_proprio, None)
#     Phone = soup.find('div', attrs={"class":u"lbc_links"}).find('span', attrs={"id":u"phoneNumber"})

#     javascript:getPhoneNumber("http://www2.leboncoin.fr", 717377389)

# def RunJS ():
#     #Exécuter le JavaScript pour récupérer le numéro de téléphone
#     driver = webdriver.Chrome #('/Macintosh HD/Applications/anaconda/chromedriver')
#     driver.get('http://www.google.com/xhtml');
#     time.sleep(5) # Let the user actually see something!
#     search_box = driver.find_element_by_name('q')
#     search_box.send_keys('ChromeDriver')
#     search_box.submit()
#     time.sleep(5) # Let the user actually see something!
#     driver.quit()

#     browser.visit('http://www2.leboncoin.fr/ar?ca=12_s&id=687453314')
#     button = browser.find_by_name('javascript:getPhoneNumber("http://www2.leboncoin.fr", 687453314)')
#     button.click()
#     browser.quit()

def getArgusCaptur(): # A FAIRE : faire le split par modèle plus précis et éventuellement 2013 / 2014
    url = 'http://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html'
    url_intens = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+intens+eco2-2013.html'
    url_life = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+life+eco2-2013.html'
    url_zen = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+zen+eco2-2013.html'
    url_arizona = 'http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+arizona+eco2-2013.html'
    url_business = 'http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+business+edc-2013.html'


    soup=getSoupFromUrl(url_intens, None)
    argus_intens= soup.find('div', attrs={"class":u"tx12"}).select('span')[0].text

    soup=getSoupFromUrl(url_life, None)
    argus_life= soup.find('div', attrs={"class":u"tx12"}).select('span')[0].text

    soup=getSoupFromUrl(url_zen, None)
    argus_zen= soup.find('div', attrs={"class":u"tx12"}).select('span')[0].text

    soup=getSoupFromUrl(url_business, None)
    argus_business= soup.find('div', attrs={"class":u"tx12"}).select('span')[0].text

    soup=getSoupFromUrl(url_arizona, None)
    argus_arizona= soup.find('div', attrs={"class":u"tx12"}).select('span')[0].text

    argus = pd.DataFrame(np.zeros((1,3)), columns = ['argus_Captur Zen', 'argus_Captur Intens', 'argus_Captur Life'])
    argus['argus_Captur Zen']= argus_zen
    argus['argus_Captur Intens']= argus_intens
    argus['argus_Captur Life']= argus_life
    argus['argus_Captur Arizona']= argus_arizona
    argus['argus_Captur Business']= argus_business

    output = argus
    print argus
    return output


def InitializeTable(Columns):
    outputData = np.array([np.zeros(1)]*11).T
    DATA = pd.DataFrame(outputData,columns = Columns)
    return DATA


def getCaptur(url, Columns):
    
    DATA = InitializeTable(Columns)

    links = GetResultsLinks(url)

    for link in links:
        OneResult = GetResultdetails(link, Columns)
        OneResult = pd.DataFrame(OneResult).T
        #print OneResult # to control the line to be insered in the DataFrame   
        DATA = DATA.append(OneResult)
        #print "une nouvelle valeur ajoutée à la table DATA"
    
    #clean DATA index (put values 0,1,2,...)
    #print 'Setting the index\n'
    idx=np.arange(DATA.shape[0])
    DATA=DATA.set_index(idx)

    #remove the first line (with index = 0, containing only zeros)
    DATA=DATA[DATA.index>=1]
    
    return DATA

def putArgusValue(DATA, argus):

    for index in DATA.index:
        if DATA['isCAPTUR'][index]==True:
            if ((DATA['version identifiee'][index]) == False):
                DATA['argus'][index] = None
            else:
                #print DATA['version'][index]
                column = 'argus_'+str(DATA['version'][index])
                if column in argus.columns:
                    ArgusValue = argus[column][0]
                    #print ArgusValue
                    DATA['argus'][index] = int(ArgusValue[0:2]+ArgusValue[3:6])
                    #print DATA['argus'][index]
    return DATA

def CompareWithArgus(DATA):

    for index in DATA.index:
        if (DATA['version'][index] != None):
            if ((DATA['prix']- DATA['argus'])[index]<0):
                DATA['comparaison argus'][index] = str((DATA['prix']- DATA['argus'])[index])+'-> Affaire à étudier'
            else:
                DATA['comparaison argus'][index] = str((DATA['prix']- DATA['argus'])[index])
        else:
            DATA['comparaison argus'][index] = None
    return DATA


def getCapturInRegion_pro_part(region, type, argus, page, Columns):
    url_part = 'http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+str(page)+'&q=Renault%20Captur&f=p'
    url_pro = 'http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+str(page)+'&q=Renault%20Captur&f=c'

    # select the url depending on the expected type of sellers (pro / part)
    if type=='part':
        url = url_part
    else:
        url=url_pro

    #print 'Starting getCaptur\n'
    DATA = getCaptur(url,Columns)

    # complete the Data with Region & pro/part information
    DATA['Region']=region
    DATA['pro/part']= type

    #print 'Start comparison with argus'
    putArgusValue(DATA, argus)
    CompareWithArgus(DATA)

    return DATA

def nbr_pages_par_recherche(Region,type):
    
    firstpagepro = 'http://www.leboncoin.fr/voitures/offres/'+Region+'/?o='+str(1)+'&q=Renault%20Captur&f='+type
    firstpagepart = 'http://www.leboncoin.fr/voitures/offres/'+Region+'/?o='+str(1)+'&q=Renault%20Captur&f='+type

    if type == 'p':
        firsturl = firstpagepart
    else:
        firsturl = firstpagepro

    soup=getSoupFromUrl(firsturl, None)
    balises_a = soup.find_all("a")
    
    numberOfPages= pd.Series([int(balise.text) for balise in balises_a if balise.text.isnumeric()])
    if len(numberOfPages)==0:
        return 1
    else:
        return numberOfPages.max()

def getCapturInRegion(region, argus, Columns):
    nb_pages_pro = nbr_pages_par_recherche(region,'c')
    nb_pages_part = nbr_pages_par_recherche(region,'p')
    
    DATA = InitializeTable(Columns)


    for page in range(1, nb_pages_part+1):
        print "part - page "+str(page)
        data = getCapturInRegion_pro_part(region,'part',argus,page, Columns)
        data = [DATA,data]
        DATA = pd.concat(data)
    
    for page in range(1, nb_pages_pro+1):
        print "pro - page "+str(page)
        data = getCapturInRegion_pro_part(region,'pro',argus,page, Columns)
        data = [DATA,data]
        DATA = pd.concat(data)

    #datas = [getCapturInRegion_pro_part(region,'pro',argus,nb_pages_pro),getCapturInRegion_pro_part(region,'part',argus,nb_pages_part)]
    return DATA

def main():
    
    Columns = ['Titre','isCAPTUR','pro/part', 'Marque', 'version', 'annee', 'km','prix','argus','comparaison argus', 'telephone']

    argus = getArgusCaptur()
    print "launch ile de france"
    DATA1 = getCapturInRegion('ile_de_france', argus, Columns)
    print "launch aquitaine"
    DATA2 = getCapturInRegion('aquitaine', argus, Columns)
    print "launch PACA"
    DATA3 = getCapturInRegion('provence_alpes_cote_d_azur', argus, Columns)
    
    #concat the results for the different regions
    datas = [DATA1,DATA2,DATA3]
    DATA = pd.concat(datas)

    print DATA

    Request_result = DATA[DATA['isCAPTUR']==True]

    #rebuild the index
    idx=np.arange(Request_result.shape[0])
    Request_result=Request_result.set_index(idx)
    Request_result=Request_result.drop('Marque',axis=1)
    Request_result=Request_result.drop('isCAPTUR',axis=1)
    Request_result=Request_result.drop('version identifiee',axis=1)

    columns = [u'Titre', u'version', u'annee', u'km', u'prix', u'argus', u'comparaison argus', u'pro/part', u'telephone', u'Region', 'Code Postal', 'latitude', 'longitude']
    Request_result = pd.DataFrame(Request_result, columns=columns)

    #print Request_result

    Request_result.to_csv('Captur.csv',encoding='utf-8')

    return Request_result


main()


