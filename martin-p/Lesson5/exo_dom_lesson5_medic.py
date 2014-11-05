import re
import pandas as pd

######################################### VAR ######################################

v_short_name = 'NOM COURT'
v_product = 'PRODUIT'
v_delisting_date = 'Date de Deremboursement'
v_refund_base = 'Base de remboursement '
v_min_year = 2008
v_max_year = 2014

######################################### FUNCTIONS ######################################

def deleteProduct(dataFrame):
	wordToRemove = str(dataFrame[v_product]).split(' ')
	n = str(dataFrame[v_short_name])
    # remove the word
	for word in wordToRemove:
		n = n.replace(word, '')
	return n

def refund(dataFrame, discontinue):
	firstYear = 2008
	lastYear = 2008
	for year in range(v_min_year, v_max_year):
		val = int(re.sub(r'\D','',dataFrame[v_refund_base + str(year)]))
		if val > 0:
			lastYear = year + 1
	if lastYear == 2014 or discontinue == True:
		for year in range(v_min_year, v_max_year):
			val = int(re.sub(r'\D','',dataFrame[v_refund_base + str(year)]))
			if val > 0:
				firstYear = year
				break
	return firstYear

def delisting(dataFrame):
	lastYear = 2008
	for year in range(2008,2014):
		val = int(re.sub(r'\D', '', dataFrame[v_refund_base + str(year)]))
		if val > 0:
			lastYear = year + 1
	return lastYear

##########################################################################################

def main():

	# get and clean the dataset
    dataset = pd.read_csv('MEDICAM 2008-2013-AMELI.csv', sep=';').dropna()

    dataset[v_short_name] = dataset.apply(lambda x : deleteProduct(x), axis = 1)
    print dataset[[v_product, v_short_name]][0:20]

    dataset[v_delisting_date] = dataset.apply(lambda x : delisting(x), axis = 1)
    print dataset[[v_product, v_delisting_date]][dataset[v_delisting_date] < v_max_year].shape
    print dataset[[v_product, v_delisting_date]][dataset[v_delisting_date] < v_max_year][0:20]

    dataset[v_delisting_date] = dataset.apply(lambda x : refund(x, False),axis = 1)
    print dataset[[v_product, v_delisting_date]][dataset[v_delisting_date] > v_min_year].shape
    print dataset[[v_product, v_delisting_date]][dataset[v_delisting_date] > v_min_year][0:20]

if __name__ == "__main__":
    main()