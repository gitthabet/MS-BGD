# Raoul Fokou, raoul.fokou@telecom-paristech.fr
#
import requests
from bs4 import BeautifulSoup

# defining http urls
def Search(year):
    str_year = str(year)
    result = requests.get('http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+str_year)

    if result.status_code == 200:
        print 'request successful'
        result.encoding = 'utf-8'
        soup = BeautifulSoup(result.text)
        tous_montants_td = []
        tous_montants_td = soup.find_all("td", "montyeartpetit G")

# Processing metric "tous_montants_td"
        tous_montants_trt = []
        if tous_montants_td == []:
            print "empty year"
            return 0
        else:
            for montant_td in tous_montants_td:
                texte = str(montant_td)
                texte1 = texte.split('<td class="montantpetit G">')[1]
                tous_montants_trt.append(texte1.split("\xc2\xa0</td>")[0])

# Define Metrics to capture
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
    
#   Define Years to capture
file=open("data_2009-2013.txt",'w') 

# years 2009 a 2013
years=[2009,2010,2011,2012,2013]
for year in years:
    print("trt year"+str(year))
    file.write("year "+str(year)+'\n')
    mts_year = Search(year)
    if mts_year == 0:
        file.write('\n')
    else:
        for Key,Value in mts_year.items():
            file.write(Key+" : "+Value+'\n')
file.close()

