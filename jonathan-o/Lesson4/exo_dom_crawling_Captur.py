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
import numpy as np
import pandas as pd


################################################################################################
# Some String manipulation functions

def normalize(string):
    return uni.normalize('NFKD',string).encode('ascii','ignore')

#################################################################################################
#                                                                                               #
"""                                             Clean CSV lebon                               """
#                                                                                               #
################################################################################################# 

def cleandata(df):
    clean_df = df
    clean_df = clean_df.fillna(value=0, axis=0)
    for i in range(0,df.shape[0]):
        if (clean_df.ix[i]['Number'] !=0):
            clean_df.loc[i,'Number'] = str(0) + str(int(df.ix[i]['Number']))
        if clean_df.ix[i]['Manufacturer'] == 0:
            if clean_df.ix[i]['Model'] == 0:
                if len(clean_df.ix[i]['Type'].split(' '))>1:
                    clean_df.loc[i,'Manufacturer'] = 'Renault'
                    clean_df.loc[i,'Model'] = 'Captur'
    clean_df = clean_df[clean_df.Manufacturer == 'Renault']
    clean_df = clean_df[clean_df.Model == 'Captur']

    return clean_df

def cleandata2(df):
    clean_df = df
    column = clean_df.apply(lambda x : x['Manufacturer'] +' '+ x['Model']+' ' + x['Type'],axis =1)
    clean_df = clean_df.drop(['Manufacturer','Model','Type'],axis = 1)
    clean_df['Model'] = Series(np.array(column),index=clean_df.index)

    final_df = clean_df[['Model','Year','KM','Sell_Price','IsaPro?','Number','Mean_Price','Exceed_Mean_Price','City']]
    return final_df

#################################################################################################
#                                                                                               #
"""                                             Add Mean value                                """
#                                                                                               #
################################################################################################# 

def addcolumn(datalebon,dataargus):
    new_df = datalebon
    columns = new_df.apply(lambda x : pd.Series(MeanFromType(x['Type'],dataargus)), axis =1)
    new_df = new_df.drop(['Type'],axis=1)
    new_df[['Mean_Price','Type']] = columns
    column2 = new_df.apply(lambda x : pd.Series(x['Sell_Price'] > x['Mean_Price']), axis =1)
    new_df[['Exceed_Mean_Price']] = column2


    return new_df

def MeanFromType(Type,dataargus):
    splits = Type.split(' ')
    istrue = {}
    df = []
    real_type =[]
    for true_type in dataargus['Type']:
        istrue[true_type] = True
        for item in splits:
            if item not in true_type:
                istrue[true_type] = False
    for true_type in dataargus['Type']:
        if istrue[true_type]:
            df.append(dataargus.ix[true_type]['value'])
            real_type.append(true_type)
    final_type = Type
    if len(real_type) ==1:
        final_type = real_type[0]
    if len(df)!=0:
        return [np.mean(df),final_type]
    newType = Type.replace(' '+splits[-1],'')
    
    return MeanFromType(newType,dataargus)




#################################################################################################
#                                                                                               #
"""                                            Add google API                                 """
#                                                                                               #
################################################################################################# 

##############################################################################################
# getcoordAPI

def getcoordAPI(city):
    link = ('https://maps.googleapis.com/maps/api/geocode/json?address='+ city +'&key=AIzaSyBmrH7Fg_LC5mWNP3bLlAddXbt255CxfSc')
    r = requests.get(link)
    if(r.ok):
        repoItem = json.loads(r.text)
        lat = repoItem['results'][0]['geometry']['location']['lat']
        lng = repoItem['results'][0]['geometry']['location']['lng']
    coordinate = [str(lat),str(lng)]
    return coordinate

def addcoordinate(datalebon):
    new_df = datalebon
    column = new_df['City'].apply(lambda city : pd.Series(getcoordAPI(str(city))),convert_dtype=True)
    print column
    new_df = new_df.drop(['City'],axis = 1)
    new_df[['lat','long']] = column
    return new_df



#################################################################################################
#                                                                                               #
"""                                             Work on CSV                                   """
#                                                                                               #
################################################################################################# 

##############################################################################################
# Main Code

# get the csv from the two other python code
dataleboncoin = DataFrame.from_csv('leboncoin.csv')
dataArgus = DataFrame.from_csv('Argus.csv')
dataArgus = dataArgus.set_index(dataArgus['Type'])

#first cleaner
dataleboncoin_clean =cleandata(dataleboncoin)
#add the missing columns
dataleboncoin_clean = addcolumn(dataleboncoin_clean,dataArgus)
#second cleaner
dataleboncoin_clean = cleandata2(dataleboncoin_clean)
#replace coordinate
finaldatalebon = addcoordinate(dataleboncoin_clean)
#convert to csv
finaldatalebon.to_csv('Final.csv')   

