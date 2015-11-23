### IMPORTS ###################################################

from stravalib import Client
import logging
import time
import serial
import struct
import random

### LOGGING AND SERIAL SETUP ###################################################

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='stravaExploration.log',
                    filemode='w')
logging.debug('A debug message')
#logging.info('Some information')
logging.warning('A shot across the bows')

try:
	ser = serial.Serial('/dev/cu.usbmodem14211', 9600)
	time.sleep(2)
	print "Connection to " + ser + " established succesfully!\n"
except Exception as e:
	print(e)

### API KEYS AND SHIT ###################################################

### eventually get this to work w/ other athelete's activities 

STRAVA_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxx'  ## i think this is just the public facing API so I can only use my own stuff
client = Client(access_token=STRAVA_ACCESS_TOKEN)
athleteID = [1818295]

### FUNCTIONS ###################################################

def getSpeeds(cIDs):

	### still not using the athlete ID

	allaIDS = []
	activities = client.get_activities(limit=100)
	
	for i in activities:
		if i.manual == False:
			allaIDS.append(i.id)

	aIDs = random.sample(allaIDS,2)
	
	streamsDicts = []
	streamsFinal = []

	for i in aIDs:
		types = ['velocity_smooth']
		streams = client.get_activity_streams(i, types=types, resolution='low')
		activity = client.get_activity(i)	
		if 'velocity_smooth' in streams.keys():
			actName = activity.name 
			raw = streams['velocity_smooth'].data
			streamsDicts.append({actName:raw[1:]})	
		else: 
			print "velocity_smooth is not available"
	
	### possible to do this w/ list comprehension? 
	for i in streamsDicts:
		for key, value in i.iteritems():
			value = [round((x * 3600) / 1000,0) for x in value]
			streamsFinal.append({key:value})
			
	printInterval(streamsFinal)

def printInterval(streamsFinal):
	#print streamsFinal
	speedComapre = [] ### this needs to be extended for more than 2
	titles = []
	dingMin = 21 #km per hour

	for i in streamsFinal:
		#print i
		for key, value in i.iteritems():
			#print key
			#print value
			titles.append(key)
			speedComapre.append(value)
	#print("{} vs {}".format(titles[0],titles[1]))
	#print titles
	for x in titles:
		print("{} / ".format(x)),

	finalSpeeds = zip(*speedComapre)  ### http://stackoverflow.com/questions/4112265/how-to-zip-lists-in-a-list
	time.sleep(1)

	for i in finalSpeeds:
		print i
		time.sleep(2)
		for x in i:
			if x >= dingMin:
				print("{}-{}".format(i.index(x),int(x)))
				pin = int(i.index(x))  # will either be a 0, 1, 2, 3...etc.
				ser.write(struct.pack('>B', pin))
				#print pin

### CALL IT ###################################################

getSpeeds(athleteID)
