import json
import operator
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import math

def getSoupFromUrl(url):
	result =requests.get(url)
	if result.status_code == 200:
		return BeautifulSoup(result.text)
	else:
		print 'Request failed with ',url

def main():
	#--------------------CRAWLING
	Villes=['Caen','Paris','Marseille','Lyon','Lille']
	Distances={}
	for origin in Villes:
		Distances[origin]={}
		for destination in Villes:
			if destination!=origin:
				req=requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin+'&destinations='+destination+'&mode=driving&key=AIzaSyBOjUcK9lw3OPG-YgdyVQ7d_PscohZykVI')
				json_ville=json.loads(req.text)
				Distances[origin][destination]=json_ville['rows'][0]['elements'][0]['distance']['text']
	print Distances

if __name__ == "__main__":
    main()



