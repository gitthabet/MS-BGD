###Cours live

requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=[your_api_key]&q=Toy+Story+3&page_limit=1')
req=requests.get('http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=[your_api_key]&q=Toy+Story+3&page_limit=1')
my_python_object = json.loads(req.text)
import json
my_python_object = json.loads(req.text)
len(my_python_object)
len(my_python_object['movies'])

