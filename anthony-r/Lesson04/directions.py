import urllib2
import requests
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

token = "AIzaSyDfZBf9UvJyjQfN_Jau0LS96en9e4JISPo"
api_root_url = "https://maps.googleapis.com/maps/api/directions/json?"

def generate_params(origin,destination,key):
    return "origin="+origin+"&destination="+destination+"&key="+token

class Distance:
    def __init__(self,origin,destination):
        self.origin =  origin
        self.destination = destination
        self.data = None
        self.distance = 0

    def get_data(self):
        self.data = requests.get(api_root_url+generate_params(self.origin,self.destination,token)).json()

    def calculate_distance(self):
        for route in self.data['routes']:
            for leg in route['legs']:
                self.distance += int(leg['distance']['value'])

    def get_distance(self):
        return self.distance


class Distances:
    def __init__(self,cities):
        self.values = list()
        for city in cities:
            for city2 in cities:
                self.values.append(Distance(city,city2))

    def load_values(self):
        for val in self.values:
            val.get_data()
            val.calculate_distance()

    def output(self):
        out = list()
        for val in self.values:
            out.append(val.get_distance())
        return out

cities = ["Paris", "Caen", "Marseille", "Lyon", "Lille"]

distances = Distances(cities)
distances.load_values()
mat = distances.output()

distance_matrix = np.array(mat)
distance_matrix = np.reshape(distance_matrix,(len(cities),len(cities)))

plt.matshow(distance_matrix)
plt.show()
