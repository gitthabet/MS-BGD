import pandas
import json

csv='paul Mochkovitch,	47 rue barault, home'

#Pour spliter le caractère du split est a specifier, retourne un tableau
csV.split(',')

#enlever les espaces avt après
csV.split(',')[0].strip()

#changer de caractère
csV.split(',')[0].replace('h','b')

#majuscule/minuscule
csV.split(',')[0].strip().lower()
csV.split(',')[0].strip().upper()
#premiere lettre en capitale
csV.split(',')[0].strip().capitalize()

#faire des templates
f="je m'appelle XXX"
f.format(['Paul'])

#index permet de retourner la position du caractère trouvé
csV.split(',')[0].strip().index('+')


#####################################################

#EXPRESSIONS REGULIERES detecter un numreo, un style de mot etc...

import re

credit_cards='thx for paying with 1234-2345-4567-5678'
#on veut detecter le pattern de chiffre dans ce texte

#regarder cheat sheet pour les construire 
cred=re.compile(r'\d{4}-\d{4}-\d{4}-\d{4}')
matches=cred.findall(credits_cards)
# va renvoyer  ['1234-2345-4567-5678']

#$ dollar veut dire a la fin du mot 
#on peut ajouter des flags, typiquement ignoré la case sensitive etc ...
cred=re.compile(r'\d{4}-\d{4}$')
cred.sub('XXXX-XXXX',credits_cards)
#resultat 'thx for paying with 1234-2345-XXXX-XXXX'

#il faut taper regex email par exemple dans google pour trouver l'expression reguliere pour detecter un email
#pour tester une expression reguliere regex101.com/#python


#MANIPULATION DE PANDA

#on peut exporter en dataframe apres
#mettre des paranthèses dans les expressions regulieres permet de pouvoir les recuperer

#####################################################
data=DataFrame(matches)

#regarder la doc de pandas pour retrouver les fcts
#example rename
#changer l'index
df.index=df.index.map(lambda x: 'Eleve'+str(x))

#on peut filtrer les duplicates avec pandas et la fonction drop duplicates
