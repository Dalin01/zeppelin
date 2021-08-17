# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:28:01 2021

@author: Darlington
"""

import config
import requests

def api_service ():
    local_params = {}
    for key, value in config.params.items():
        if value != None:
            local_params[key] = value
    response = requests.get(config.BASE_URL + config.endpoint, params=local_params)
    if response:
        return response.json()
    else:
        return { 'error':'400', 'message': 'An error has occured.' }
    
    
    