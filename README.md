# SmartPurpleAir
 This is a python script to trigger TP-Link devices based on a Purple Air Sensor's reading.  Coded to support Python3
 
## Getting Started (Setup)

- Install Python
- Install Dependencies:

`pip install requests`

`pip install uuid`

`pip install config parser`

- Define settings in config.ini

This program utilizes your TP-Link Kasa login information, as well as a specific Purple Air Sensor to function.  You will need to find your TP-Link login information and enter that into the `config.ini` file.  For the program to work, you will need:

- your TP-Link account username
- your TP-link account password
- the name of the TP-link device you want to control
- the sensor ID for a specific Purple Air Monitor

A sample `config_example.ini` has been created - copy it or create a new `config.ini` for your own config.

## Running the Script

The `aqi_trigger.py` file contains the example code to turn a specific TP-Link device on and off based on an AQI reading of greater than 30 for a specified purple air sensor.
For my use case, I've gone ahead and set this script up on a cloud server, and have used a cron job to run the script every 5 minutes.  If the AQI in my house goes above 30, a TP-Link plug will turn on.  This TP-Link plug is connected to a BlueAir 211 air purifier. 

```sh
python aqi_trigger.py
```

## Details

The script is useful for triggering TP-Link smart devices based on Purple Air sensor data.  If you have a sensor in your house, or close to your house, this will allow you to turn various things on or off.  I do not have any TP-Link Kasa lights, but you could easily modify the code to create your own "Real Time" AQI indicator in your house with a smart LED light.  I'm using in alongside my Purple Air monitor to improve the air qualiy in my house, based on specific events.

