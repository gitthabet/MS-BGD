import requests
from captur import Captur
from bs4 import BeautifulSoup
import re


url = "http://www.leboncoin.fr/voitures/offres/ile_de_france/?q=renault%20captur"

class Crawler:
    def __init__(self,regions):
        self.root_url = "http://www.leboncoin.fr/voitures/offres/"
        self.regions = regions
        self.urls = list()
        self.get_data()

    def get_data(self):
        for region in self.regions:
            region_url = self.root_url + region + "/?q=renault%20captur"
            page_number = self.retrieve_page_count(region_url)
            for page in range(1,page_number):
                urls = self.retrieve_item_list(region_url,page)
                self.urls = self.urls + urls


    def retrieve_page_count(self,url):
        page = requests.get(url).text
        html = BeautifulSoup(page)
        tag = html.find('ul',{'id' : 'paging'})
        tag_class = tag['class'][1]
        page_count = int(tag_class.split('-')[1])
        return page_count

    def retrieve_item_list(self,url,page_number):
        final_url = url + "&o=" + str(page_number)
        page = requests.get(url).text
        html = BeautifulSoup(page)
        tags = html.find("div",class_="list-lbc")
        links = tags.findAll("a")

        urls = list()
        for link in links:
            urls.append(link['href'])

        return urls


crawl = Crawler(["ile_de_france","aquitaine","provence_alpes_cote_d_azur"])

capturs = list()

for craw in crawl.urls[:10]:
    capturs.append(Captur(craw))

for captur in capturs:
    captur.describe()
