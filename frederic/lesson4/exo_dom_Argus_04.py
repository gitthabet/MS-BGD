import requests
import unicodedata as uni
from bs4 import BeautifulSoup
import json
import re
#from pandas import Series, DataFrame

################################################################################################
# Some String manipulation functions

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')


################################################################################################
# Returns a soup object from a given url

def getSoupFromUrl(url):
    result = requests.get(url)
    
    if result.status_code == 200:
        return BeautifulSoup(result.text)
    
    else:
        print 'Request failed', url
        return None

#################################################################################################
#                                                                                               #
"""                                             ARGUS                                         """
#                                                                                               #
################################################################################################# 

##############################################################################################
# GetArgus 

def getArgus():
    soup = getSoupFromUrl('http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html')
    # 
    balises_td = soup.find_all('td', class_="tdSD QuotMarque")
    ListCars = [normalize(balise.select('a')[0].text) for balise in balises_td]

    ListPrix=[]
#    balises_a=soup.select('a')
#    balises_a=soup.find_all('a',text-decoration="underline")

    balises_a = [balise.select('a') for balise in balises_td]

    links = [balise[0].get('href').encode('ascii','replace') for balise in balises_a]
    link=[]
    for link in links:    
    # 
#    balises_td = soup.find_all('td', class_="tdSD QuotMarque")
#        print 'link' , link
        if link is not None:
            if re.match(r'^(.)*(cote-auto-renault-captur)(.)*',link):
                soup2=getSoupFromUrl('http://www.lacentrale.fr/'+link)
                balise_prix=soup2.find_all('span',class_="Result_Cote")
                prix=int(normalize(balise_prix[0].text).replace(' ',''))
                ListPrix.append(prix)
    

     
    Argus = {}
    for i in range(0,len(ListCars)):
#        Argus.append([ListCars[i] ,ListPrix[i]])
         Argus[ListCars[i]]= ListPrix[i]  
    print Argus
#    return Argus

##############################################################################################
# getValue

def getValue(part_URL):
    soup = getSoupFromUrl('http://www.lacentrale.fr/' + part_URL)
    balises_td = soup.find_all('span', class_="Result_Cote")
    return int(normalize(balises_td[0].text).replace(' ',''))

#createCSV for Argus
Argusdata = getArgus()
dataframeArgus = DataFrame(Argusdata,columns = ['Type','value'])
dataframeArgus.to_csv('Argus.csv')

