#!/usr/bin/python

from time import localtime, strftime
import time
import datetime
import sqlite3 as lite
import urllib2
import sched
import sys

class PeriodicScheduler(object):                                                
    def __init__(self):                                                         
        self.scheduler = sched.scheduler(time.time, time.sleep)                 
                                                                                
    def setup(self, interval, action, actionargs=()):                           
        action(*actionargs)                                                     
        self.scheduler.enter(interval, 1, self.setup,                           
                        (interval, action, actionargs))                         
                                                                                
    def run(self):                                                              
        self.scheduler.run()

#This is the event to execute every time
def periodic_event():
	con = lite.connect('temps.db')
	temp = int(urllib2.urlopen("http://192.168.75.20/temp").read())
	timestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
	
	with con:
		
		cur = con.cursor()    
		cur.execute("INSERT INTO sample VALUES('%(timestamp)s',%(temp)d)" % {"timestamp" : timestamp, "temp" : temp})
    
INTERVAL = 300 # every 5min
periodic_scheduler = PeriodicScheduler() 
periodic_scheduler.setup(INTERVAL, periodic_event) # it executes the event just once
periodic_scheduler.run() # it starts the scheduler
