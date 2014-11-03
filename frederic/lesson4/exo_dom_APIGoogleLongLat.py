import requests
import unicodedata
from bs4 import BeautifulSoup
import json

def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getLongLat(city,cp):
   

   link = ('https://maps.googleapis.com/maps/api/geocode/json?address='+city+'+'+cp+'&key=AIzaSyDZsaD7vuuFVqQ3kYLV9nefQTvmm0jGLKo')
   
   print link
   r = requests.get(link)
   print r.status_code
   if(r.ok):
        repoItem = json.loads(r.text)
   latitude= repoItem['results'][0].get('geometry').get('location').get('lat')
   longitude= repoItem['results'][0].get('geometry').get('location').get('lng')
 
   return longitude,latitude

city='paris'
cp='75012'
        
longitude,latitude=getLongLat(city,cp)
print longitude,latitude