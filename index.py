# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:58:28 2021

@author: Darlington
"""

import api_service
import config

def start():
    data = api_service.api_service(config.BASE_URL, config.endpoint, config.api_key, 
                config.symbols)
    print(data)
    
if __name__ == '__main__':
    start()




