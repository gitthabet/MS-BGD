import requests
from bs4 import BeautifulSoup
import re
import json

# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None

def getAllHackers():
   
    result = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
    balises_tr = result.find_all("tr")

    for balise_tr in balises_tr:
        user=balise_tr.select("td:nth-of-type(1)")[0].text.split(" ")[0].strip()
#        print 'user ', user
#init val dico  pour chaque cle :     
        users[user]=0

def NbStars(json_user):
    sum=0
    for i in range(len(json_user)):
        sum=sum+json_user[i]['stargazers_count']
    return sum/len(json_user)

users={}
getAllHackers()
print'===================================='
print(users)
for user in users.keys():
#    print 'user ', user
    req=requests.get('https://api.github.com/users/'+user+'/repos')
#    print'aaaaaaaa'
    json_user=json.loads(req.text)
#    print 'json_user ', json_user
    users[user]=NbStars(json_user)

print sorted(users.iteritems(), reverse=True, key=operator.itemgetter(1))