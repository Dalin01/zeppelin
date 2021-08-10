# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:28:01 2021

@author: Darlington
"""

import requests

def api_service (url: str, endpoint: str, key: str, symbols: str):
    response = requests.get(url + endpoint, params={'access_key': key, 'symbols': symbols})
    if response:
        return response.json()
    else:
        return {'error':'400', 'message': 'An error has occured.'}
    
    
    