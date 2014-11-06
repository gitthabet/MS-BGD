import xlrd

file_location = "C:\Users\Nico\Desktop\Cours MS\Kit Big Data - Charles\Lesson 6\medicam.xls"
workbook = xlrd.open_workbook(file_location)
#le 0 permet d'indiquer que c'est le premier onglet que l'on souhaite lire
sheet = workbook.sheet_by_index(0)
# 0,0 : premiere valeur de notre tableau Excel
#sheet.cell_value(0,0)

#nombre de lignes/colonnes
#sheet.nrows
#sheet.ncols

nouvellerbs2013=[]

for ligne in range(sheet.nrows):
	if sheet.cell_value(ligne,26)!= 0 and sheet.cell_value(ligne,25)==0:
	a = sheet.cell_value(ligne,2)
	nouvellerbs2013.append(a.encode('ascii','ignore'))

print nouvellerbs2013

derbs2007 = []

for lignes in range(sheet.nrows):
	if (sheet.cell_value(lignes,26) == 0 and sheet.cell_value(lignes,25) == 0 and sheet.cell_value(lignes,24) == 0 and sheet.cell_value(lignes,23) == 0 and sheet.cell_value(lignes,22) == 0 and sheet.cell_value(lignes,21) == 0 and sheet.cell_value(lignes,20) == 0):
		b = sheet.cell_value(lignes,2)
		derbs2007.append(b.encode('ascii','ignore'))

print derbs2007