import requests
from bs4 import BeautifulSoup


#print balises_td

def getInfo(annee):
	exercice=str(annee)
	url= 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+ exercice
	result = requests.get(url)
	soup=BeautifulSoup(result.text)
	balises_td=soup.find_all("td",class_="montantpetit G")

	A_parhabitant=balises_td[1].text;
	A_parhabitant=int(A_parhabitant.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	A_moyenneStrate=balises_td[2].text;
	A_moyenneStrate=int(A_moyenneStrate.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	print "A_parhabitant "+ exercice +" = " , A_parhabitant
	print "A_moyenneStrate "+ exercice +" = " , A_moyenneStrate

	B_parhabitant=balises_td[4].text;
	B_parhabitant=int(B_parhabitant.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	B_moyenneStrate=balises_td[5].text;
	B_moyenneStrate=int(B_moyenneStrate.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	print "B_parhabitant "+ exercice +" = " , B_parhabitant
	print "B_moyenneStrate "+ exercice +" = " , B_moyenneStrate

	C_parhabitant=balises_td[10].text;
	C_parhabitant=int(C_parhabitant.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	C_moyenneStrate=balises_td[11].text;
	C_moyenneStrate=int(C_moyenneStrate.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	print "C_parhabitant "+ exercice +" = " , C_parhabitant
	print "C_moyenneStrate "+ exercice +" = " , C_moyenneStrate

	D_parhabitant=balises_td[13].text;
	D_parhabitant=int(D_parhabitant.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	D_moyenneStrate=balises_td[14].text;
	D_moyenneStrate=int(D_moyenneStrate.replace('<td class="montantpetit G">',"").replace(' ' ,''))
	print "D_parhabitant "+ exercice +" = " , D_parhabitant
	print "D_moyenneStrate "+ exercice +" = " , D_moyenneStrate

	return None

for annee in [2010,2011,2012,2013]:
	getInfo(annee)

#for balise in balises_td
#	if balise[18]=1 or balise[18]=2
#		likes_count = int(likes_count.replace(u'\xa0', u' ').replace(' ' ,''))

#<td class="montantpetit G">2 308&nbsp;</td>
#<td class="montantpetit G">2 235&nbsp;</td>
#<td class="montantpetit G">1 157&nbsp;</td>
#<td class="montantpetit G">1 048&nbsp;</td>

#<td class="montantpetit G">2 308&nbsp;</td>
#<td class="montantpetit G">2 235&nbsp;</td>
#<td class="montantpetit G">1 157&nbsp;</td>
#<td class="montantpetit G">1 048&nbsp;</td>