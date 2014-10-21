# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 23:39:18 2014

@author: Romain
"""

import requests
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if(result.status_code == 200):
        print('Request succesful')
        return BeautifulSoup(result.text)
    else:
        print('Request failed', url)
        return None

# initialize result list
result_list = []

# Initialization parameters
year = 2009
while(year < 2014):
    year_no = year-2009
    result_list.append([year,'','','','','','','','','',''])  
    
    # City index to be used in query
    if(year > 2009):
        city_index = '056'
    else:
        city_index = '101'
    
    # Web crawler for Paris' accounts
    html = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=' + city_index + '&dep=075&type=BPS&param=5&exercice=' + str(year))
    html_raw = html.html.select(".bleu > *")
    
    # Loop that looks for figures
    ind = 0
    while(ind < len(html_raw)):
        # finds 'A' figures
        if(html_raw[ind].text== 'TOTAL DES PRODUITS DE FONCTIONNEMENT = A'):
            result_list[year_no][1] = int(html_raw[ind-3].text.replace(u'\xa0', u'').replace(' ',''))
            result_list[year_no][2] = int(html_raw[ind-2].text.replace(u'\xa0', u'').replace(' ',''))
    
        # finds 'B' figures
        if(html_raw[ind].text== 'TOTAL DES CHARGES DE FONCTIONNEMENT = B'):
            result_list[year_no][3] = int(html_raw[ind-3].text.replace(u'\xa0', u'').replace(' ',''))
            result_list[year_no][4] = int(html_raw[ind-2].text.replace(u'\xa0', u'').replace(' ',''))
            
        # finds 'C' figures
        if(html_raw[ind].text== 'TOTAL DES RESSOURCES D\'INVESTISSEMENT = C'):
            result_list[year_no][5] = int(html_raw[ind-3].text.replace(u'\xa0', u'').replace(' ',''))
            result_list[year_no][6] = int(html_raw[ind-2].text.replace(u'\xa0', u'').replace(' ',''))
            
        # finds 'D' figures
        if(html_raw[ind].text== 'TOTAL DES EMPLOIS D\'INVESTISSEMENT = D'):
            result_list[year_no][7] = int(html_raw[ind-3].text.replace(u'\xa0', u'').replace(' ',''))
            result_list[year_no][8] = int(html_raw[ind-2].text.replace(u'\xa0', u'').replace(' ',''))
      
        # finds 'E' figures
        if(html_raw[ind].text== '= Besoin ou capacité de financement de la section d\'investissement = E'):
            result_list[year_no][9] = int(html_raw[ind-3].text.replace(u'\xa0', u'').replace(' ',''))
            result_list[year_no][10] = int(html_raw[ind-2].text.replace(u'\xa0', u'').replace(' ',''))
        ind += 1
    year += 1

result_list
