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

""" getMontantABCD recupere les montants states et hab pour les totaux ABCD dans un dictionnaire"""
def getMontantABCD(year):
    soupYoutube = getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str(year))
    balises_bleu = soupYoutube.find_all("tr", class_="bleu")
    Montant_hab={}
    Montant_strate={}
    for balise in balises_bleu:
        if 'TOTAL' in str(balise):
            #netoyage des entiers
            col = balise.find_all("td")
            Montanthab = col[1].text
            Montantstrate = col[2].text
            index = col[3].text[-1:]
            index = str(index)
            Montanthab = int(Montanthab.replace(u'\xa0', u' ').replace(' ' ,''))
            Montantstrate = int(Montantstrate.replace(u'\xa0', u' ').replace(' ' ,''))
            Montant_hab[index]= Montanthab
            Montant_strate[index] = Montantstrate
    # retourne         
    return [Montant_hab,Montant_strate]


Date = {2010,2011,2012,2013}
Compte_de_Paris_Habitants={}
Compte_de_Paris_Strates={}
for date in Date: 
    temp = getMontantABCD(date)
    Compte_de_Paris_Habitants[str(date)] = temp[0]
    Compte_de_Paris_Strates[str(date)] = temp[1]
Compte_de_Paris={}
Compte_de_Paris['Strates']= Compte_de_Paris_Strates
Compte_de_Paris['Habitants'] = Compte_de_Paris_Habitants

""" Compte_de_Paris[1*][2*][3*]
1* type 'Strates' ou 'Habitants'
2* Annee '2010' - '2013'
3* Totaux 'A','B','C','D'    """
print  Compte_de_Paris
print Compte_de_Paris['Strates']['2010']['A']
