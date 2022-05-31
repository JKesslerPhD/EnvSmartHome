#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
import pytz
from datetime import datetime

class WattTime():
    def __init__(self, username, password, address):
        self.username = username
        self.password = password
        self.address = address
       
        self.token = None
        self.BA = None
        
        self._seturl()
    
    def _seturl(self):
        self._url = "https://api2.watttime.org/v2/"
        
    def register(self, email, org = "NA"):
        register_url = self._url+'register'
        params = {'username': self.username,
                 'password': self.password,
                 'email': email,
                 'org': org}
        rsp = requests.post(register_url, json=params)
        print(rsp.text)

    def get_token(self):
        if self.token:
            return self.token

        login_url = self._url+'login'
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
        
        region_url = self._url+'ba-from-loc'
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'latitude': lat, 'longitude': lon}
        rsp=requests.get(region_url, headers=headers, params=params)
        data = rsp.json()
        
        try:
            self.BA = data["abbrev"]
        except:
            raise Exception("A balancing authority could not be found for lat: {} lon: {}".format(lat, lon))
        return self.BA

        
    def get_emissions(self):
        if not self.BA:
            self.get_ba_from_loc()
        
        index_url = self._url+'index'
            
        

        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'ba': self.BA}
        rsp=requests.get(index_url, headers=headers, params=params)
        data = rsp.json()
        
        
        try:
            emissions = data["percent"]
        except:
            raise Exception("Invalid Balancing Authority Selected.")
            
        return int(float(emissions))
        
            
    
class California(WattTime):
    def _seturl(self):
        self._url = "https://sgipsignal.com/"
        
    def get_ba_from_loc(self, utility=None):
        if not self.token:
            self.get_token()
            
        try:
            self.setUtility(utility)
        except:
            raise Exception("A balancing authority could not be found for: {}. Please use setUtility()".format(utility))
        return self.BA
    
    def get_emissions(self):
        if not self.BA:
            self.get_ba_from_loc()
        
        index_url = self._url+'sgipmoer/'
            
    
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'ba': self.BA}
        rsp=requests.get(index_url, headers=headers, params=params)
        data = rsp.json()
        
        try:
            forecast = self.get_forecast()
            forecast.norm()
            percent = forecast.rank(data["moer"])

        except:
            raise Exception("Unable to make forecast with data")
            
        return int(float(percent))
   
    def get_forecast(self, hourly=False):
        if not self.BA:
            self.get_ba_from_loc()
            
        index_url = self._url+'sgipforecast/'
            
        tz = pytz.timezone("US/Pacific")
        
        date = datetime.now(tz=tz)
        day = date.isoformat()[0:10]
        
        forecast_day = day+"T00:00:00"

        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        params = {'ba': self.BA, "starttime":forecast_day, "endtime":forecast_day}
        rsp=requests.get(index_url, headers=headers, params=params)
        data = rsp.json()
        
        try:
            p = Predictions(data[0]["forecast"])
            return p
        except:
            raise Exception("Unable to generate forecast for {}".format(day))     
        
    
    def setUtility(self, name):
        if not self.token:
            self.get_token()
            
        utilities = {
        'Pacific Gas and Electric Company (PG&E)': 'SGIP_CAISO_PGE',
        'San Diego Gas & Electric (SDG&E)': 'SGIP_CAISO_SDGE',
        'Southern California Edison (SCE)': 'SGIP_CAISO_SCE',
        'Alameda Municipal Power': 'SGIP_CAISO_PGE',
        'Anza Electric Cooperative, Inc.': 'SGIP_CAISO_SCE',
        'Azusa Light and Water': 'SGIP_CAISO_SCE',
        'Bear Valley Electric Service (BVES)': 'SGIP_CAISO_SCE',
        'Biggs Municipal Utilities': 'SGIP_CAISO_PGE',
        'Burbank Water and Power': 'SGIP_LADWP',
        'CCSF, Power Enterprise of the San Francisco Public Utilities Commission': 'SGIP_CAISO_PGE',
        'City of Anaheim': 'SGIP_CAISO_SCE',
        'City of Banning': 'SGIP_CAISO_SCE',
        'City of Cerritos, Cerritos Electric Utility': 'SGIP_CAISO_SCE',
        'City of Corona, Department of Water and Power': 'SGIP_CAISO_SCE',
        'City of Healdsburg,  Electric Department': 'SGIP_CAISO_PGE',
        'City of Industry': 'SGIP_CAISO_SCE',
        'City of Lompoc, Electric Division': 'SGIP_CAISO_PGE',
        'City of Needles, Public Utility Authority': 'SGIP_WALC',
        'City of Palo Alto, Utilities Department': 'SGIP_CAISO_PGE',
        'City of Pittsburg, Pittsburg Power Company Island Energy': 'SGIP_CAISO_PGE',
        'City of Riverside, Public Utilities Department': 'SGIP_CAISO_SCE',
        'City of Shasta Lake': 'SGIP_BANC_P2',
        'City of Ukiah, Electric Utilities Division': 'SGIP_CAISO_PGE',
        'City of Vernon, Gas & Electric Department': 'SGIP_CAISO_SCE',
        'Colton Public Utilities': 'SGIP_CAISO_SCE',
        'Eastside Power Authority': 'SGIP_CAISO_SCE',
        'Glendale Water and Power': 'SGIP_LADWP',
        'Gridley Electric Utility': 'SGIP_CAISO_PGE',
        'Imperial Irrigation District (IID)': 'SGIP_IID',
        'Kirkwood Meadows Public Utility District': 'SGIP_CAISO_PGE',
        'Lassen Municipal Utility District': 'SGIP_CAISO_PGE',
        'Lathrop Irrigation District': 'SGIP_CAISO_PGE',
        'Liberty Utilities (a.k.a. CalPeco for California Pacific Electric Co.)': 'SGIP_NVENERGY',
        'Lodi Electric Utility': 'SGIP_CAISO_PGE',
        'Los Angeles Department of Water & Power (LADWP)': 'SGIP_LADWP',
        'Merced Irrigation District (MeID)': 'SGIP_TID',
        'Modesto Irrigation District (MID)': 'SGIP_BANC_P2',
        'PacifiCorp': 'SGIP_PACW',
        'Pasadena Water and Power': 'SGIP_CAISO_PGE',
        'Plumas-Sierra Rural Electric Cooperative': 'SGIP_CAISO_PGE',
        'Port of Oakland': 'SGIP_CAISO_PGE',
        'Port of Stockton': 'SGIP_CAISO_PGE',
        'Power and Water Resources Pooling Authority (PWRPA)': 'SGIP_CAISO_PGE',
        'Rancho Cucamonga Municipal Utility': 'SGIP_CAISO_SCE',
        'Redding Electric Utility': 'SGIP_BANC_P2',
        'Roseville Electric': 'SGIP_BANC_P2',
        'Sacramento Municipal Utility District (SMUD)': 'SGIP_BANC_SMUD',
        'Shelter Cove Resort Improvement District': 'SGIP_CAISO_PGE',
        'Silicon Valley Power (SVP), City of Santa Clara': 'SGIP_CAISO_PGE',
        'Surprise Valley Electrification Corporation': 'SGIP_PACW',
        'Trinity Public Utilities District (PUD)': 'SGIP_BANC_P2',
        'Truckee Donner Public Utilities District': 'SGIP_NVENERGY',
        'Turlock Irrigation District (TID)': 'SGIP_TID',
        'Victorville Municipal Utilities Services': 'SGIP_CAISO_SCE'}
        
        for utility, code in utilities.items():
            if name.lower() in utility.lower():
                self.BA = code

        if not self.BA:
            print("Utility could not be found.  Try one of these: %s" % utilities)
            return None
        
        return self.BA

