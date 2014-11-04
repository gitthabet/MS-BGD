""" Exercise: 2nd hand car prices """
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
import re
# Note: cheating by using pygeocoder 1.2.5, available at http://code.xster.net/pygeocoder/wiki/Home
from pygeocoder import Geocoder
import numpy as np

###############
# Function defs
###############

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None



## Find number of results pages
def numberOfPages(item4sale,region):
	soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/' + \
		                   region +'/?f=a&th=1&q=' + item4sale)
	for link in soup.find_all('a'):
	    if link.text==">>":
	        linkLastResult=link.get('href')
	lastPageMark = re.findall(r'=\d{1,}&',linkLastResult)
	lastPage = lastPageMark[0].strip('=').strip('&')
	print 'Query contains ' + lastPage + ' pages of results.'
	return lastPage



## Function: Get links from all results pages
def getAllLinks(region,item4sale,lastPage):
	validLinks = []
	for ipage in range(1,int(lastPage)+1):

		if ipage == 1:
			qDefString = '/?f=a&th=1&q='
		else:
			qDefString = '/?o='+str(ipage)+'&q='

		print '++++++ Page = ', ipage
		soup = getSoupFromUrl('http://www.leboncoin.fr/voitures/offres/' + \
	                       region + qDefString + item4sale)

		allLinks = [link.get('href') for link in soup.find_all('a')]
		for link in allLinks:
			if link != None:
				if re.findall(r'\d{9}.htm',link) != []:
					validLinks.append(link)
	return validLinks



def getCoteData(car,year):
	"""Function: gets cote data"""
	car = item4sale
	year = str(year)
	url = 'http://www.lacentrale.fr/cote-voitures-' + car.replace('\%20','-') + '--' + year + '-.html'
	dataC = DataFrame()
	soup = getSoupFromUrl(url)
	argusModelLink = [link.find_all('a')[0].get('href') for link in soup.find_all(class_ = "tdSD QuotMarque")]
	argusModelText = [link.text.strip('\n').replace(';','') for link in soup.find_all(class_ = "tdSD QuotMarque")]
	argusModelCote = [] 

	for link in argusModelLink:
		soup = getSoupFromUrl('http://www.lacentrale.fr/'+link)
		cote = soup.find_all(class_ = 'Result_Cote')[0].text[0:6].replace(' ','')
		#print 'cote = ', cote
		argusModelCote.append(cote)

	i = 0
	for desc in argusModelText:
		result = DataFrame({'Model':[desc], 'Cote': [argusModelCote[i]]})
		#print result
		dataC = dataC.append(result)
		i += 1
	return dataC



def addRowAsIndex(pdDataStruc):
	"""Adds a row number index to data structure"""
	mLin, nCol = pdDataStruc.shape
	pdDataStruc['indx'] = range(0,mLin)
	pdDataStruc = pdDataStruc.set_index('indx')
	return pdDataStruc



