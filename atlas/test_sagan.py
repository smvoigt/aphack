#!/usr/bin/python3
# from ripe.atlas.sagan import Result

# # from test_costeau.py
# results = {'measurements': [23976423, 23976424]}


# file = open("../resources/test2.json", "r")
# data=file.readlines()
# file.close

import requests
from ripe.atlas.sagan import SslResult, PingResult

source = "https://atlas.ripe.net/api/v2/measurements/23976424/results/"
responses = requests.get(source).json()

# print(response)
print(type(responses))
print (len(responses))

for response in responses:
    print (response)
    