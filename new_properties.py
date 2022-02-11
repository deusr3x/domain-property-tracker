from urllib import request
import requests
import os
import json
import time

url = "https://api.domain.com.au/v1/listings/residential/_search"

api_key = os.getenv('DOMAINAPI')
headers = {
    'accept': 'application/json',
    'X-Api-Key': api_key
}

with open("suburb_list.txt", "r") as f:
    suburbs = f.read()


property_ids = set()
for i in suburbs:
    data = {
        "listingType": "Sale",
        "propertyTypes": ["House", "Villa", "Townhouse"],
        "propertyEstablishedType": "Any",
        "minBedrooms": 2,
        "maxBedrooms": 4,
        "locations": [
            {
                "state": "NSW",
                "suburb": i[0],
                "postCode": i[1],
                "includeSurroundingSuburbs": True,
            }
        ],
        "pageSize": 30,
    }
    d = requests.post(url, headers=headers, data=json.dumps(data))
    p = d.json()

    for j in p:
        listing_info = j["listing"]
        property_ids.add(listing_info["id"])
        details = listing_info['propertyDetails']
        print(f"{i[0]}: {details.get('displayableAddress', 'No Address')}, ({details.get('bedrooms', 0)}, {details.get('bathrooms', 0)}, {details.get('carspaces',0)}), {details.get('landArea', 0)}m^2 - {listing_info['priceDetails']['displayPrice']}")
    
    time.sleep(2)