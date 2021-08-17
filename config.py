# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:41:52 2021

@author: Darlington
"""
import os
from configparser import ConfigParser

BASE_URL: str = 'http://api.exchangeratesapi.io/v1/'
endpoint: str = 'latest'
api_key: str = os.environ.get('API_KEY')

params = {
    'access_key': api_key,
    'base': 'EUR', # 'EUR' or None
    'symbols': None, # 'EUR,AUD,CAD,PLN,MXN' or None
    'from': None, # 'USD' or None
    'to': None, # 'EUR' or None
    'amount': None, # '25' or None
    'start_date': None, # 'YYYY-MM-DD' or None
    'end_date': None, # 'YYYY-MM-DD' or None
    }

def dbConfig(filename, section):
    parser = ConfigParser()
    parser.read(filename)
    dbConfig = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            dbConfig[param[0]] = param[1]
    else:
        print('Section {0} not found in the {1} file'.format(section, filename))
    return dbConfig

