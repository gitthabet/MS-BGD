# author Claire Feldman
#
import requests
from bs4 import BeautifulSoup



def recherche(annee):
    annee_str = str(annee)
    result = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+annee_str)
    mts_annee = []

    if result.status_code == 200:
        print 'request successful'
        result.encoding = 'utf-8'
        soup = BeautifulSoup(result.text)
        tous_montants_td = []
        tous_montants_td = soup.find_all("td", "montantpetit G")
#        print(soup.prettify())
#        print tous_montants_td

# traitement pour récupérer le montant
        tous_montants_trt = []
        if tous_montants_td == []:
            print "année vide"
            return 0
        else:
            for montant_td in tous_montants_td:
                texte = str(montant_td)
                texte1 = texte.split('<td class="montantpetit G">')[1]
                tous_montants_trt.append(texte1.split("\xc2\xa0</td>")[0])
 #       print tous_montants_trt

# ranger les montants qui nous intéressent dans un dict
        dict_mt = {}
        dict_mt["mt_A_par_hab"] = tous_montants_trt[1]
        dict_mt["mt_A_par_strate"] = tous_montants_trt[2]
        dict_mt["mt_B_par_hab"] = tous_montants_trt[4]
        dict_mt["mt_B_par_strate"] = tous_montants_trt[5]
        dict_mt["mt_C_par_hab"] = tous_montants_trt[10]
        dict_mt["mt_C_par_strate"] = tous_montants_trt[11]
        dict_mt["mt_D_par_hab"] = tous_montants_trt[13]
        dict_mt["mt_D_par_strate"] = tous_montants_trt[14]
        print(dict_mt)
        return dict_mt

    else:
        print 'request failed'
    
    return mts_annee

fichier=open("fic_result.txt",'w') 

# Annees 2009 a 2013
ans=[2009,2010,2011,2012,2013]
for an in ans:
    print("trt annee"+str(an))
    fichier.write("annee "+str(an)+'\n')
    mts_annee = recherche(an)
    if mts_annee == 0:
        fichier.write('\n')
    else:
        for cle,valeur in mts_annee.items():
            fichier.write(cle+" : "+valeur+'\n')


fichier.close()

