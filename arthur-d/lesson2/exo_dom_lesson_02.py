#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys, re, getopt, string


class DataSearch:

	def __init__(self):
		self.url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5"


	def get_page_soup(self, year):
		payload = {'exercice':year}
		r = requests.get(self.url , params=payload)
		if r.status_code == 200:
			print "get the page code for year" , year
			return BeautifulSoup(r.text)


	def get_a_habitant(self, soup, x):
		line_x = soup.find("td", text=re.compile(".* = "+x+"$"))
		res =  line_x.find_previous_sibling().find_previous_sibling().getText()
		return ''.join([c for c in res if c in '1234567890'])


	def record_data(self, year):
		soup = self.get_page_soup(year)
		letters = ['A','B','C','D']
		result = []
		for x in letters:
			result.append(self.get_a_habitant(soup, x))
		return result


class Main:

	def main():
		ds = DataSearch()  
		for year in range(2010,2014): #de 2010 compris à 2014 compris
			res = ds.record_data(year)
			print year, " ", str(res)

	if __name__ == "__main__" : 
		main()