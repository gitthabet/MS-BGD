# -*- coding: utf-8 -*-
#!/usr/bin/python

import requests, re, StringIO, html5lib, csv
from ghost import Ghost
from slugify import slugify
from unicodedata import normalize
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



"""
==== Manque la lecture des pages suivantes et les coordonnées géographiques
"""
class Car:
	car_info = {
		'link' : None, 'price' : None,
		'version' : None, 'year' : None,
		'kilometers' : None, 'tel' : None,
		'seller' : None, 'argus' : None,
		'lati' : None, 'longi' : None
	}

	def __init__(self,link):
		self.car_info['link'] = link

	# définir les différentes caractéristiques de la voiture
	def set_elem(self, elem, value):
		assert elem in self.car_info.keys()
		self.car_info[elem] = value
		print elem, ", set to :", value

	#récuperrer les différentes caractéristiques de la voiture
	def get_elem(self, elem):
		assert elem in self.car_info.keys()
		return self.car_info[elem]

	#enregistrer dans fichier csv
	def put_in_csv(self):
		serie = Series([value for value in self.car_info.values()])
		serie.to_csv('cars.csv', sep=',')
		"""with open('cars.csv', 'a') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			spamwriter.writerow([value for value in self.car_info.values()])"""

"""
===== Recherche de la côte argus =======
"""
def get_argus(car):
	model = car.get_elem('version')
	year = car.get_elem('year')
	if year == None: year = 2013
	driver = webdriver.Firefox()
	driver.get("http://www.lacentrale.fr/cote-auto-renault-captur-1.5+dci+90+"+model+"+edc-"+str(year)+".html")
	elem = driver.find_element_by_id("Affiner").click()
	wait = WebDriverWait(driver, 10)
	element = wait.until(EC.presence_of_element_located((By.ID,'km')))
	driver.find_element_by_id('km').send_keys(car.get_elem('kilometers'))
	element = driver.find_element_by_class_name("BoutonCalculer").click()
	wait = WebDriverWait(driver, 10)
	element = wait.until(EC.presence_of_element_located((By.ID, 'cote_perso')))
	driver.close()
	return driver.find_element_by_id('cote_perso').text


"""
===== Recherche des différent paramettres d'une voiture donnée
"""
def get_info(link):
	models = ["life","zen","intens", "business", "série limitée hell"]
	r = requests.get(link)
	if r.status_code == 200:
		car = Car(link)
		soup = BeautifulSoup(r.text)
		balise_colRight = soup.find("div",{"class":"colRight"})

		#Type d'annonce privée/pro
		if balise_colRight != None:
			seller = balise_colRight.find("div", {"class":"upload_by"})
			if seller.find("div",{"class":"ad_pro"}) != None:
				car.set_elem('seller', 'pro')
			else:
				car.set_elem('seller', 'priv')

			#prix
			price = balise_colRight.find("span", {"class":"price"}).getText().strip()
			price = int(''.join([c for c in price if c in '1234567890']))
			car.set_elem('price', price)

			#kilomètres, année de la voiture
			balise_criterias = balise_colRight.find("div",  {"class":"lbcParams criterias"})
			if balise_criterias != None:
				balise_tr = balise_criterias.find_all("tr")
				for tr in balise_tr:
					key = slugify(tr.find("th").getText())
					if "kilom" in key:
						kilom = int("".join([c for c in tr.find("td").getText().strip() if c in '1234567890']))
						car.set_elem('kilometers', kilom)
					if "annee" in key:
						year = int(tr.find("td").getText().strip())
						car.set_elem('year', year)

			#version de la voiture
			balise_description = balise_colRight.find("div", {"class":"AdviewContent"})
			if balise_description != None:
				content = slugify(balise_description.find("div", {"class":"content"}).getText())
				for model in models:
					if model in content:
						car.set_elem('version', model)
						break

				#num tél du proprio
				phone = re.search(r'((\+[0-9]{2})|0).?[1-9](.?[0-9]{2}){3}.?[0-9]{2}', content)
				if phone != None:
					car.set_elem('tel', "".join([c for c in phone.group(0) if c in "1234567890"]))
				else:
					print ""
		"""#côte argus
		argus = get_argus(car)
		argus  = int("".join([c for c in argus if c in "1234567890"]))
		car.set_elem('argus', argus)"""

		#put in csv file
		car.put_in_csv()

"""
====== Parcours des liste de voitures
"""
def get_cars(soup, search_words):
	balise_content = soup.find("div", {"class":"list-lbc"})
	balises_ads = balise_content.find_all("a")
	for ad in balises_ads:
		title = slugify(ad.get('title'))
		ok = True
		for word in search_words.split("+"):
			if word not in title:
				ok = False
				break
		if ok:
			get_info(ad.get('href'))

"""
===== Main =====
"""
def main():
	search = "Renault Captur"
	url = "http://www.leboncoin.fr/voitures/offres/"
	regions = ["ile_de_france", "aquitaine", "provence_alpes_cote_d_azur"]

	search_terms = slugify(search, separator="+")

	for region in regions:
		payload = {"q":search_terms}
		r = requests.get(url+region, params=payload)
		if r.status_code == 200:
			get_cars(BeautifulSoup(r.text, "html5lib"), search_terms)
		else:
			print "Can't access url" , url , region

if __name__ == "__main__":
	main()