def makeCarData(item4sale,region,coteData):
	"""Produces data table for car item4sale sold in leboncoin.fr at given region.
	Requires Argus cote dataframe as coteData.
	Fields are: City, Id = index in query results page, Kms, Lat(city), Lon(city),
	Model = item description, PCode = postal code, Phone, Price, 
	User = Pro[fessionnel]/Par[ticulier],  Year, Argus = cote, cCher = True if (Price > Argus) """

	# determine number of pages and get all valid links
	nPages = numberOfPages(item4sale,region)
	validLinks = getAllLinks(region,item4sale,nPages)

	# get info from all ads
	data = DataFrame()
	item = 0
	for link in validLinks:
		item += 1
		print 'Item ' + str(item) + ' of ' + str(len(validLinks))
		soup = getSoupFromUrl(link)

	    #Check car model
		carModel = soup.select("table:nth-of-type(2) tr:nth-of-type(2) td")[0].text.lower()
		if carModel != 'captur':
			print '********** Warning: model = ' + carModel + ', moving on...'
		else:
			#get user type
			user = soup.find_all(class_ = "upload_by")[0].text.strip().split('\n')[0]
			userTyp = 'Pro'
			if user.split(' ')[0] != 'Pro':
				userTyp = 'Par'
			#get car model, city, postal code
			title = soup.find_all(id = "ad_subject")[0].text.replace(';','')
			city = soup.select("table:nth-of-type(1) tr:nth-of-type(2) td")[0].text
			try:
				postalCode = soup.select("table:nth-of-type(1) tr:nth-of-type(3) td")[0].text
			except IndexError:
				print '***** Warning: Error in postal code'
				postalCode = []

	        #get car price, kms
			carItem = soup.find_all(class_ = "floatLeft")[0].text
			price = int( re.findall(r'\d{1,} \d{3}',carItem)[0].replace(' ','') )
			if re.findall(r'\d{1,} \d{3} KM',carItem):
				kilom = int( re.findall(r'\d{1,} \d{3} KM',carItem)[0].replace(' ','').replace('KM','') )
			elif re.findall(r'\d{1,} KM',carItem):
				kilom = int( re.findall(r'\d{1,} KM',carItem)[0].replace(' ','').replace('KM','') )
			else:
				kilom = None

	        #get year
			year  = int( re.findall(r'\d{4}',carItem)[1] )
			if (year<2011 or year > 2014):
				print '***** Warning: year = ' + str(year) + ' setting to None'
				year = -1

			#get seller telephone
			OfferRef = link.split('/')[4].split('.')[0]
			sellerLink = 'http://www2.leboncoin.fr/ar/form/0?ca=21_s&id=' + OfferRef
			soupSel = getSoupFromUrl(sellerLink)
			content = soupSel.find_all(class_ = "content")[0].text
			sellerTel = re.findall(r'\d{10}',content)
			if sellerTel == []:
				print '***** Warning: could not find telephone, setting to empty'
				sellerTel = []
			else:
				sellerTel = sellerTel[0]

	        #get lat, lon for city
			latCity, lonCity = Geocoder.geocode(city,"france").coordinates
			#print city, latCity, lonCity

			result = DataFrame({'Id':[item-1], 'User': [userTyp],'Model': [title], \
								'Price': price, 'Year': year, 'Kms': kilom, 'Phone': [sellerTel], \
								'City': [city], 'PCode': [postalCode], \
								'Lat': [latCity], 'Lon': [lonCity]})
			data = data.append(result)
	data = addRowAsIndex(data)


    ## Match car description to Argus types
    #init item Argus cote
	data['Argus'] = np.zeros(data.shape[0])
    #start 
	for i in range(0,data.shape[0]):
		#get word list for car description
		desc = data[i:i+1].Model
		#print desc
		mod = desc[i].upper().split(' ')
		for word in ['RENAULT', 'CAPTUR']:
			if word in mod:
				mod.remove(word)
		wMatches = np.zeros(coteData.shape[0])
		# loop Argus types
		for k in range(0,coteData.shape[0]):
			mType = coteData[k:k+1].Model
			for word in mod:
				if word in mType[k].split(' '):
					#print word, mType
					wMatches[k] += 1
		#print wMatches,wMatches.argmax()
		data.Argus[i] = coteData.Cote[wMatches.argmax()]

	data['cCher'] = (data.Price>data.Argus)

	#saving data
	filename = 'carPriceData_' + item4sale.replace('\%20','_') + '_' + region + '.csv'
	data.to_csv(filename, encoding='utf-8')

	return data



#################
# Main
#################

# Params init
region = 'provence_alpes_cote_d_azur'
item4sale = 'Renault\\%20captur'
yearArgus = 2013

# get Argus cote
coteData = getCoteData(item4sale,yearArgus)
coteData = addRowAsIndex(coteData)

dataset = DataFrame()
for region in ['ile_de_france','provence_alpes_cote_d_azur','aquitaine']:
	print 'Getting data for region ' + region.upper().replace('_',' ')
	resultData = makeCarData(item4sale,region,coteData)
	dataset = dataset.append(resultData)
	
dataset = dataset.drop('Id',axis=1)
dataset = addRowAsIndex(dataset)

filename = 'carPriceData_' + item4sale.replace('\%20','_') + '_global' + '.csv'
#saving data
#optionally use: data.to_csv(filename, encoding='utf-16')
dataset.to_csv(filename, encoding='utf-8')
