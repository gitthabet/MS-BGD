# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests, re, unicodedata
from bs4 import BeautifulSoup

class Car:
	car_info = {
		'link' : None, 'pric' : None, 
		'version' : None, 'year' : None, 
		'kilometers' : None, 'tel' : None,
		'seller' : None, 'argus' : None, 
		'lati' : None, 'longi' : None
	}
	
	def __init__(self,link):
		self.car_info['link'] = link
		print link

	def set_elem(self, elem, value):
		assert elem in self.car_info.keys()
		self.car_info[elem] = value
		print elem, ", set to :", value


def norm(text):  #normalisation du texte
	text = unicode(text)
	return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')).lower()

def get_info(link):
	models = ["life","zen","intens", "business", "série limitée hell"]
	r = requests.get(link)
	if r.status_code == 200:
		car = Car(link)
		soup = BeautifulSoup(r.text)
		balise_container = soup.find("div", {"class":"colRight"})

		#Type d'annonce privée/pro
		seller = balise_container.find("div", {"class":"upload_by"})
		if seller.find("div",{"class":"ad_pro"}) != None:
			car.set_elem('seller', 'pro')
		else:
			car.set_elem('seller', 'priv')

		#prix
		price = int(balise_container.find("span", {"class":"price"}).getText().strip())
		car.set_elem('price', price)

def get_cars(soup, search_words):
	balise_content = soup.find("div", {"class":"list-lbc"})
	balises_ads = balise_content.find_all("a")
	for ad in balises_ads:
		title = norm(ad.get('title'))
		ok = True
		for word in search_words.split("+"):
			if word not in title:
				ok = False
				break
		if ok:
			get_info(ad.get('href'))
						

def main():
	search = "Renault Captur"
	url = "http://www.leboncoin.fr/voitures/offres/"
	regions = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]

	search_terms = norm(re.sub(r'\s+', "+", search))

	for region in regions:
		payload = {"q":search_terms}
		r = requests.get(url+region, params=payload)
		if r.status_code == 200:
			get_cars(BeautifulSoup(r.text), search_terms)
		else:
			print "Can't access url" , url , region 

if __name__ == "__main__":
	main()