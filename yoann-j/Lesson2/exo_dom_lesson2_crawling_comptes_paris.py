import requests
import sys
import html5lib
from bs4 import BeautifulSoup

#Retrieve the HTML soup from the given URL
def getSoupfromURL(url):
	#Retrieve HTML code for the given URL
  result = requests.get(url)
  #Check that the request was done successfully and return the soup
  if result.status_code == 200:
    print url + " : " + "Request successful"
    return BeautifulSoup(result.text, "html5lib")
  else:
    print "Request failed : ", url
    return None

#Get the yearly financial data for Paris city on http://alize2.finances.gouv.fr/ for the given year (string format)
def getYearlyFinancialData (year, requiredDataList):
  
  #Get soup from the webpage
  yearlyFinancialStatementPageSoup = getSoupfromURL ('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year)

  #Initialize the dictionnary to store the data
  dataDictionary = {}  
  index = 1
  for requiredData in requiredDataList:
    
    #Get the Object associated to the required data
    requiredDataObject = yearlyFinancialStatementPageSoup.find('td', text=requiredData)
   
    #Get the Parent Object
    requiredDataObjectParent = requiredDataObject.findParent()
    
    #Get the "Euros par habitant" and "Moyenne de la strate" values 
    eurosParHabitantInformation = requiredDataObjectParent.select('td:nth-of-type(2)')[0].string
    eurosParHabitantValue = int (eurosParHabitantInformation.replace(u'\xa0', u' ').replace(' ' ,''))

    moyenneDeLaStrateInformation = requiredDataObjectParent.select('td:nth-of-type(3)')[0].string
    moyenneDeLaStrateValue = int (moyenneDeLaStrateInformation.replace(u'\xa0', u' ').replace(' ' ,''))

    #Add data to the dictionary
    dataDictionary.update ({str(index)+ " " + requiredData + ' - ' + 'Euros Par Habitant' : eurosParHabitantValue})
    dataDictionary.update ({str(index)+ " " + requiredData + ' - ' + 'Moyenne par strate' : moyenneDeLaStrateValue})
    index +=1
  return dataDictionary
  

def main():
    
    #Create the overall dictionary
    allYearsDataDictionary = dict()

    requiredDataList= ["TOTAL DES PRODUITS DE FONCTIONNEMENT = A", "TOTAL DES CHARGES DE FONCTIONNEMENT = B", "TOTAL DES RESSOURCES D'INVESTISSEMENT = C", "TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
    
    for year in range(2010,2014):
      yearlyDictionary = getYearlyFinancialData(str(year), requiredDataList)
      allYearsDataDictionary.update({str(year) : yearlyDictionary})

    for key1, value1 in sorted(allYearsDataDictionary.items()):
      print "\nAnnee " + str(key1) + " : \n"
      for key2, value2 in sorted(value1.items()):
        print str(key2) + " : " + str(value2)

if __name__ == "__main__":
    main()




  
