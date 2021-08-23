# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 18:04:53 2021

@author: HP
"""
import psycopg2
from config import dbConfig, endpoint
from .create_tables import create_db_tables
import json
import datetime as dt

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
    if endpoint == 'convert':
        print('Convert endpoint is not considered. Do that using SQL.')
    elif endpoint == 'symbols':
        print('Symbols endpoint is not considered.')
    else:
        file = open('mock.json')
        if data['success'] and endpoint != 'timeseries':
            base_values = (data['timestamp'], data['base'], data['date'])
            if list(data['rates'].keys()) == list(json.load(file).keys()): # Ensure the cols are the same as with the DB.
                rates_values = tuple(data['rates'].values())
                return { 'payload': [rates_values, base_values] }
            else:
                print('The number of rate currencies does not match with the DB.')
            
        elif data['success'] and endpoint == 'timeseries':
            base = []
            rates = []            
            for key, value in data['rates'].items():
                base_value = (data['timestamp'], data['base'], key)
                if list(value.keys()) == list(json.load(file).keys()): # Ensure the cols are the same as with the DB.
                    rates_values = tuple(value.values())
                    base.append(base_value)
                    rates.append(rates_values)
                else:
                    print('The number of rate currencies does not match with the DB at '+str(key))
            return { 'payload': [rates, base] }
        file.close()
    return { 'error': 'An error occured. Please try again.'}

def save(data):
    rate_info = data[0]
    base_info = data[1]
    # Get the col headers for the rate table 
    file = open('mock.json')
    cols_array = ['base', *json.load(file).keys()]
    file.close()
    cols_array[3] = 'albanianLek' # replace all with this
    conn = None
    try:
        params = dbConfig('db.ini', 'postgresql')
        conn = psycopg2.connect(**params)
        if conn:
            print('Database connection was successful')
        cursor = conn.cursor()

        base_id = -1
        if isinstance(base_info, tuple): # latest or historical 
            result = None
            select_base = 'SELECT * FROM bases WHERE base_date = %s;'
            date = dt.date(int(base_info[2].split('-')[0]),
                           int(base_info[2].split('-')[1]),
                           int(base_info[2].split('-')[2]))
            cursor.execute(select_base, (date,))

            result = cursor.fetchone()
            if result == None: # new record
                insert_base = '''
                    INSERT INTO bases (time_stamp, base, base_date)
                    VALUES (%s, %s, %s) RETURNING id;
                '''
                cursor.execute(insert_base, base_info)
                base_id = cursor.fetchone()[0]
                if base_id != -1:
                    rate_info = tuple((base_id, *rate_info))
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
                    
                    insert_rate = 'INSERT INTO rates {} VALUES {};'.format(cols, temp)
                    cursor.execute(insert_rate, rate_info)
                    print('New rate has been added to the Database')
            else: # updating
                base_id = result[0]
                temp = '('
                cols = '('
                cols_array = cols_array[1:]                
                for num in range(len(rate_info)):
                    if num < len(rate_info) - 1:
                        temp += '%s,'
                        cols += cols_array[num] + ','
                    else:
                        temp += '%s'
                        cols += cols_array[num]
                temp += ')'
                cols += ')'
                update_base = '''
                    UPDATE rates SET {} = {}
                    WHERE base = {};
                '''.format(cols, temp, base_id)
                print(update_base, rate_info)
                cursor.execute(update_base, rate_info)
                print('Record has been updated')
        
        cursor.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()