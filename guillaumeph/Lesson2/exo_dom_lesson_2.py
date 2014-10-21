# -*- coding: utf-8 -*-
import urllib2
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

#définition des paramètres
Url_to_crawl = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='

Headers_Rows = ['A : TOTAL DES PRODUITS DE FONCTIONNEMENT', 'B = TOTAL DES CHARGES DE FONCTIONNEMENT', 'C = TOTAL DES RESSOURCES D_INVESTISSEMENT','TOTAL DES EMPLOIS D_INVESTISSEMENT']
Headers_Rows_light = ['A', 'B', 'C', 'D']
Rows = [10, 14, 22, 27]
Headers_Columns = ['Euros par habitant', 'Moyenne de la strate']
Columns = [2, 3]


# Returns the HTML content from a given url
def GetSoupFromUrl (url):
    try:
        fileHandle  = urllib2.urlopen(url)
    	html = fileHandle.read()
    	fileHandle.close()
    	# print 'html crawling successful'
        
        soup=BeautifulSoup(html)
	soup.Prettify
	# print soup
	return soup

    except urllib2.URLError, e:
        print 'you got an error with the request', e
        return none 


# SELECTION DES CELLULES DANS LE TABLEAU

# Prend en input l'output de GetSoupFromURL
def Crawl_values(pageweb,Headers_Rows,Rows,Headers_Columns,Columns):
    
    Montants_par_habitant = []
    Montants_par_strate = []

    for i in Rows:
        Montant_Hab = pageweb.select('tr:nth-of-type('+str(i)+') > td:nth-of-type('+str(Columns[0])+')')
        Montant_Strate = pageweb.select('tr:nth-of-type('+str(i)+') > td:nth-of-type('+str(Columns[1])+')')

        Montant_Hab = int(Montant_Hab[0].text.replace(" " , ""))
        Montant_Strate = int(Montant_Strate[0].text.replace(" " , ""))

        Montants_par_habitant.append(Montant_Hab)
        Montants_par_strate.append(Montant_Strate)
    
        i=i+1

    print (Headers_Rows_light)
    print [Montants_par_habitant]
    print [Montants_par_strate]
    print ('\n')

    return [[Montants_par_habitant],[Montants_par_strate]]

def get_values(Url_to_crawl, year):
    pageweb = GetSoupFromUrl(Url_to_crawl+str(year))
    print year
    result = Crawl_values(pageweb, Headers_Rows,Rows,Headers_Columns,Columns)


get_values(Url_to_crawl, 2010)
get_values(Url_to_crawl, 2011)
get_values(Url_to_crawl, 2012)
get_values(Url_to_crawl, 2013)
