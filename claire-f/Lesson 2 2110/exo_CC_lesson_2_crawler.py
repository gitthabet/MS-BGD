# author Claire Feldman
#
import requests
from bs4 import BeautifulSoup



def recherche():
    result = requests.get('https://news.ycombinator.com/news')
 
    if result.status_code == 200:
        print 'request successful'
        result.encoding = 'utf-8'
        soup = BeautifulSoup(result.text)
 #       print soup
        balises_td = soup.find_all("td",class_="title")
 #       print balises_td
        for balise_td in balises_td:
            print(balise_td)
            texte = str(balise_td)
            texte1 = texte.split('="top">')[1]
            if texte1.startswith('1'):
                #je vais chercher la page détail
                pagedet = requests.get('news.ycombinator.com/user?id='+link).text
                https://news.ycombinator.com/user?id=pierre-renaux
                
   

recherche()
