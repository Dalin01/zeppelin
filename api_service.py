# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:28:01 2021

@author: Darlington
"""

import config
import requests

def api_service ():
    parameter = {}
    # Extract relevant parameters for querying the API
    for key, value in config.params.items():
        if value != None:
            parameter[key] = value
    
    # GET /baseURL/endpoint/parameters
    response = {}
    try:
        response = requests.get(config.BASE_URL + config.endpoint, params=parameter)
    except requests.exceptions.RequestException as error:
        raise SystemExit(error)
    return response
    
    
    