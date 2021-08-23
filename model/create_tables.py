# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 18:49:29 2021

@author: HP
"""

def create_db_tables(symbol_list):    
    commands = [base_table(), rates_table(symbol_list)]
    return commands

def base_table():
    query = '''CREATE TABLE bases
            (id SERIAL PRIMARY KEY NOT NULL,
            time_stamp VARCHAR(100) NOT NULL,
            base VARCHAR(100) NOT NULL,
            base_date DATE NOT NULL);'''
    return query

def rates_table(col):
    cols = ""
    for item, value in enumerate(col):
        if item < len(col) - 1:
            if value.lower() == "all":
                value = "albanianLek"
            cols += value + " NUMERIC, "
        else:
            cols += value + " NUMERIC"

    query = '''CREATE TABLE rates (id SERIAL PRIMARY KEY NOT NULL, base INT NOT NULL, 
     ''' + cols + ''', 
     FOREIGN KEY (base) REFERENCES bases (id) ON DELETE CASCADE);'''

    return query
