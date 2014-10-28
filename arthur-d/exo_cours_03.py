#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Google direction API, on prend 5 villes française, donner les distance entre les villes
#API key: 
import requests, re, json
from pprint import pprint

API_KEY = "AIzaSyDIFuv6HjLHmn17Ijt1tWU6WTgVBp1KjTw"

def get_distance(a, b):
	payload = {'origin':a, 'destination':b, 'key': API_KEY, 'mode':'driving'}
	url = "https://maps.googleapis.com/maps/api/directions/json?"
	r = requests.get(url, params=payload)
	data = json.loads(r.text)
	routes = data['routes']
	print routes[0]
	#for route in routes:

	#print data

def main():
	villes = ["Caen","Paris","Marseille","Lyon", "Lille"]
	'''for i in range(0,len(villes)):
		for j in range(0,len(villes)):
			a, b = villes[i], villes[j]
			if i == j:
				print a, " ", b, " :", 0
			else:
				print a, " ", b, " :", get_distance(a,b)'''
	get_distance("Caen", "Paris")

if __name__ == "__main__":
	main()