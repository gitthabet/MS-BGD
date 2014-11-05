__author__ = 'MP'

import requests
import re
import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


""""""""""""""""""""""""""""""""""""""""""
""" Class to use utils functions """
""""""""""""""""""""""""""""""""""""""""""
class Util:

    # returns a soup object from a given url
    @staticmethod
    def getSoupFromUrl(url):
        result = requests.get(url)
        if result.status_code == 200:
            return BeautifulSoup(result.text, "html5lib")
        else:
            print 'Request failed', url
        return None

    # for a given request, get the number of pages of results
    @staticmethod
    def getNumberPages(url):
        soupUrl = Util.getSoupFromUrl(url)
        nbAds = soupUrl.select('span b')[0].contents[0]
        return int(np.ceil(int(nbAds) / 100.0))

    # create a list of urls refers to the ads
    @staticmethod
    def createAdsUrls(url):
        urlSoup = Util.getSoupFromUrl(url)
        a_balises = urlSoup.find(class_ = "list-lbc").find_all('a')
        return [balise.get('href') for balise in a_balises]


""""""""""""""""""""""""""""""""""""""""""
""" Class to use LeBonCoin crawler """
""""""""""""""""""""""""""""""""""""""""""
class LbcCrawler:

    @staticmethod
    def getVersion(words):
        param = {'Cylindre': "" ,
                 'OilType1': "" ,
                 'Digits': "",
                 'Name1': "",
                 'Name2': "",
                 'Name3': "",
                 'Name4': "",
                 'Name5': "",
                 'OilType2': ""}
        version =""
        if words.count('0.9')>0 :
            param['Cylindre'] = '0.9'
        if words.count('1.2')>0 :
            param['Cylindre'] = '1.2'
        if words.count('1.5')>0 :
            param['Cylindre'] = '1.5'
        if words.count('tce')>0 :
            param['OilType1'] = 'TCE'
        if words.count('dci')>0 :
            param['OilType1'] = 'DCI'
        if words.count('90')>0 :
            param['Digits'] = '90'
        if words.count('120')>0 :
            param['Digits'] = '120'
        if words.count('energy')>0 :
            param['Name1'] = 'ENERGY'
        if words.count('s&s')>0 :
            param['Name2'] = 'S&S'
        if words.count('arizona')>0 :
            param['Name3'] = 'ARIZONA'
        if words.count('intens')>0 :
            param['Name3'] = 'INTENS'
        if words.count('life')>0 :
            param['Name3'] = 'LIFE'
        if words.count('zen')>0 :
            param['Name3'] = 'ZEN'
        if words.count('business')>0 :
            param['Name3'] = 'BUSINESS'
        if words.count('edc')>0 :
            param['Name4'] = 'EDC'
        if words.count('ec02')>0 :
            param['Name5'] = 'EC02'
        if words.count('essence')>0 :
            param['OilType2'] = 'Essence'
        if words.count('diesel')>0 :
            param['OilType2'] = 'Diesel'
        # 0.9 TCE 90 ENERGY ARIZONA ECO2
        if param['Cylindre'] == '0.9' and  param['Name1'] == 'ENERGY' and param['Name3'] == 'ARIZONA' and param['Name5'] == 'EC02':
            return "0.9 TCE 90 ENERGY ARIZONA ECO2"
        if (param['Cylindre'] == '0.9' or (param['OilType1'] == 'TCE' and param['Digits'] == '90')) and param['Name3'] == 'ARIZONA' :
            return "0.9 TCE 90 ENERGY ARIZONA ECO2"
        # 1.2 TCE 120 ARIZONA EDC Essence
        if (param['Cylindre'] == '1.2' or param['Digits'] == '120') and param['Name3'] == 'ARIZONA' and param['Name4'] == 'EDC' :
            return "1.2 TCE 120 ARIZONA EDC Essence"
        if (param['Cylindre'] == '1.2' or param['Digits'] == '120') and param['Name3'] == 'ARIZONA' :
            return "1.2 TCE 120 ARIZONA EDC Essence"
        # 1.5 DCI 90 ENERGY ARIZONA ECO2
        if (param['Cylindre'] == '1.5' or param['OilType1'] == 'DCI') and param['Name1'] == 'ENERGY' and param['Name3'] == 'ARIZONA' and param['Name5'] == 'EC02':
            return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
        if (param['Cylindre'] == '1.5' or param['OilType1'] == 'DCI') and param['Name1'] == 'ENERGY' and param['Name3'] == 'ARIZONA' :
            return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
        # 1.5 DCI 90 ARIZONA EDC ECO2 Diesel
        if (param['Cylindre'] == '1.5' or param['OilType1'] == 'DCI') and param['Name3'] == 'ARIZONA' and param['Name4'] == 'EDC' and param['Name5'] == 'EC02':
            return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
        if (param['Cylindre'] == '1.5' or param['OilType1'] == 'DCI') and param['Name3'] == 'ARIZONA' and param['Name4'] == 'EDC':
            return "1.5 DCI 90 ARIZONA EDC ECO2 Diesel"
        # 0.9 TCE 90 ENERGY S&S INTENS ECO2
        if (param['Cylindre'] == '0.9' or param['Digits'] == '90') and param['Name3'] == 'INTENS' and (param['Name5'] == 'EC02' or param['Name2'] == 'S&S'):
            return "0.9 TCE 90 ENERGY S&S INTENS ECO2"
        if (param['Cylindre'] == '0.9' or param['Digits'] == '90') and param['Name3'] == 'INTENS':
            return "0.9 TCE 90 ENERGY S&S INTENS ECO2"
        # 1.2 TCE 120 INTENS EDC Essence
        if (param['Cylindre'] == '1.2' or param['Digits'] == '120') and param['Name3'] == 'INTENS' and param['Name4'] == 'EDC' :
            return "1.2 TCE 120 INTENS EDC Essence"
        if (param['Cylindre'] == '1.2' or param['Digits'] == '120') and param['Name3'] == 'INTENS':
            return "1.2 TCE 120 INTENS EDC Essence"
        # 0.9 TCE 90 ENERGY S&S LIFE ECO2
        if param['Name3'] == 'LIFE':
            return "0.9 TCE 90 ENERGY S&S LIFE ECO2"
        # "0.9 TCE 90 ENERGY S&S ZEN ECO2
        if (param['Cylindre'] == '0.9' or param['Digits'] == '90') and param['Name3'] == 'ZEN' and param['Name5'] == 'EC02' :
            return "0.9 TCE 90 ENERGY S&S ZEN ECO2"
        if (param['Cylindre'] == '0.9' or param['Digits'] == '90') and param['Name3'] == 'ZEN':
            return "0.9 TCE 90 ENERGY S&S ZEN ECO2"
        # "1.2 TCE 120 ZEN EDC Essence"
        if (param['Cylindre'] == '1.2' or param['Digits'] == '120') and param['Name3'] == 'ZEN' and param['Name4'] == 'EDC' :
            return "1.2 TCE 120 ZEN EDC Essence"
        if (param['Cylindre'] == '1.2' or param['Digits'] == '120') and param['Name3'] == 'ZEN':
            return "1.2 TCE 120 ZEN EDC Essence"
        # 1.5 DCI 90 BUSINESS EDC Diesel
        if param['Name3'] == 'BUSINESS' :
            return "1.5 DCI 90 BUSINESS EDC Diesel"
        return version



