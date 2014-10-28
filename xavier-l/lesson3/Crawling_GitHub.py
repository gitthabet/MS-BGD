import requests
from bs4 import BeautifulSoup


# Returns a soup object from a given url
def getSoupFromUrl(url):
    result = requests.get(url)
    if result.status_code == 200:
        #print 'Request succesful'
        return BeautifulSoup(result.text)
    else:
        print 'Request failed', url
        return None


def getAllNames():
    soupGit = getSoupFromUrl('https://gist.github.com/paulmillr/2657075')
    balises = soupGit.find_all("tr")
    Name_dict={}
    for balise in balises:
        textBalise = balise.__str__()
        if textBalise.find("("):        
            Name = textBalise[textBalise.find("(")+1:textBalise.find(")")]
            Surname = textBalise[textBalise.find("rel=\"noreferrer\">")+17:textBalise.find("</a>")]
            Link = "https://github.com/"+Surname
            Name_dict[Name]=Link
    return Name_dict
    
 
Resultat = getAllNames()
print Resultat

