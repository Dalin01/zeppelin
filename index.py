# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:58:28 2021

@author: Darlington
"""

import api_service
from model.index import connect_to_DB, format_data, save
import json

def start():
    data = api_service.api_service()
    response = format_data(data)
    if ('payload' in response):
        save(response['payload'])
    else:
        print(response['error message'])

def create_DB_Tables():
    symbols = api_service.api_service()
    if symbols and symbols['success']:
        symbol_list = symbols['symbols'].keys()
        file = json.load(open('mock.json')).keys()
        if list(file) == list(symbol_list):
            connect_to_DB(symbol_list)

if __name__ == '__main__':
    start()
