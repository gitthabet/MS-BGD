import requests
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


def getAllValuesForABCD(year):
    soupMairie = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
    balises = soupMairie.find_all("tr", class_="bleu")
    
    balise_A = balises[3];
    detail_A = balise_A.find_all("td", class_="montantpetit G")
    montant_HAB_A = detail_A[1].text
    montant_Strate_A = detail_A[2].text
    montant_HAB_A = int(montant_HAB_A.replace(u'\xa0', u' ').replace(' ' ,''))
    montant_Strate_A = int(montant_Strate_A.replace(u'\xa0', u' ').replace(' ' ,''))      
    
    balise_B = balises[7];
    detail_B = balise_B.find_all("td", class_="montantpetit G")
    montant_HAB_B = detail_B[1].text
    montant_Strate_B = detail_B[2].text
    montant_HAB_B = int(montant_HAB_B.replace(u'\xa0', u' ').replace(' ' ,''))
    montant_Strate_B = int(montant_Strate_B.replace(u'\xa0', u' ').replace(' ' ,'')) 
    
    balise_C = balises[15];
    detail_C = balise_C.find_all("td", class_="montantpetit G")
    montant_HAB_C = detail_C[1].text
    montant_Strate_C = detail_C[2].text
    montant_HAB_C = int(montant_HAB_C.replace(u'\xa0', u' ').replace(' ' ,''))
    montant_Strate_C = int(montant_Strate_C.replace(u'\xa0', u' ').replace(' ' ,'')) 
    
    balise_D = balises[20];
    detail_D = balise_D.find_all("td", class_="montantpetit G")
    montant_HAB_D = detail_D[1].text
    montant_Strate_D = detail_D[2].text 
    montant_HAB_D = int(montant_HAB_D.replace(u'\xa0', u' ').replace(' ' ,''))
    montant_Strate_D = int(montant_Strate_D.replace(u'\xa0', u' ').replace(' ' ,'')) 

    return [montant_HAB_A,montant_Strate_A,montant_HAB_B,montant_Strate_B,montant_HAB_C,montant_Strate_C,montant_HAB_D,montant_Strate_D]


Dates = [2010,2011,2012,2013]
print "Exercice" 
print "HAB_A Strate_A HAB_B Strate_B HAB_C Strate_C HAB_D Strate_D"

for date in Dates: 
    print date
    print getAllValuesForABCD(date)

