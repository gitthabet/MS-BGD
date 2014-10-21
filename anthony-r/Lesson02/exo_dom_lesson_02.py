import urllib2
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

root_url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice="

def num(st):
  return int( st.encode('ascii','ignore') )

class YearResults:
  def __init__(self,year):
    self.data = None;
    self.year = year
    self.per_habitant = dict()
    self.per_stratum = dict()
    self.url = root_url+str(self.year)
    print self.url

  def retrieve_data(self):
    self.data = BeautifulSoup(requests.get(self.url).text)

  def parse(self):

    cells = self.data.findAll(attrs={'class': "montantpetit"})
    self.per_habitant['A'] = cells[1].text
    self.per_stratum['A'] = cells[2].text

    self.per_habitant['B'] = cells[20].text
    self.per_stratum['B'] = cells[21].text

    self.per_habitant['C'] = cells[53].text
    self.per_stratum['C'] = cells[54].text

    self.per_habitant['D'] = cells[77].text
    self.per_stratum['D'] = cells[78].text

  def describe(self):
    print self.per_habitant
    print self.per_stratum

# Retrieving URLs
results = list()

for i in range(2010,2014):
  results.append(YearResults(i))

for result in results:
  result.retrieve_data()
  result.parse()
  result.describe()
