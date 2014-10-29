import requests
# html5lib parser de meilleur qualite
import html5lib
import unicodedata
from bs4 import BeautifulSoup
import json




# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

""" getUsersLinks recupere les liens et les users des 256 plus actifs de GitHub """
def getAPIcity(city_a,city_b):
   link = ('https://maps.googleapis.com/maps/api/distancematrix/json?origins=' + city_a + '&destinations='+city_b+'&mode=driving&language=fr-FR&key=AIzaSyDoW_3Q8oJ-wCmHAO374P405bthsbJhDYM')
   print link
   r = requests.get(link)
   if(r.ok):
        repoItem = json.loads(r.text)
        print repoItem
   return repoItem['rows'][0]['elements'][0]['distance']['value'] 




        
getAPIcity('Caen','Paris')