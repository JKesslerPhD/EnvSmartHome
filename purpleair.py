import requests

class Monitor():
    def __init__(self, monitor_id):
        """
        

        Parameters
        ----------
        monitor_id : integer
            Will load the relevant purple air data for a specified Purple Air monitor id.
            The ID can be found from the purple air map

        Returns
        -------
        None.

        """
        self.monitor_id = monitor_id
        self.sensor_uptime = None
        self.pm25 = None
        self.aqi = None
        self.status = None
        
        self.update()

    def update(self):
        self.pm25 = self.getReading()
        a = AQI(self.pm25)
        self.aqi = a.aqi
        self.status = a.status
        return "{}(considered '{}')".format(self.aqi, self.status)
        
    def getReading(self):
        r = requests.get("https://www.purpleair.com/json?show={}".format(self.monitor_id))
        data = r.json()["results"][0]
        uptime = data["Uptime"]
        if uptime == self.sensor_uptime:
            return None
        else:
            self.sensor_uptime == uptime
        return float(data["PM2_5Value"])
        

class AQI():
    def __init__(self, pm):
        """
        

        Parameters
        ----------
        pm : float
            this is a PM2.5 reading from the relevant purple air sensor

        Returns
        -------
        None.

        """
        self.aqi = self.aqiFromPM(pm)
        self.status = self.getAQIDescription(self.aqi)
        
    
    def bplFromPM(self, pm):
        if (pm > 350.5):
            return 401
        elif (pm > 250.5):
            return 301
        elif (pm > 150.5):
            return 201
        elif (pm > 55.5):
            return 151
        elif (pm > 35.5):
            return 101
        elif (pm > 12.1):
            return 51
        elif (pm >= 0):
            return 0;
        else:
            return 0;
        

    def aqiFromPM(self, pm):
        """
        

        Parameters
        ----------
        pm : float
            This is the AQI formula found in the Purple Air API documentation

        Returns
        -------
        int
            The AQI value
        """
        if (pm > 350.5):
            return self.calcAQI(pm, 500, 401, 500, 350.5)
        elif (pm > 250.5):
            return self.calcAQI(pm, 400, 301, 350.4, 250.5)
        elif (pm > 150.5):
            return self.calcAQI(pm, 300, 201, 250.4, 150.5)
        elif (pm > 55.5):
            return self.calcAQI(pm, 200, 151, 150.4, 55.5)
        elif (pm > 35.5):
            return self.calcAQI(pm, 150, 101, 55.4, 35.5)
        elif (pm > 12.1):
            return self.calcAQI(pm, 100, 51, 35.4, 12.1)
        elif (pm >= 0):
            return self.calcAQI(pm, 50, 0, 12, 0)
        else:
            return None

 
    def calcAQI(self, Cp, Ih, Il, BPh, BPl):
        
        a = (Ih - Il);
        b = (BPh - BPl);
        c = (Cp - BPl);
        return round((a/b) * c + Il)
      

 
 
    def getAQIDescription(self, aqi):
        if (aqi >= 401):
            return 'Hazardous'
        elif (aqi >= 301):
            return 'Hazardous'
        elif (aqi >= 201):
            return 'Very Unhealthy'
        elif (aqi >= 151):
            return 'Unhealthy'
        elif (aqi >= 101):
            return 'Unhealthy for Sensitive Groups'
        elif (aqi >= 51):
            return 'Moderate'
        elif (aqi >= 0):
            return 'Good'
        else:
            return None