class Predictions():
    def __init__(self, dictionary):
        """
        

        Parameters
        ----------
        dictionary : forecast dictionary from California.get_forecast(hourly=True)
            Will generate an object to get utilize hourly emission profiles

 
        """
        self.data = dictionary
        self.hourly = None
        self.min = None
        self.max = None
        self.avg = None
        self.scalar = None
        self._aggregate_time(self.data)
        
    
    def norm(self, lbound = 0, ubound = 100):
        if not isinstance(self.min,float) or not isinstance(self.max,float):
            raise Exception("Cannot normalize.  Emissions not loaded")
        self.scalar = (ubound - lbound)/(self.max-self.min)
        
        
    def rank(self, value):
        if not self.scalar:
            self.norm()
            print("Normalization not defined.  Defautling to scale of 0 to 100")
        percent = round((float(value)-self.min)*self.scalar,0)
        
        return percent
    
    def get_emissions(self,rank=True):
        times = {}
        for hour, emissions in self.hourly.items():
            avg = self.avg_emissions(hour)
            if rank:
                times[hour] = self.rank(avg)
            else:
                times[hour] = avg
        
        return times
            
        
    def avg_emissions(self, hour):
        """
        

        Parameters
        ----------
        hour : TYPE integer
            

        Returns
        -------
        TYPE
            Returns the emissions for a given hour

        """
        int(hour)
        
        if not self.hourly:
            self._aggregate_time(self.data)
            
            
        return sum(self.hourly[hour])/len(self.hourly[hour])
    
    def _aggregate_time(self, dictionary):
        from dateutil import parser
        aggregate = {}
        emissions = []
        for entry in dictionary:
            hour = parser.parse(entry["point_time"]).hour
            if hour not in aggregate:
                aggregate[hour] = []
            
            emissions.append(entry["value"])
            aggregate[hour].append(entry["value"])
            
        self.hourly = aggregate
        self.min = min(emissions)
        self.max = max(emissions)
        self.avg = sum(emissions)/len(emissions)
        
        return self.hourly
        
        


    
    