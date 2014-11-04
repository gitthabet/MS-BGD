#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, re
from bs4 import BeautifulSoup
from github import Github
import numpy as np

KEY_TOKEN = "3dd7d7655b6016ea7bbbf67a1f651326be493a47"

def getKey(item):
	return item[1]

def sort_contrib(C):
	print "sorting"
	C2 = sorted(C, key=getKey)
	for contrib in C2:
		print contrib[0], " ", contrib[1]


def get_etoiles_user(full_name):
	m = 0
	g = Github(KEY_TOKEN)
	if g != None:
		user = re.split("\s", full_name)[0]
		print user, " :"
		repos_list = g.get_user(user).get_repos()
		list_star = []
		for repo in repos_list:
			list_star.append(repo.stargazers_count)
		if len(list_star) > 0:
			m = np.mean(list_star)
	print m
	return m
	

def main():
	#session git hub
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