import requests
from bs4 import BeautifulSoup
import html5lib


def getBeautifulSoupFromURL(URL):
	res = requests.get(URL)
	if res.status_code != 200:
		print "Echec de la requete", URL
		return None
	else:
		print "Succes de la requete"
		return BeautifulSoup(res.text, "html5lib")    # text contient le code HTML associé à res

def getPopulariteArtiste(artiste):
	soupYouTube = getBeautifulSoupFromURL("http://youtube.com/results?search_query=" + artiste)
	balises_a = soupYouTube.find_all("a",class="yt-uix-title-link") # liste des balises HTML de type a et de style yt-uix-title-link
	liensVideoArtiste = [balise.get("href") for balises in balises_a] # liste des URL correspondant aux résultats de la requête Rihanna
	liensVideoArtiste.pop(0)    # Pour enlever le 1er élément, non pertinent
	populariteAll = []
	for lien in liensVideoArtiste:
		if lien[:6] == "/watch":
			soupVideo = getBeautifulSoupFromURL("http://http://www.youtube.com/" + lien)
			likeCountStr = soupVideo.find_all(id="watch-like")[0].text
			likeCountStr.replace(u'\xa0',u' ').replace(" ","")      # pour nettoyer la donnée récupérée de ses cochonnries !
			likeCount = int(likeCountStr)
			dislikeCountStr = soupVideo.find_all(id="watch-dislike")[0].text
			dislikeCountStr.replace(u'\xa0',u' ').replace(" ","")
			dislikeCount = int(dislikeCountStr)
			viewCountStr = soupVideo.find_all(class_="watch-view-count")[0].text
			viewCountStr.replace(u'\xa0',u' ').replace(" ","")
			viewCount = int(viewCountStr)
			popularite['titre'] = soupVideo.title.text
			popularite['vues'] = viewCount
			popularite['aime'] = likeCount
			popularite['naimepas'] = dislikeCount
			populariteAll.append(popularite)
	return populariteAll

def calculCritere(artiste):
	getPopulariteArtiste(artiste)
	totalVues = 0
	totalAime = 0
	totalNAimePas = 0.
	for titre in populariteTitres:
		totalVues += titre.get("vues")
		totalAime += titre.get("aime")
		totalNAimePas += titre.get("naimepas")
	critere["vues"] = totalVues
	critere["aime"] = totalAime
	critere["naimepas"] = totalNAimePas
	return critere

def main():
	critereRihanna = calculCritere("rihanna")
	critereBeyonce = calculCritere("beyonce")
	print "Les vidéos de Rihanna ont été vues %d fois sur YouTube, avec un taux de satisfaction de %f.1 et d'insatisfaction de %f.1" ...
			% (critereRihanna.get("vues"), critereRihanna.get("aime")/critereRihanna.get("vues"), critereRihanna.get("naimepas")/critereRihanna.get("vues"))
	print "Les vidéos de Beyonce ont été vues %d fois sur YouTube, avec un taux de satisfaction de %f.1 et d'insatisfaction de %f.1" ...
			% (critereBeyonce.get("vues"), critereBeyonce.get("aime")/critereBeyonce.get("vues"), critereBeyonce.get("naimepas")/critereBeyonce.get("vues"))

if __name__ == '__main__':
    main()
