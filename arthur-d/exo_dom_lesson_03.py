#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, re
from bs4 import BeautifulSoup
from github import Github

def getKey(item):
	return item[1]

def sort_contrib(C):
	C2 = sorted(C, key=getKey)
	for contrib in C2:
		print contrib[0], " ", contrib[1]


def get_etoiles_user(full_name):
	g = Github("Jaffeur", "********")
	user = re.split("\s", full_name)[0]
	repos_list = g.get_user(user).get_repos()
	tot = 0
	n = 0
	for repo in repos_list:
		n += 1
		tot += repo.stargazers_count
	if n == 0:
		return 0
	else:
		return tot/n
	

def main():
	#session git hub
	g = Github("Jaffeur", "S45tBuE4")

	r = requests.get("https://gist.github.com/paulmillr/2657075")
	if r.status_code == 200:
		soup = BeautifulSoup(r.text)
		balise_table = soup.find("table").find("tbody")
		balise_liste = balise_table.findChildren("td")
		contrib_note_list = []
		for elem in balise_liste:
			if elem.find("a") != None:
				if re.match("\s+",elem.getText()) != None:
					name = elem.getText().lstrip()
					contrib_note_list.append([name, get_etoiles_user(name)])
		sort_contrib(contrib_note_list)
	else: 
		return "La page ne peut pas être chargée"


if __name__ == "__main__":
	main()