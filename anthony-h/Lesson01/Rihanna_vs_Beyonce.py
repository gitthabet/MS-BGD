import requests
from bs4 import BeautifulSoup


url='https://www.youtube.com/results?search_query=rihanna&page=2'
result = requests.get(url)
print result

if result.status_code==200:
	print 'Succesful'
	print BeautifulSoup(result.txt)





#soupYoutube=BeautifulSoup()
#balises_a = soupYoutube.find_all("a", class_="yt-uix-tile-link")

#print balises_a