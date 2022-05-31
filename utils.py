#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:26:31 2022

@author: jeffkessler
"""
import datetime
import pytz

class AlarmTime():
    def __init__(self, start=7, end=22):
        self.start = datetime.time(start-1,59,59,9999)
        self.end = datetime.time(end-1,59,59,9999)
    
    def _now(self):
        pst = pytz.timezone('America/Los_Angeles')
        return datetime.datetime.now(pst).time()
        

    def is_active(self):
        now = self._now()
        if self.start <= now <= self.end:
            return True
        else:
            return False
    