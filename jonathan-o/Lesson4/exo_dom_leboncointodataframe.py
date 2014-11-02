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

################################################################################################
# Some String manipulation functions

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')


################################################################################################
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
# Create DataFrame Style.

def getdataonsell(regions,search):
    dataframe=[]
    for region in regions:
        # for each region, go fetch the links
        links = getleboncoinlinks(region,search)
        for link in links:
            #for each link, go fetch all info from soup
            soup = getSoupFromUrl(link)
            sell_info = getinfoonsell(soup)
            user_info = getinfoonuser(soup)
            number,type_of_car = getinfofromdesc(soup,sell_info[5])
            dataframe.append(user_info + number + sell_info[0:5] + type_of_car + [sell_info[6]])
    return dataframe


##############################################################################################
# getleboncoinlinks return the links from a search in a given region

def getleboncoinlinks(region,search):
    soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/'+region+'/?q='+ search)
    # find the number of pages from the soup
    pages = getnumberofsales(soup)
    links=[]
    for i in range(0,pages):
        soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/'+region+'/?o='+ str(i+1) + '&q='+ search)
        balises_td = soup.find_all('div', class_="list-lbc")
        balises_a = balises_td[0].find_all('a')
        links += [balise.get('href') for balise in balises_a]
    
    return links

##############################################################################################
# getnumberofsales return the number of pages form the soup

def getnumberofsales(soup):
    balises_num = normalize(soup.select('ul li span + span')[0].text)
    cleaner_num = re.compile('((\\d+))')
    num_sell = int(cleaner_num.findall(balises_num)[2][0])
    num_pages = num_sell/35 + 1
    return num_pages



##############################################################################################
# getinfoonsell return the information on the car from soup

def getinfoonsell(soup):
    #find the info on the sell
    balises_info = soup.select('tr th + td')
    sell_info = [normalize(balise.parent.text).replace('\n','').replace('\t','').replace(' ','') for balise in balises_info]
    # create a dictionnary from the header info of sale
    dico_sell_info = {}
    for i in range(0,len(sell_info)):
        split = sell_info[i].split(':')
        dico_sell_info[split[0]] = split[1]

    # parse the dictionnary to fill a formated list of info
    clean_sell_info = []
    if 'Marque' in dico_sell_info:
        clean_sell_info.append(dico_sell_info['Marque'])
    else:
        clean_sell_info.append('')
    if 'Modele' in dico_sell_info:
        clean_sell_info.append(dico_sell_info['Modele'])
    else:
        clean_sell_info.append('')
    if 'Prix' in dico_sell_info:
        clean_sell_info.append(re.sub(r'\D','',dico_sell_info['Prix']))
    else:
        clean_sell_info.append('')
    if 'Annee-modele' in dico_sell_info:
        clean_sell_info.append(re.sub(r'\D','',dico_sell_info['Annee-modele']))
    else:
        clean_sell_info.append('')
    if 'Kilometrage' in dico_sell_info:
        clean_sell_info.append(re.sub(r'\D','',dico_sell_info['Kilometrage']))
    else:
        clean_sell_info.append('')
    if 'Carburant' in dico_sell_info:
        clean_sell_info.append(dico_sell_info['Carburant'])
    else:
        clean_sell_info.append('')

    # create a format of style 'City,+Codepostal,+France to feed in the googleAPI later on
    if 'Ville' in dico_sell_info:
        tmp = dico_sell_info['Ville'] + ',+'
    else:
        tmp =''
    if 'Codepostal' in dico_sell_info:
        tmp = tmp + dico_sell_info['Codepostal'] +',+'
    else:
        tmp = tmp + ''
    clean_sell_info.append(tmp+ 'France')


    return clean_sell_info

##############################################################################################
# getinfoonuser return the information on the seller from soup

def getinfoonuser(soup):
    #find the info on the seller
    balise_user = soup.find_all('div', 'upload_by')[0]
    user_balise = normalize(balise_user.text).split('\n')

    user_info =[]
    for info in user_balise:
        if info.strip() != '':
            user_info.append(info.strip())

    #Determine the type of seller from header info
    if 'PRO VEHICULES' in user_info[0].upper():
        clean_user_info = []
        clean_user_info.append(user_info[1])
        clean_user_info.append('Pro')
    else :
        clean_user_info = []
        clean_user_info.append(user_info[0])
        clean_user_info.append('')

    return clean_user_info

##############################################################################################
# getinfofromdesc find desc of product + title 

def getinfofromdesc(soup,fuel):
    
    #find Description
    balise_desc = soup.find_all('div', class_="content")
    desc = normalize(balise_desc[0].text)

    #find Title
    balise_title = soup.find_all('h2', id="ad_subject")
    title = normalize(balise_title[0].text)
    
    #add title to desc
    desc = title + '\n' + desc
    
    #call find type of car
    type_of_car = [findcartypeindesc(desc,fuel)]
    #call find Number
    number = [findnumberindesc(desc)]

    return number,type_of_car


##############################################################################################
# findcartypeindesc determine from desc and title the type of the car

def findcartypeindesc(desc,fuel):

    list_of_type = ['ARIZONA','INTENS','ZEN','BUSINESS','LIFE']

    comp90 = re.compile('((90)(\D{1})(CH))')
    comp120 = re.compile('((120)(\D{1})(CH))')

    find_car = ''
    
    # divide in two type Diesel and Essence and find the model and additionnal info
    if 'DIESEL' in fuel.upper():
        if 'ENERGY' in desc.upper():
            find_car=' ECO2'
        for item in list_of_type:
            if item in desc.upper():
                find_car = ' ' + item + find_car 
                break
        if 'EDC' in desc.upper():
            find_car = find_car + ' EDC'
        find_car = 'DIESEL' + find_car

    if 'ESSENCE' in fuel.upper():
        if 'ENERGY' in desc.upper():
            find_car = ' ECO2'
        for item in list_of_type:
            if item in desc.upper():
                find_car = ' ' + item + find_car 
                break
        if 'EDC' in desc.upper():
            find_car = find_car + ' EDC'
        find_car = 'ESSENCE' + find_car

    return find_car

##############################################################################################
# findnumberindesc search for number in desc and title

def findnumberindesc(desc):
    search_number = re.compile('((\D{1}0\d{9}\D{1})|(\D{1}0\d{1})(\W{1})(\d{2})(\W{1})(\d{2})(\W{1})(\d{2})(\W{1})(\d{2}\D{1}))')
    num=search_number.search(desc)
    print num
    if num:
        clean_num = re.sub(r'\D','',num.group(1))
        return clean_num
    return ''



#################################################################################################
#                                                                                               #
"""                                         Create CSV                                        """
#                                                                                               #
#################################################################################################

#Region = raw_input("enter your region here: ")
Regions = ['provence_alpes_cote_d_azur','ile_de_france','aquitaine']
#Search = raw_input("enter your search here: ")
Search = 'captur+renault'

dataframe = getdataonsell(Regions,Search)

df=DataFrame(dataframe,columns = ['User_Name','IsaPro?','Number','Manufacturer','Model','Sell_Price','Year','KM','Type','City'])

df.to_csv('leboncoin.csv')    
