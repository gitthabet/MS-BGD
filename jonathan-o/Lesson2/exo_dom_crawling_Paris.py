import requests
# html5lib parser de meilleur qualite
import html5lib
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

""" getMontantABCD recupere les montants states et hab pour les totaux ABCD """
def getMontantABCD(year):
    soupYoutube = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
    balises_bleu = soupYoutube.find_all("tr", class_="bleu")
    Montant_hab=[]
    Montant_strate=[]
    i=0
    for balise in balises_bleu:
        if 'TOTAL' in str(balise):
            #netoyage des entiers
            Montanthab = balise.find_all("td")[1].text
            Montantstrate = balise.find_all("td")[2].text
            Montanthab = int(Montanthab.replace(u'\xa0', u' ').replace(' ' ,''))
            Montantstrate = int(Montantstrate.replace(u'\xa0', u' ').replace(' ' ,''))
            Montant_hab.append(Montanthab)
            Montant_strate.append(Montantstrate)
            i=i+1
    return [Montant_hab,Montant_strate]
        #print 'Here are the links', links
    #link = links[0]
    # all_metrics = []
    # for link in links:
    #     if link[0:6] == '/watch':
    #      soupPage = getSoupFromUrl('https://www.youtube.com' +link)
    #      likes_count = soupPage.find_all(id='watch-like')[0].text
    #      dislikes_count = soupPage.find_all(id='watch-dislike')[0].text
    #      views_count = soupPage.find_all(class_='watch-view-count')[0].text
    #      dislikes_count = int(dislikes_count.replace(u'\xa0', u' ').replace(' ' ,''))
    #      likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))
    #      views_count = int(views_count.replace(u'\xa0', u' ').replace(' ' ,''))
    #      metrics = {}
    #      metrics['views_count'] = views_count
    #      metrics['dislikes_count'] = dislikes_count
    #      metrics['likes_count'] = likes_count
    #      metrics['title'] = soupPage.title.text
    #      #print 'MEtrics for ', metrics
    #      all_metrics.append(metrics)
    # print 'parser succesful, metric calculated for ' + artist
    # return all_metrics
result2010 = getMontantABCD(2010)
result2011 = getMontantABCD(2011)
result2012 = getMontantABCD(2012)
result2013 = getMontantABCD(2013)

print  result2010
print  result2011 
print  result2012
print  result2013


