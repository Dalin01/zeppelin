# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 18:04:53 2021

@author: HP
"""
import psycopg2
from config import dbConfig
from .create_tables import create_db_tables
import json

def database_connection(commands):
    conn = None
    try:
        params = dbConfig('db.ini', 'postgresql')
        conn = psycopg2.connect(**params)
        if conn:
            print('DATABASE CONNECTION SUCCESSFUL')
        cursor = conn.cursor()  
        for command in commands:
            cursor.execute(command)
        print('COMMANDS WERE SUCCESSFULLY')
        cursor.close()
        conn.commit()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def connect_to_DB(symbol_list):
    commands = create_db_tables(symbol_list)
    database_connection(commands)

def format_data(data):
    rates_table = []
    if data['success']:
        base_table = (data['timestamp'], data['base'], data['date'])
        if list(data['rates'].keys()) == list(json.load(open('mock.json')).keys()):
            rates_table = tuple(data['rates'].values())
            return {'payload': [rates_table, base_table]}
        else:
            return {'error message': 'Rates does not match the Database.'}

def save(data):
    rate_info = data[0]
    base_info = data[1]
    cols_array = ['base_id', 'date_current', *json.load(open('mock.json')).keys()]
    cols_array[4] = 'albanianLek'
    conn = None
    try:
        params = dbConfig('db.ini', 'postgresql')
        conn = psycopg2.connect(**params)
        if conn:
            print('DATABASE CONNECTION SUCCESSFUL')
        cursor = conn.cursor()

        insert_base = 'INSERT INTO bases (timestamp, base, date) VALUES (%s, %s, %s) RETURNING base_id;'
        cursor.execute(insert_base, base_info)
        base_id = cursor.fetchone()[0]

        if base_id:
            rate_info = tuple((base_id, base_info[2], *rate_info))
            temp = '('
            cols = '('
            for num in range(len(rate_info)):
                if num < len(rate_info) - 1:
                    temp += '%s,'
                    cols += cols_array[num] + ','
                else:
                    temp += '%s'
                    cols += cols_array[num]
            temp += ')'
            cols += ')'
            insert_rate = 'INSERT INTO rates_table '+cols+' VALUES' + temp +'RETURNING rate_id;'
            cursor.execute(insert_rate, rate_info)
            cursor.fetchone()[0]
            print('RATES HAS BEEN ADDED TO THE DATABASE.')

        cursor.close()
        conn.commit()
        return 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()