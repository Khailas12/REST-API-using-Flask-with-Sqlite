import requests


URL = "http://127.0.0.1:5000/"

# # 'http://127.0.0.1:5000/helloworld/<string:name>/<int:age>' 
# get = requests.get(URL + "names/bruce/20")
# print(get.json())

get = requests.get(URL + "names/bruce")
print(get.json())