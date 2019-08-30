#!/usr/bin/python

############################################ 
# PROBLEM STATEMENT:
# This program will publish test mqtt messages using the AWS IOT hub
# 
# To test this program you have to run first its companinon aws_iot_sub.py
# that will subscribe and show all the messages sent by this program
#
############################################

############################################
# STEPS:
#
# 1. Sign in to AWS Amazon > Services > AWS IoT > Settings > copy Endpoint
#    This is your awshost
# 
# 2. Change following things in the below program:
#    a. awshost   (from step 1)
#    b. clientId  (Thing_Name)
#    c. thingName (Thing_Name)
#    d. caPath    (root-CA_certificate_Name)
#    e. certPath  (<Thing_Name>.cert.pem)
#    f. keyPath   (<Thing_Name>.private.key)
# 
# 3. Paste aws_iot_pub.py & aws_iot_sub.py python scripts in folder where all unzipped aws files are kept. 
# 4. Provide Executable permition for both the python scripts.
# 5. Run aws_iot_sub.py script
# 6. Run this aws_iot_pub.py python script
#
############################################

# importing libraries
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as paho
import os
import socket
import ssl
from random import uniform
 
connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a2dw4o069pca8w.iot.ap-south-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "raspberry"                                     # Thing_Name
thingName = "raspberry"                                    # Thing_Name
caPath = "root-CA.crt"                                      # Root_CA_Certificate_Name
certPath = "raspberry.cert.pem"                            # <Thing_Name>.cert.pem
keyPath = "raspberry.private.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop
 
GPIO.setmode(GPIO.BCM)

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# Pins connected to the HC-SR04 sensor
iTriggerPin = 21
iEchoPin    = 20

GPIO.setup(iTriggerPin, GPIO.OUT)
GPIO.setup(iEchoPin, GPIO.IN)

GPIO.output(iTriggerPin, False)
time.sleep(0.5)

while True:
	GPIO.output(iTriggerPin, True)
	time.sleep(0.0001)
	GPIO.output(iTriggerPin, False)

	while GPIO.input(iEchoPin) == 0:
		pass
	fPulseStart = time.time()

	while GPIO.input(iEchoPin) == 1:
		pass
	fPulseEnd = time.time()

	fPulseDuration = fPulseEnd - fPulseStart

	fDistance = round((fPulseDuration * 17150), 2)

	print ("Distance:", fDistance, "cm.")

	time.sleep(0.5)

GPIO.cleanup()
 
