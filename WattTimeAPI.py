#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import urllib.parse

class WattTime():
    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.address = address
        self.token = None
        self.BA = None
    
    def register(self, email, org = "NA"):
        register_url = 'https://api2.watttime.org/v2/register'
        params = {'username': self.username,
                 'password': self.password,
                 'email': email,
                 'org': org}
        rsp = requests.post(register_url, json=params)
        print(rsp.text)

    def get_token(self):
        if self.token:
            return self.token

        login_url = 'https://api2.watttime.org/v2/login'
        rsp = requests.get(login_url, auth=HTTPBasicAuth(self.username, self.password))
        try:
            data = rsp.json()
            self.token = data["token"]
        except:
            raise Exception("There was an error logging in to the server. Please register a new account first.")
        return self.token
    
    def get_lat_from_address(self, address):
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
        
        response = requests.get(url).json()
        
        try:
            lat = response[0]["lat"]
            lon = response[0]["lon"]
        except:
            raise Exception("The entered address was not valid.")
    
        return (lat, lon)

    def get_ba_from_loc(self):
        if not self.token:
            self.get_token()
            
        lat, lon = self.get_lat_from_address(self.address)
        
        region_url = 'https://api2.watttime.org/v2/ba-from-loc'
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'latitude': lat, 'longitude': lon}
        rsp=requests.get(region_url, headers=headers, params=params)
        data = rsp.json()
        
        try:
            self.BA = data["abbrev"]
        except:
            raise Exception("A balancin authority could not be found for lat: {} lon: {}".format(lat, lon))
        return self.BA
    
    def get_emissions(self):
        if not self.BA:
            self.get_ba_from_loc()
        
        index_url = 'https://api2.watttime.org/index'
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'ba': self.BA}
        rsp=requests.get(index_url, headers=headers, params=params)
        data = rsp.json()
        print(rsp.text)
        return int(data["percent"])