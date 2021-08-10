# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:41:52 2021

@author: Darlington
"""
import os

BASE_URL: str = 'http://api.exchangeratesapi.io/v1/'
endpoint: str = 'latest'
api_key: str = os.environ.get('API_KEY')
symbols: str = 'USD,AUD,CAD,PLN,MXN'
