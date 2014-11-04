import requests
from bs4 import BeautifulSoup
import re

class Models:
    def __init__(self):
        self.url = "http://www.lacentrale.fr/cote-voitures-renault-captur--2013-suv_4x4.html"
        self.models = list()
        self.retrieve_models()

    def retrieve_models(self):
        raw_data = BeautifulSoup(requests.get(self.url).text)
        table = raw_data.find('table',id="TabAnnHomeCote")
        models = table.findAll('tr')
        models.pop(11)
        models.pop(0)
        for model in models:
            title = model.find('td',class_="tdSD QuotMarque").find('a').text
            url = model.find('td',class_="tdSD QuotMarque").find('a')['href']
            gear = model.find('td', class_="tdSD QuotBoite").text
            fuel = model.find('td', class_="tdSD QuotNrj").text
            self.models.append(Model(title,url,gear,fuel))


class Model:
    def __init__(self,title,url,gear,fuel):
        self.title = title
        self.price = 0
        self.gears = gear
        self.fuel = fuel
        self.url = url
        self.get_price()

    def get_price(self):
        raw_data = BeautifulSoup(requests.get("http://www.lacentrale.fr/"+self.url).text)
        price = int(raw_data.find('span',class_="Result_Cote").text[:-2].replace(" ",""))
        self.price = price
