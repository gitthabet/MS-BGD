import requests
from bs4 import BeautifulSoup
import html5lib

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text, "html5lib")
    else:
        print 'Request failed', url
        return None

def getDataForEachYear(year):
    soup=getSoupFromUrl('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year)
    balises= soup.find_all("td", class_='montantpetit G')
    print balises
    figures=[]
    #print type(figures)
    #print type(balises[0].text.encode('utf8'))
    #print "bla"+balises[0].text
    #print "bla"+balises[1].text
    #print "bla"+balises[1].text
    n=len(balises)-1;
    print "taille de figures",n
    for i in range(n):
        figures.append(int(balises[i].text.replace(u'\xc2\xa0', u' ').replace(' ' ,'')))
    print "fig",figures
    exercices=['A','B','C','D']
    #print exercices
    #positions=[2,3,5,6,11,12,14,15]
    positions=[1,4,10,13]
    #print type(positions[0])
    resultats={}
    all_resultats=[]
    #print type(resultats)
    #print type(exercices[0])
    for i in range(4):
        all_resultats.append(exercices[i])
        resultats['Par strate']=figures[positions[i]+1]
        resultats['Par hbs']=figures[positions[i]]
        #print resultats
        all_resultats.append(resultats)
        resultats={}
    print all_resultats


getDataForEachYear('2013')
getDataForEachYear('2012')  
getDataForEachYear('2011')
getDataForEachYear('2010')
