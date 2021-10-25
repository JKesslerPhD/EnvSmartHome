# Envrionmental Smart Home
 This repository contains a collection of python scripts that were coded to better integrate Kasa TP-Link devices with
 relevant environmental signals.  I anticipate inclusion of Nest thermostats in the near future.  Right now, I have Coded
 support for Purple Air sensors and carbon emission signals based on marginal grid emission signals from WattTime's API.  Coded to support Python3.


## Getting Started (Setup)

- Install Python
- Install Dependencies:

`pip install -r requirements.txt`

- Define settings in config.ini

This program utilizes your TP-Link Kasa login information, as well as a specific WattTime login information and Purple Air Sensor to function.  You will need to find your TP-Link login information and enter that into the `config.ini` file.  For the program to work, you will need:

- your TP-Link account username
- your TP-link account password
- the name of the TP-link device you want to control

For Purple Air monitor integration, you will need:

- the sensor ID for a specific Purple Air Monitor

For integrating the WattTime signal, you will need to:

- register a WattTime account.  You can do this using the WattTime functionality I have added

```from WattTimeAPI import WattTime
# If you are in California, use the higher-resolution CA signals
# from WattTimeAPI import California

wt_user = 'USER'
wt_password = 'PASSWORD'
address = 'Sacramento, CA 95814'

wt = WattTime(wt_user, wt_password, address)
wt.register('email@email_address.com')

```

A sample `config_example.ini` has been created - copy it or create a new `config.ini` for your own config.

## Running the Script

The `aqi_trigger.py` file contains the example code to turn a specific TP-Link device on and off based on an AQI reading of greater than 30 for a specified purple air sensor.  I have also bundled in some carbon intensity functionality into
this script example.

For my use case, I've gone ahead and set this script up on a cloud server, and have used a cron job to run the script every 5 minutes.  I am monitoring the AQI outside my house and inside of my house to control various air purifiers.  Additionally, I have setup a TP-Link bulb to change color based on the carbon intensity of the grid, so that I may choose to run various discretionary devices -- like washing machines, and dishwashers, etc.

```sh
python aqi_trigger.py
```

## Details

The script is useful for triggering TP-Link smart devices based on environmental data.  If you have a Purple Air sensor in your house, or close to your house, this will allow you to turn various things on or off.  I have added light bulb functionality and color changing baed on a Purple Air color range. You can use this, alongside Kasa color bulbs to create visual signals.
