import requests
import time
import os
import json


with open("property_list.txt", "r") as f:
    properties = f.read()

try:
    with open("house_data.json", "r") as f:
        past_data = json.load(f)
except:
    past_data = {}

properties = properties.split("\n")
api_key = os.getenv('DOMAINAPI')

headers = {
    'accept': 'application/json',
    'X-Api-Key': api_key
}

house_data = {}
for i in properties:
    url = f"https://api.domain.com.au/v1/listings/{i}"
    d = requests.get(url, headers=headers)
    p = d.json()
    # print(f"{i} - {p['status']}: {p['addressParts']['displayAddress']}, ({p['bedrooms']}, {p['bathrooms']}, {p['carspaces']}) - {p['priceDetails']['displayPrice']}")
    house_data[i] = p
    time.sleep(2)

with open('house_data.json', 'w') as f:
    json.dump(house_data, f)

diff_ids = []
for i in house_data.keys():
    if str(i) in past_data.keys():
        if past_data[str(i)]["dateUpdated"] != house_data[i]["dateUpdated"]:
            diff_ids.append(i)

check_keys = ['status', 'priceDetails']
for i in diff_ids:
    for j in check_keys:
        if past_data[i][j] != house_data[i][j]:
            print(f"{house_data[i]['addressParts']['displayAddress']} - changed: {j}, old value: {past_data[i][j]}, new value: {house_data[i][j]}")
