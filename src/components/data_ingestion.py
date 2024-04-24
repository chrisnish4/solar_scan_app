import os
import sys
import json
import requests
from google.cloud import storage

sys.path.append('/Users/chrisnishimura/Documents/Personal_Projects/solar_scan/src')
from exception import CustomException
from logger import logging
from utils import *
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    tmp_img_path: str = os.path.join('tmp', 'location.png')

class DataIngestion:
    def __init__(self, address):
        self.ingestion_config = DataIngestionConfig()
        self.address = address

    def initiate_data_ingestion(self):
        print('log info should be logged')
        address = self.address
        logging.info('Entered the data ingestion method or component')

        try:
            hash_addr_path = 'hashed_address.json'
            if not os.path.exists(hash_addr_path):
                with open(hash_addr_path, 'w') as f:
                    json.dump(dict(), f)
                logging.info('Created hashed_address.json')

            with open(hash_addr_path, 'r') as f:
                json_data = json.load(f)
            
            os.makedirs('tmp', exist_ok=True)

            if address in json_data.keys():
                logging.info('Address previously queried')
                hash_value = json_data[address]
                obj_name = f'{hash_value}.png'
                local_path = self.ingestion_config.tmp_img_path
                
                read_gcs('ind_uploads', obj_name, local_path)
                logging.info('Image successfully retrieved')

            else:
                logging.info('Address not found, adding to logs')
                hash_value = generate_hash(address)
                json_data[address] = hash_value

                with open(hash_addr_path, 'w') as f:
                    json.dump(json_data, f)
                logging.info('Address successfully added to logs')

                img_tmp_path = get_img_temp_path(address)
                file_hash_name = img_tmp_path.split('/')[1]
                upload_gcs('ind_uploads', img_tmp_path, file_hash_name)
                logging.info('Image successfully uploaded to GCP')


        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataIngestion('376 Utica Ln, San Jose, CA')
    obj.initiate_data_ingestion()