""""""""""""""""""""""""""""""""""""""""""
""" Class with data frame function """
""""""""""""""""""""""""""""""""""""""""""
class DataFrame:

    columnsNames = ['region','version','year','km','price','argus','cost','phone','vendor label','latitude', 'longitude','URL']

    # we create the data frame
    def createDfAdsCars(self):
        dfAdsCars = pd.DataFrame(columns=self.columnsNames)
        return dfAdsCars

    #Get all the required data from the ads
    def getAdsData(self, adsUrl):

        # get values
        adsUrlSoup = Util.getSoupFromUrl(adsUrl)
        adsTitle = adsUrlSoup.title.string
        price = int(re.sub(r'\D', "", adsUrlSoup.find(class_ = "price").select('span')[0].string))
        year = re.sub(r'\D', "", adsUrlSoup.find(class_ = "lbcParams criterias").select('tr + tr + tr td')[0].string)
        try:
            km = int(re.sub(r'\D', "", adsUrlSoup.find(class_="lbcParams criterias").select('tr + tr + tr + tr td')[0].string))
        except ValueError:
            km = float('nan')
        zipCode = int(re.sub(r'\D', "", adsUrlSoup.find(class_="floatLeft").select('tr + tr + tr td')[0].string))

        # Google API
        gpsCoordinates = GoogleAPI.getGPSCoord(zipCode)
        # get latitude
        latitude = gpsCoordinates.split(',')[0]
        # get longitude
        longitude = gpsCoordinates.split(',')[1]

        textAdsTags = adsUrlSoup.find(class_ = "content").contents
        # get the phone numbers
        phoneNumbers=""
        phoneNumbersList=[]

        for adsTag in textAdsTags:
            # regex define the phone number pattern
            phoneNumberRegex = r'([0]\d{1}[-\.\s]*\d{2}[-\.\s]*\d{2}[-\.\s]*\d{2}[-\.\s]*\d{2})'
            phoneNumberPattern = re.compile(phoneNumberRegex)
            phoneNumbersTags = list(set(phoneNumberPattern.findall(unicode(adsTag.string))))

            if phoneNumbersTags:
                phoneNumbersList = phoneNumbersList + phoneNumbersTags

        for phoneNumber in list(set(phoneNumbersList)):
                phoneNumbers = phoneNumbers + re.sub(r'\D',"", unicode(phoneNumber)).strip() + " | "
        phoneNumbers = phoneNumbers[:-2]

        # if we haven't found phone numbers
        if phoneNumbers == "":
            phoneNumbers = 'nc'

        carDesc = adsTitle
        for tag in textAdsTags:
            carDesc = carDesc + " " + unicode(tag.string)
        desc = carDesc.lower()

        version = LbcCrawler.getVersion(desc)

        # get argus
        centralUrl = "nc"
        def setCentralUrl(url):
            centralUrl = url
        version = {
         '0.9 TCE 90 ENERGY ARIZONA ECO2' :  setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+arizona+eco2-2013.html'),
         '1.2 TCE 120 ARIZONA EDC Essence' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+arizona+edc-2013.html'),
         '1.5 DCI 90 ENERGY ARIZONA ECO2' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+energy+arizona+eco2-2013.html'),
         '1.5 DCI 90 ARIZONA EDC ECO2 Diesel' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+arizona+edc+eco2-2013.html'),
         '0.9 TCE 90 ENERGY S&S INTENS ECO2' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+intens+eco2-2013.html'),
         '1.2 TCE 120 INTENS EDC Essence' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+intens+edc-2013.html'),
         '0.9 TCE 90 ENERGY S&S LIFE ECO2' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+life+eco2-2013.html'),
         '0.9 TCE 90 ENERGY S&S ZEN ECO2' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-0.9+tce+90+energy+s%5Es+zen+eco2-2013.html'),
         '1.2 TCE 120 ZEN EDC Essence' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-1.2+tce+120+zen+edc-2013.html'),
         '1.5 DCI 90 BUSINESS EDC Diesel' : setCentralUrl('http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+business+edc-2013.html')
        }

        if centralUrl== "nc":
            argus = float('nan')
        else :
            centralUrlSoup = Util.getSoupFromUrl(centralUrl)
            argus = int(re.sub(r'\D',"", centralUrlSoup.find(class_ = "Result_Cote arial tx20").string))
            if year == '2014':
                argus = argus * 1.06 # coeff

        # compare price
        cost = ''
        if argus > price:
            cost = 'less expensive'
        elif argus == price:
            cost = 'equals'
        elif argus < price:
            cost = 'more expensive'

        valuesList = [('',version, year, km, price, argus, cost, phoneNumbers, '', latitude, longitude, adsUrl)]

        # create data frame
        dataFrameRecord = pd.DataFrame(valuesList, columns = self.columnsNames)

        return dataFrameRecord


