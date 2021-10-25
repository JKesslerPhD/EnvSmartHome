#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import colormap
import kasaAPI as kapi
from WattTimeAPI import WattTime
from WattTimeAPI import California
import configparser
import os

config = configparser.ConfigParser()
config.sections()

# Depending on how you run the script, you may need to specify the config.ini path location
config.read(os.path.join(os.path.dirname('__file__'), 'config.ini'))


# Load Relevant Settings
username = config["Kasa"]["username"]
password = config["Kasa"]["password"] 

wt_user = config["WattTime"]["username"]
wt_password = config["WattTime"]["password"]
address = config["WattTime"]["address"]


c = kapi.TPLink(username, password)


bulb = c.findDevice("CI Indicator")


wt = California(wt_user, wt_password, address)
wt.setUtility("smud")


emissions = wt.get_emissions()

col = colormap.GenerateColor(emissions, 0, 100)
bulb.ChangeColor(col["hue"],col["saturation"],5, 1)
        