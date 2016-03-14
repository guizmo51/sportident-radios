#!/usr/bin/python
from sireader import SIReader, SIReaderReadout, SIReaderControl
from lib_nrf24 import NRF24
import time
import threading
import RPi.GPIO as GPIO
import sys
import sched, time
import spidev
import random
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setwarnings(False)
si = []
siInstance = []
siStationCode = []


pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
global radio
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()


radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])


def send_data(data):
	radio.write(list(data))
	Blink(int(1),float(0.2))

def Blink(numTimes,speed):
	GPIO.output(15,True)## Switch on pin 7
	time.sleep(speed)## Wait
	GPIO.output(15,False)## Switch off pin 7

def listen_SI(si,radio):
	
	while True:
		time.sleep(1)
		punch = si.poll_punch()
		if (len(punch)>0):
			strData = str(str(punch[0][0])+'|'+str(si.get_station_code()))
			print(strData);
			send_data(strData)
		
def alive():
	while True:
		time.sleep(10)
		
		strData = str("alive|"+str(siInstance[0].get_station_code())+"")
		send_data(strData)

for i in range(0,4):
	try:
		si = SIReaderControl('',port='/dev/ttyUSB'+str(i)+'')
		siInstance.append(si)
		
	except: 
		pass
	


try:
	for y in siInstance:
		threading.Thread(None, listen_SI,None, (y,radio) ).start()
	threading.Thread(None, alive,None ).start()
	
	#radio.write(list(str("helloworld")))
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "\n"        








#threading.Thread(None, listen_SI,None, (siInstance[1],) ).start() 