""""""""""""""""""""""""""""""""""""""""""
""" Class with Google API function """
""""""""""""""""""""""""""""""""""""""""""
class GoogleAPI:

    # get the gps coordinates (latitude and longitude) from a zip code
    @staticmethod
    def getGPSCoord(zipCode):
        token = 'AIzaSyC2lEs3BXaBMxTMGz5UtOmJ1SKnQo4El2E'
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + str(zipCode) + '+France&key=' + token
        req = requests.get(url)
        res = json.loads(req.content)
        # get latitude
        latitude = res.get('results')[0].get('geometry').get('location').get('lat')
        # get longitude
        longitude = res.get('results')[0].get('geometry').get('location').get('lng')

        return (str(latitude) + ',' + str(longitude))


#Create and feed the DataFrame with all the cars ads and export it to Excel and CSV format
def main():

    # initialize objects
    dataFrame = DataFrame()

    # we create the data frame
    dfAdsCars = dataFrame.createDfAdsCars()

    # 3 regions
    regions = ['ile_de_france',
               'provence_alpes_cote_d_azur',
               'aquitaine']
    # two kind of vendors, "particulier" or "professionel"
    vendorsKind = {'f=p' : 'Particulier',
                   'f=c' : 'Professionnel'}

    # for each region
    for region in regions:
        print region
        # and for each vendor type
        for vendorKey, VendorLabel in vendorsKind.items():
            print VendorLabel
            url = 'http://www.leboncoin.fr/voitures/offres/' + region + '?o=0&q=Captur&it=1&th=0&' + vendorKey
            # get the number of pages
            numberPages = Util.getNumberPages(url)

            # for each page
            for pageIndex in range(numberPages):
                print pageIndex
                url = 'http://www.leboncoin.fr/voitures/offres/' + region + '?o=' + str(pageIndex+1) + '&q=Captur&it=1&th=0&' + vendorKey
                listUrlsAds = Util.createAdsUrls(url)

                # for each ads
                for urlAds in listUrlsAds:
                    dfRecord = dataFrame.getAdsData(urlAds)
                    dfRecord['vendor label'] = VendorLabel
                    dfRecord['region'] = region
                    dfAdsCars = dfAdsCars.append(dfRecord)

    # clean the data frame with dropna
    dfAdsCars = dfAdsCars.dropna(subset=['version','km','price','argus'], how = 'any')

    # write into csv file
    dfAdsCars.to_csv('Renault_Captur_result.csv')

# launch the main
if __name__ == "__main__":
    main()

