from __future__ import division
import requests
import sys
import json
import pandas as pd
import numpy as np
import math

def getCityDistance():
	
	cityMatrix = np.zeros(shape=(5,5))
	columnNames = ['Caen', 'Paris', 'Marseille', 'Lyon', 'Lille']
	df = pd.DataFrame(cityMatrix, index=columnNames, columns=columnNames)
	for i in range (0,5):
		for j in range (0,5):
			req=requests.get ('https://maps.googleapis.com/maps/api/directions/json?origin='+str(df.columns.values[i])+'&destination='+str(df.columns.values[j])+'&key=AIzaSyAWelhRJMkKfVZee_EC-qz6GGQ-mipGy3M')
			feedbackJson = json.loads(req.content)
			df.iloc[i,j] = math.trunc(feedbackJson.get('routes')[0].get('legs')[0].get('distance').get('value')/1000)
			 
	return df
			
	
	

def main():
  print getCityDistance()


if __name__ == "__main__":
    main()



