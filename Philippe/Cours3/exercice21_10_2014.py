import requests
from bs4 import BeautifulSoup
import html5lib


def getPersonneKarmaBS4(Personne):
	URL = "http://news.ycombinator.com/user?id=" + Personne
	res = requests.get(URL)
	if res.status_code != 200:
		print "Echec de la requete pour " + Personne
		return None
	else:
		return BeautifulSoup(res.text,"html5lib")

def analysePagePrincipale():
	URL = "http://news.ycombinator.com"
	res = requests.get(URL)
	if res.status_code != 200:
		print "Echec de la requete pour le site " + URL
	else:
		print "Scores sur ycombinator : "
		soupe = BeautifulSoup(res.text,"html5lib")
		balises_by = soupe.find_all("td", class_="subtext")#text="by", class_="subtext")
		for balise in balises_by:
			if len(balise.contents)>2 and str(balise.contents[1]) == " by ":
				Personne = str(balise.contents[2].text)
				soupePersonne = getPersonneKarmaBS4(Personne)
				baliseTexteKarma = soupePersonne.find("td",text="karma:")
				baliseMere = baliseTexteKarma.find_parent()
				print "  Karma de %s : %s" % (Personne, baliseMere.select("td:nth-of-type(2)")[0].get_text())

def main():
	analysePagePrincipale()

if __name__ == "__main__":
	main()