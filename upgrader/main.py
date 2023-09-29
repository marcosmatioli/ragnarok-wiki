#!/bin/python

import requests
import time
import logging
import pymongo
import os

# start variables
log_level=os.environ['LOG_LEVEL']
api_key=os.environ['API_KEY']
mongodb_url=os.environ['MONGODB_URL']

# set log configuration
log_format = '%(asctime)s - %(levelname)s - %(message)s'

log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

if log_level in log_levels:
    log_level = log_levels[log_level]
    logging.basicConfig(format=log_format, level=log_level)

else:
    raise ValueError('LOG_LEVEL ({LOG_LEVEL}) environment variable invalid')

# mongodb connection
mongo_client = pymongo.MongoClient(mongodb_url)
db = mongo_client["ragnarok"]
collection = db["monsters"]
status = db["status"]

# position
position = status.find_one({'status': 'id'})['id']

def save_status(position):
    status.update_one(
        { 'status': 'id' },
        { '$set': { 'id': position } },
        upsert=True
    )

# upgrade ragnarok db
while True:
    for n in range(position, 50000):
        url = f"https://www.divine-pride.net/api/database/Monster/{n}?apiKey={api_key}"
        cabecalhos = {'Accept-Language': 'pt-BR'}

        while True:
            response = requests.get(url, headers=cabecalhos)

            logging.debug(f'{response.content}')

            if response.status_code == 200:
                data = response.json()
                if data['name'] not in ('', None, 'null'):
                    
                    collection.update_one(
                        { 'id': data['id'] },
                        { '$set': data },
                        upsert=True
                    )

                    logging.info(f'id {data["id"]} add/update to db')
                    time.sleep(1)
                
                break

            elif response.status_code == 403:
                logging.error(f'id {data["id"]} with status code 403')
                time.sleep(3600)
            
            else:
                logging.warning(f'id {n} with status code {response.status_code}')
                time.sleep(1)
                break

        save_status(n)
    position = 1001
