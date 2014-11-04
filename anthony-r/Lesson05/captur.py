# coding=utf-8
import requests
from bs4 import BeautifulSoup
import re

class Captur:
    def __init__(self,url):
        self.title = None
        self.year = None
        self.mileage = None
        self.price = 0
        self.owner_phone = None
        self.pro = False
        self.desciption = None
        self.gears = None
        self.fuel = None

        self.raw_data = requests.get(url).text
        self.parse_lbc_info()

    def parse_lbc_info(self):
        html = BeautifulSoup(self.raw_data)

        # Data cleaning, don't mind the mess here.
        self.title = html.find('h2',id="ad_subject").text

        self.price = int(html.find('span',class_="price").text[:-2].replace(" ","")) # Trust me I'm an engineer

        self.year = int(html.find('div',class_="lbcParams criterias").findAll('td')[2].text) # Trust me I'm an engineer

        self.gears = html.find('div',class_="lbcParams criterias").findAll('td')[5].text # Trust me I'm an engineer

        self.fuel = html.find('div',class_="lbcParams criterias").findAll('td')[4].text # Trust me I'm an engineer

        self.mileage = int(html.find('div',class_="lbcParams criterias").findAll('td')[3].text[:-3].replace(" ","")) # Trust me I'm an engineer

        self.description = html.find('div',class_="AdviewContent").find('div',class_="content").text # Trust me I'm an engineer

        self.pro = html.find('div',class_="upload_by").text.encode('utf-8').lstrip()[:14] == 'Pro Véhicules' # Trust me I'm an engineer

    def parse_owner_phone(self):
        """ We assume the phone number is in the description, please only use this method after having called parse_lbc_info"""
        pass

    def get_model(self):
        pass

    def describe(self):
        print self.title + ":"
        print str(self.price) + " - " + str(self.year) + " - " + self.gears + " - " + self.fuel + " - " + str(self.mileage) + " - " + str(self.pro)
