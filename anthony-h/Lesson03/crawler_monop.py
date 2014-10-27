# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def get_monop_rayons():
	url = "http://courses.monoprix.fr/magasin-en-ligne/courses-en-ligne.html"
	r = requests.get(url)
	soup = r.BeautifulSoup(r.text)
	rayons = find("ul", class_="SideNav").find_all("a").get('href')




def main():
	get_monop_soup(url)

if __name__ == "__main__":
	main()