""" This exercise returns info from users in ycombinator.com """

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



def getUsersFromY():
	soupYcomb = getSoupFromUrl('https://news.ycombinator.com/')
	balises_td = soupYcomb.find_all("td", class_="subtext")
	users=[]
	for balise in balises_td:
		aa = balise.text.split()
		#print aa
		if aa[2]=='by':
			user = aa[3]
			users.append(user)
	#print "Users are: " + str(users)
	users.sort()
	return users


allUsers = getUsersFromY()
print 'Retrieving data from news.ycombinator.com...'
for user in allUsers:
	soupUser = getSoupFromUrl('https://news.ycombinator.com/user?id=' + user)
	ik = soupUser.text.find('karma')
	aa = soupUser.text[ik+6:].split()
	print 'User: ' + user + ' ++ karmic force: ' + aa[0]

