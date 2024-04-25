import requests
import os
import sys
import hashlib
from google.cloud import storage
from exception import CustomException


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from api_key import API_KEY

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
    
def generate_hash(address):
    enc_data = address.encode('utf-8')
    hash_value = hashlib.sha256(enc_data).hexdigest()

    return hash_value

def get_img_temp_path(address):
    hash_value = generate_hash(address)
    lat, lon = geocode(address)

    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    query = f"?center={lat},{lon}&zoom=21&size=600x600&maptype=satellite&key={API_KEY}"
    search_url = base_url + query

    response = requests.get(search_url)

    if response.status_code == 200:
        os.makedirs('tmp', exist_ok=True)
        with open(f'tmp/{hash_value}.png', 'wb') as f:
            f.write(response.content)
           
        return f'tmp/{hash_value}.png'
 
def upload_gcs(bucket_name, source_file_path, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

def read_gcs(bucket_name, object_name, local_file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.download_to_filename(local_file_path)
