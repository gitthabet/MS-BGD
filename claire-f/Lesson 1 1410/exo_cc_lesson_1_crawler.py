# author Claire Feldman
#
import sys
import requests
from bs4 import BeautifulSoup



def recherche(chanteuse):
    result = requests.get('https://www.youtube.com/results?search_query='+chanteuse)
#print result.status_code
    if result.status_code == 200:
        print 'request successful'
        soup = BeautifulSoup(result.text)
        balises_a = soup.find_all("a", class_="yt-uix-tile-link")
        links = [balise.get('href') for balise in balises_a]

        links.pop(0)

        print 'here are the links'
        print links

        count = 0
        for link in links:
            if link.find("watch") == -1:
                links.pop(count)
            count = count+1
    

# exploration des pages
        link = links[0]
        compteurs_youtube = []
        for link in links:
            pagedet = requests.get('https://www.youtube.com/'+link).text
            pagedetsoup = BeautifulSoup(pagedet)
            print "page detail", pagedetsoup.title

            compteur_likes = pagedetsoup.find_all(id='watch-like')[0].text
        #print "likes : ", compteur_likes
       
            compteur_dislikes = pagedetsoup.find_all(id='watch-dislike')[0].text
            compteur_views = pagedetsoup.find_all(class_='watch-view-count')[0].text
            compteur_likes = int(compteur_likes.replace(u'\xa0', u' ').replace(' ' ,''))
            compteur_dislikes = int(compteur_dislikes.replace(u'\xa0', u' ').replace(' ' ,''))
            compteur_views = int(compteur_views.replace(u'\xa0', u' ').replace(' ' ,''))

            chiffres = {}
            chiffres['compteur_views'] = compteur_views
            chiffres['compteur_dislikes'] = compteur_dislikes
            chiffres['compteur_likes'] = compteur_likes
            chiffres['title'] = pagedetsoup.title.text

            compteurs_youtube.append(chiffres)

            texte = (str(compteur_views)+":"+str(compteur_likes)+":"+str(compteur_dislikes)+'\n')
            fichier.write(texte)
   
        return compteurs_youtube

    else:
        print 'request failed'

def calc_totaux(cptr_chanteuse):
    nb_views = 0
    nb_likes = 0
    nb_dislikes = 0
    for cpt_page in cptr_chanteuse:
        nb_views = nb_views + cpt_page['compteur_views']
        nb_likes = nb_likes + cpt_page['compteur_likes']
        nb_dislikes = nb_dislikes + cpt_page['compteur_dislikes']
    return (nb_views,nb_likes,nb_dislikes)

fichier=open("fic_result.txt",'w') 

# RIHANNA
fichier.write("Rihanna"+'\n')
cptr_rihanna = recherche("rihanna")
totaux_rihanna = calc_totaux(cptr_rihanna)
print "Totaux rihanna", totaux_rihanna


# BEYONCE
fichier.write("Beyonce"+'\n')
cptr_beyonce = recherche("beyonce")
totaux_beyonce = calc_totaux(cptr_beyonce)
print "Totaux beyoncé", totaux_beyonce

fichier.close()

if totaux_rihanna[1]>totaux_beyonce[1]:
    print("Rihanna gagne en likes")
else:
    print("C est Beyonce qui gagne en likes")
