import requests
# html5lib parser de meilleur qualite
import html5lib
import unicodedata
from bs4 import BeautifulSoup

def between(myString, start, stop):
  beg = myString.index(start) + len(start)
  end = myString.index(stop, beg)
  return myString[beg:end]
def before(myString,Symbol):
    end = myString.index(Symbol)
    return myString[0:end]  


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text,"html5lib")
    else:
        print 'Request failed', url
        return None

""" getUsersLinks recupere les liens et les users des 256 plus actifs de GitHub """
def getUsersReferences():
    soupYoutube = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
    balises_a = soupYoutube.find_all("table", cellspacing="0")
    Users_dict={}
    for i in range(2,258):
        References={}
        Users_line = balises_a[0].select("tr:nth-of-type("+str(i)+")")
        User_name = unicodedata.normalize('NFKD',Users_line[0].select("td:nth-of-type(1)")[0].text).encode('ascii','ignore')
        References['Link']=between(str(Users_line[0].select("td:nth-of-type(1)")[0]),'href=',' rel=').replace('"','')
        References['Contributions']=str(Users_line[0].select("td:nth-of-type(2)")[0].text)
        References['Language']=str(Users_line[0].select("td:nth-of-type(3)")[0].text)
        References['Location']=unicodedata.normalize('NFKD',Users_line[0].select("td:nth-of-type(4)")[0].text).encode('ascii','ignore')
        Users_dict[str(User_name)]=References
        print User_name, References
    return Users_dict

def addUsersRepositoryAPI(Users_dict):
    for user in Users_dict:
        print Users_dict[user]['Link']

Users_dict=getUsersReferences()
addUsersRepositoryAPI(Users_dict)