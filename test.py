import requests


URL = "http://127.0.0.1:5000/"
                                        
# data = [
#     {"name": "bruce", "age": 20, "gender": "male"},
#     {"name": "martha", "age": 35, "gender": "female"},
#     {"name": "thomas", "age": 40, "gender": "male"}
# ]

# for i in range(len(data)):
#     put = requests.put(URL + "main/" + str(i), data[i])
#     print(put.json())

# input("\nPress enter\n")

get = requests.get(URL + "main/7")
print(get.json())

patch = requests.patch(URL + "main/2", {"gender": "male"})  # updating values accordinly
print(patch.json())