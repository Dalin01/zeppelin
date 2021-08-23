# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:58:28 2021

@author: Darlington
"""

import api_service
from model.index import connect_to_DB, format_data, save
from model.create_tables import create_db_tables
from config import dbConfig
import psycopg2
import json

def start():
    # create_DB_Tables()
    data = json.loads(api_service.api_service().content)
    if 'error' in data: # handle error
        print(data['error']['code'])
    else:
        response = format_data(data)
        if 'error' in response:
            print(response['error'])
        else:
            save(response['payload'])

    # if ('payload' in response):
    #     save(response['payload'])
    # else:
    #     print(response['error message'])

def create_DB_Tables():
    symbols = json.loads(api_service.api_service().content)
    if symbols and symbols['success']:
        symbol_list = symbols['symbols'].keys()
        commands = create_db_tables(symbol_list)
        conn = None
        try:
            params = dbConfig('db.ini', 'postgresql')
            conn = psycopg2.connect(**params)
            if conn:
                print('Database connection was successful')
            cursor = conn.cursor()  
            for command in commands:
                cursor.execute(command)
            print('Commands on database were successful')
            cursor.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

if __name__ == '__main__':
    start()
