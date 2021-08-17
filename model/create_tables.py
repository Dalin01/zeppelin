# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 18:49:29 2021

@author: HP
"""

def create_db_tables(symbol_list):    
    commands = [base_table(),rates_table(symbol_list, 'table')]

    return commands

def base_table():
    query = '''CREATE TABLE bases
            (base_id SERIAL PRIMARY KEY NOT NULL,
            timestamp VARCHAR(100) NOT NULL,
            base VARCHAR(100) NOT NULL,
            date DATE NOT NULL);'''
    return query

def rates_table(col, name):
    cols = ""
    for item, value in enumerate(col):
        if item < len(col) - 1:
            if value.lower() == "all":
                value = "albanianLek"
            cols += value + " NUMERIC, "
        else:
            cols += value + " NUMERIC"

    query = '''CREATE TABLE rates_'''+name+''' 
    (rate_id SERIAL PRIMARY KEY NOT NULL, base_id INT NOT NULL, 
     date_current DATE NOT NULL, ''' + cols + ''', 
     FOREIGN KEY (base_id) REFERENCES bases (base_id) ON DELETE CASCADE);'''

    return query
