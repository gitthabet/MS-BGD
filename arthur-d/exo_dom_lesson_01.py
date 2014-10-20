#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, getopt
import requests  #pour faire des requêtes
from bs4 import BeautifulSoup #pour parser du html, css

def return_num(s):
	r = ''.join([c for c in s if c in '1234567890'])
	return int(r)

def is_video(url):
	return re.search("/watch", url)

def artist_request(artist):
	payload = {'search_query': artist}
	return requests.get("https://www.youtube.com/results?", params=payload)


def music_link_request(music_link):
	r =  requests.get("https://www.youtube.com" + music_link)
	nb_views, nb_like, nb_dislike = 0, 0, 0

	if r.status_code == 200:
		soup = BeautifulSoup(r.text)

		balise_view = soup.find("div", class_="watch-view-count")
		if balise_view != None: 
			nb_views = balise_view.getText()
			nb_views = return_num(nb_views)

		balise_watch_like = soup.find("button", id="watch-like")
		if balise_watch_like != None: 
			balise_like = balise_watch_like.find("span", class_="yt-uix-button-content")
			nb_like = return_num(balise_like.getText())

		balise_view_dislike = soup.find("button", id="watch-dislike")
		if balise_view_dislike != None: 
			balise_dislike = balise_view_dislike.find("span", class_="yt-uix-button-content")
			nb_dislike = return_num(balise_dislike.getText())

		if nb_dislike != None and nb_like != None and nb_views != None :
			return nb_views*float(nb_like - nb_dislike)/float(nb_like + nb_dislike)
		else: return None


def get_music_list(result):
	soup = BeautifulSoup(result.text)
	balises_a = soup.find_all("a", class_="yt-uix-tile-link")
	links = [balise.get('href') for balise in balises_a]

	musics_data = []

	for l in links:
		if is_video(l) != None:
			result = music_link_request(l)
			musics_data.append(result)
	fame = 0
	for i in musics_data:
		if i != None: fame += i
	return fame

def main():
	artistes = ["rihanna", "beyonce"]

	for a in artistes:
		r = artist_request(a)
		if r.status_code == 200: #retourne le code que retourne la page, si 200 = ok
			print "La requete marche pour l'artiste: " + a
			print "résultat pour " + a + " :", get_music_list(r)
		else:
			print "Request fail for: " + a
		

if __name__ == "__main__":
	main()