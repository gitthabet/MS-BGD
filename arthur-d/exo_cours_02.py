#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sys, re, getopt, string

def get_page_soup(url):
	r = requests.get(url)
	return BeautifulSoup(r.text)

def get_user_karma(url, user):
	r = requests.get(url+user)
	soup = BeautifulSoup(r.text)
	return soup
	#

def get_user_link(soup):
	users = soup.find_all("a", href=re.compile("^(user\?).*"))
	return users


def main():
	url = "https://news.ycombinator.com/"
	users = get_user_link(get_page_soup(url))
	for user in users:
		print user.getText(), ": "
		print get_user_karma(url, user)


if __name__ == "__main__":
	main()