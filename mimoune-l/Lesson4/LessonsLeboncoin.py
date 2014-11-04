import numpy as np 
import pandas as pd 
from bs4 import BeautifulSoup
import requests
import re
import json
import unicodedata as uni



#url = 'http://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&q=renault%20captur&f=c'


def urlT(NumeroPage, region):
    return  'http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+str(NumeroPage)+'&q=renault%20captur&f=c'
    
# avec index on peut parcourir toutes les pages qui nous interesse en principe il faut une fonction qui nous permet de le calculer

def getSoupFromUrl(site):
    
    result = requests.get(site)
    if result.status_code == 200:
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', urlT(NumeroPage,region)
        return None
        
        
def TrouvezLesLiesnUrl(site):
    soup = getSoupFromUrl(site)
    LienUrl =soup.find(class_="list-lbc").find_all('a')
    return [Lien.get('href') for Lien in LienUrl]


def MettreLesSoupEnList(List_Url):
    ListDesSoup = []
    for i in  range(len(List_Url)):
       ListDesSoup.append(getSoupFromUrl(List_Url[i]))
    return ListDesSoup

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')

def TelephoneVendeur(ApartirText):
     infDiv=[normalize(bInfDiv.text).strip() for bInfDiv in ApartirText] 
     words=infDiv.split("\n")
     numtel=''
     for w in words :
            if re.match(r'(^(.)*(?P<tel>(0[0-9]([ .-]?[0-9]{2}){4})))',w):
              numtel=re.sub(r'(^(.)*(?P<tel>(0[0-9]([ .-]?[0-9]{2}){4}))(.)*)',r'\g<tel>',w)
              return numtel

def ArgusDesVoitures(marque, model) :

	url = 'http://www.lacentrale.fr/cote-voitures-renault-captur--2013-.html'
	soup = getSoupFromUrl(url)
	# Obtention des liens vers les différents modèle
	tdContainers = soup.find_all('td', class_="tdSD QuotMarque")
	balisesA = [ td.select('a')[0] for td in tdContainers ]
	links = ['http://www.lacentrale.fr/' + link.get("href") for link in balisesA]
	models =  [link.text for link in balisesA]

	# Pour chaque lien on récupère le nom du modèle et son prix
	argus = {}
	for i in range(0, len(links)) :
		soupCurrentModel = getSoupFromUrl(links[i])
		currentArgus = int( re.sub('\D{1}', '', soupCurrentModel.find('span', class_="Result_Cote").text) )
		argus[ models[i] ] = currentArgus

	return argus  
 
#_Leprix = ListSoup[0].find(class_="price").select('span')[0].text
#Leprix = int( re.sub('[^0-9]*', '', _Leprix) )
#Ville = ListSoup[0].find(class_="floatLeft").select('tr  + tr td')[0].text
#CodePostale = ListSoup[0].find(class_="floatLeft").select('tr  + tr + tr td')[0].text
#TelephoneDeVendeur_Brut = ListSoup[0].find(class_= "content")
#_Model_annee = ListSoup[0].find(class_="lbcParams criterias").select('tr + tr + tr td')[0].text
# Model_annee = int( _Model_annee)
# _Kilometrage = ListSoup[0].find(class_="lbcParams criterias").select('tr + tr + tr + tr td')[0].text
# Kilometrage = int( re.sub('[^0-9]*', '',  _Kilometrage ) )
#_CodePostale = ListSoup[0].find(class_="floatLeft").select('tr  + tr + tr td')[0].text
#TelephoneDeVendeur_N = TelephoneVendeur(TelephoneDeVendeur_Brut)



def Data_Frame():
    colonnes = ['le prix','model annee','Kilometrage','ville','code postale','Telephone','Type vendeur','Latitude', 'Longitude']
    FormatInfo = pd.DataFrame(columns = colonnes)
    return FormatInfo

def ChercherLesDonnees(ListSoup,index):
    ListDesDonnees =[]
    _Leprix = ListSoup[index].find(class_="price").select('span')[0].text
    Leprix = int( re.sub('[^0-9]*', '', _Leprix ) )
    _Model_annee = ListSoup[index].find(class_="lbcParams criterias").select('tr + tr + tr td')[0].text
    Model_annee = int(_Model_annee )
    _Kilometrage = ListSoup[index].find(class_="lbcParams criterias").select('tr + tr + tr + tr td')[0].text
    _Ville = ListSoup[index].find(class_="floatLeft").select('tr + tr td')[0].text
    Ville = str(_Ville)
    Kilometrage = int( re.sub('[^0-9]*', '',  _Kilometrage ) )
    _CodePostale = ListSoup[index].find(class_="floatLeft").select('tr  + tr + tr td')[0].text
    CodePostale = int(_CodePostale)
    
    ListDesDonnees.append(Leprix)
    ListDesDonnees.append(Model_annee )
    ListDesDonnees.append(Kilometrage)
    ListDesDonnees.append(Ville)
    ListDesDonnees.append(CodePostale)
    
    return ListDesDonnees

def RecuperationDesDonnees(NumeroPage, region):
    
    for index in range(NumeroPage):
        for region in ['ile_de_france', 'aquitaine', 'provence_alpes_cote_d_azur']:
            ListeComplete =  ChercherLesDonnees(NumeroPage,region )
        return ListeComplete 

listcomplete = RecuperationDesDonnees(3)
EssaiDonnees = ChercherLesDonnees()

def main():
#je test pour un cas simple
    NumeroPage=1
    region= 'ile_de_france'
    site = urlT(NumeroPage, region)
    List_Des_Liens = TrouvezLesLiesnUrl(site)
    List_Des_Soup =  MettreLesSoupEnList(List_Des_Liens)
    List_Des_Donnees = ChercherLesDonnees(List_Des_Soup,NumeroPage)
    dataFrameRecord = pd.DataFrame(List_Des_Donnees, columns=['le prix','model annee','Kilometrage','ville','code postale','Telephone','Type vendeur','Latitude', 'Longitude'])
    doDataFrame = doDataFrame.append(dataFrameRecord)
    doDataFrame.to_csv('Renault.csv')
    
#mettre les donnees do dans un fichier


if __name__ == "__main__":
    main()
 

