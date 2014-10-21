import requests
from bs4 import BeautifulSoup

def YearReport(year):
	year=str(year)
	url= 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='+year
	
	#get html source into reponse object
	page= requests.get(url)
	
	#give html code to parse to beautiful soup
	soup= BeautifulSoup(page.text)
	
	#define the tags
	Tags=['TOTAL DES PRODUITS DE FONCTIONNEMENT = A',
	'TOTAL DES CHARGES DE FONCTIONNEMENT = B',
	"TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
	"TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
	
	#initialize final result
	report={}

	for tag in Tags :

	  # the values we want are in blocks such as :

	  # 	<tr class="bleu">
	  #   		<td class="montantpetit G">5 234 622&nbsp;</td>
	  #   		<td class="montantpetit G">2 308&nbsp;</td>
	  # 	    		<td class="montantpetit G">2 308&nbsp;</td>
	  #     		<td class="libellepetit G">TOTAL DES PRODUITS DE FONCTIONNEMENT = A</td>
	  #   		<td class="montantpetit" colspan="3" style="text-decoration:underline;text-align:center">en % des produits</td>
	  # 	</tr>

		# we need to find this block in the html file with .find() method		
		line = soup.find(text=tag).parent.parent
		# print line
		# print line.contents[1]
		# print line.contents[2]
		# print line.contents[3]
		# print line.contents[4]
		# print line.contents[5]
		# print line.contents[6]
		# print line.contents[7]
		# print line.contents[8]
		# print line.contents[9]
		# print line.contents[10]
		
		

		dataInEuros= line.contents[1].text
		dataInEuros= int(dataInEuros.replace(u'\xa0', ' ',2).replace(' ' ,''))
		
		dataPerHab= line.contents[3].text
		dataPerHab= int(dataPerHab.replace(u'\xa0', u' ').replace(' ' ,''))
		
		dataPerStrate = line.contents[5].text
		dataPerStrate= int(dataPerStrate.replace(u'\xa0', u' ').replace(' ' ,''))
		
		result={}
		result["MilEuros"]=dataInEuros
		result["EuroPerHab"]=dataPerHab
		result["MeanStrate"]=dataPerStrate
		
		report[tag]=result
	return report

# Reports={}
# Reports["Report2013"]= YearReport('2013')
# Reports["Report2012"]= YearReport('2012')
# Reports["Report2011"]= YearReport('2011')
# Reports["Report2010"]= YearReport('2010')

Report2013 = YearReport('2013')
Report2012 = YearReport('2012')
Report2011 = YearReport('2011')
Report2010 = YearReport('2010')

print Report2013
print Report2012
print Report2011
print Report2010