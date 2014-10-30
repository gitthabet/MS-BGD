# -*- coding: utf-8 -*-

"""

Created on Thu Oct 30 2014
    
@author: Ohayon

"""

import requests
import html5lib
import unicodedata as uni
from bs4 import BeautifulSoup
import json
import re
from pandas import Series, DataFrame

##############################################################################################
# Some String manipulation functions

def between(myString, start, stop):
  beg = myString.index(start) + len(start)
  end = myString.index(stop, beg)
  return myString[beg:end]


def before(myString,Symbol):
    end = myString.index(Symbol)
    return myString[0:end]  

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')


##############################################################################################
# Returns a soup object from a given url

def getSoupFromUrl(url):
    result = requests.get(url)
    
    if result.status_code == 200:
        return BeautifulSoup(result.text,"html5lib")
    
    else:
        print 'Request failed', url
        return None

#################################################################################################
#                                                                                               #
"""                                         leboncoin                                         """
#                                                                                               #
#################################################################################################

##############################################################################################
# getleboncoinlinks return the links from a search in a given region

def getleboncoinlinks(region,search):
    soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/'+region+'/?f=a&th=1&q='+ search)
    balises_a = soup.select('div div div div div div a')
    links = [balise.get('href') for balise in balises_a]
    
    cleaner = re.compile('((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)'+\
                            '(?:leboncoin\\.fr\\/voitures\\/)(\\d+)(?:[^\\s"]*))' )
    
    clean_links =[]
    for link in links:
        clean_link = cleaner.search(str(link)) 
        if clean_link:
            clean_links.append(clean_link.group(1))
    
    return clean_links

##############################################################################################
# getinfoonsell return the information on the car (price and km and seller) from a link

def getinfoonsell(link):
    soup = getSoupFromUrl(link)
    
    #find the info on the sell
    balises_info = soup.select('tr th + td')
    
    sell_info = [normalize(balise.text).strip() for balise in balises_info]

    #find the info on the seller
    balise_user = soup.find_all('div', 'upload_by')[0]
    user_balise = normalize(balise_user.text).split('\n')
    
    user_info =[]
    for info in user_balise:
        if info.strip() != '':
            user_info.append(info.strip())

    if 'PRO VEHICULES' in user_info[0].upper():
        clean_user_info = []
        clean_user_info.append(user_info[1])
        clean_user_info.append('Pro')
    else :
        clean_user_info = []
        clean_user_info.append(user_info[0])
        clean_user_info.append('')

    clean_sell_info = []
    if 'RENAULT' in [info.upper() for info in sell_info]:
        if 'ZOE' in [info.upper() for info in sell_info]:
            clean_sell_info.append(sell_info[0])
            clean_sell_info.append(sell_info[5])
            clean_sell_info.append(sell_info[6])

    #find number img address 
    #balise_number = soup.select('span div div + img')
    #print balise_number
    return clean_sell_info,clean_user_info

##############################################################################################
# Create DataFrame Style.

def getdataonsell(regions):
    dataframe=[]
    for region in regions:
        links = getleboncoinlinks(region,'zoe+renault')
        for link in links:
            sell_info,user_info = getinfoonsell(link)
            if len(sell_info) == 3:

                    dataframe.append(user_info + sell_info)
    return dataframe

#################################################################################################
#                                                                                               #
"""                                             ARGUS                                         """
#                                                                                               #
################################################################################################# 

##############################################################################################
# GetArgus 

def getArgus():
    soup = getSoupFromUrl('http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html')
    # find the info on cars
    balises_td = soup.find_all('td', class_="tdSD QuotMarque")
    List_of_car = [normalize(balise.select('a')[0].text) for balise in balises_td]
    Url_of_car = [normalize(balise.select('a')[0].get('href')) for balise in balises_td]
    
    Argus_dico = {}
    for i in range(0,len(List_of_car)):
        Argus_dico[List_of_car[i]] = getValue(Url_of_car[i])
    return Argus_dico

##############################################################################################
# getValue

def getValue(part_URL):
    soup = getSoupFromUrl('http://www.lacentrale.fr/' + part_URL)
    balises_td = soup.find_all('span', class_="Result_Cote")
    return int(normalize(balises_td[0].text).replace(' ',''))



#################################################################################################
#                                                                                               #
"""                                             Main C                                        """
#                                                                                               #
################################################################################################# 


##############################################################################################
# Main Code

#Region = raw_input("enter your region here: ")
Regions = ['provence_alpes_cote_d_azur','ile_de_france','aquitaine']
#Search = raw_input("enter your search here: ")
Search = 'zoe+renault'


#dataframe = getdataonsell(Regions)
#df=DataFrame(dataframe,columns = ['User_Name','IsaPro?','Sell_Price','Year','KM'])
#print df

dico = getArgus()
print dico