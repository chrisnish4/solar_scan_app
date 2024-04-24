import requests
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from config import API_KEY

def geocode(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    query = f"address={address}&key={API_KEY}"
    search_url = base_url + query

    response = requests.get(search_url)
    data = response.json()

    if data["status"] == "OK":
        coords = data['results'][0]['geometry']['location']
        lat, lon = coords['lat'], coords['lng']

        return lat, lon
    else:
        return "Invalid Address"