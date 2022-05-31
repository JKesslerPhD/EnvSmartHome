import kasaAPI as kapi
import purpleair as pa
import configparser
import os

config = configparser.ConfigParser()
config.sections()

# Depending on how you run the script, you may need to specify the config.ini path location
config.read(os.path.join(os.path.dirname('__file__'), 'config.ini'))

# Depending on server implementation, you may need to hardcode your path. Eg:
#config.read('/home/jeffkessler/TPLink/config.ini')


# Load Relevant Settings
pa_indoor_id = config["PurpleAir"]["indoor_sensor"]
pa_outdoor_id = config["PurpleAir"]["outdoor_sensor"]
pa_key = config["PurpleAir"]["pa_key"]
username = config["Kasa"]["username"]
password = config["Kasa"]["password"]
blue_purifier = config["Kasa"]["device_one"]
carrier_purifier = config["Kasa"]["device_two"]



# Connect to your Kasa Account
c = kapi.TPLink(username, password)

# Select the device to be turned on/off
blue = c.findDevice(blue_purifier)
carrier = c.findDevice(carrier_purifier)

# Check a specific Purple Air sensor
indoor = pa.Monitor(pa_indoor_id, pa_key)
outdoor = pa.Monitor(pa_outdoor_id, pa_key)

#print("Sensor's Air Quality is {} (considered '{}')".format(m.aqi, m.status))

# Turn on or off smart switch based on AQI trigger
# This can also be set to a relevant status; e.g. != "Good"
# Check purpleair.py AQI class for status codes, or PrupleAir API docs

if indoor.aqi > 30:
    blue.TurnOn()

if indoor.aqi <= 15:
    blue.TurnOff()


# This enables the turn on and turnoff triggers for the Carier Air Purifier
if outdoor.status != "Good" or indoor.status != "Good":
    carrier.TurnOn()

# Will remain on until the air quality is exceptionally good indoors
if outdoor.status == "Good" and indoor.aqi <= 5:
    carrier.TurnOff()


# Triggers for Carbon Intensity
import colormap
from WattTimeAPI import California
from WattTimeAPI import WattTime

wt_user = config["WattTime"]["username"]
#wt_user = "kesslerj"  # For WattTimeAPI. jkessler for SGIP API
wt_password = config["WattTime"]["password"]
address = config["WattTime"]["address"]



# TP-Link Bulb named "CI Indicator"
bulb = c.findDevice("CI Indicator")

wt = California(wt_user, wt_password, address)
wt.setUtility("smud")

emissions = wt.get_emissions()


# Should make some modifications toa llow bulb to remain off/on
col = colormap.GenerateColor(emissions, 0, 100)
bulb.ChangeColor(col["hue"],col["saturation"],col["brightness"])
bulb.Brightness(10,1)
