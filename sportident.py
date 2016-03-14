import pprint
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.OUT)
GPIO.setwarnings(False)
from lib_nrf24 import NRF24
import time
import sys
import sched, time
import spidev
import random
import math
from sireader import SIReader, SIReaderReadout, SIReaderControl
from time import sleep

pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

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

def Blink(numTimes,speed):
	GPIO.output(15,True)## Switch on pin 7
	time.sleep(speed)## Wait
	GPIO.output(15,False)## Switch off pin 7
	
# connect to station
si = SIReaderControl()
stationCode = si.station_code


print "RPi in forest - ready to send data"

try:
    while True:
       if sys.argv[1]!="demo":
		while not si.poll_punch():
			sleep(1);
    	
		strData = str(str(si._read_punch(si._next_offset-8)[0])+'|'+str(stationCode))
       else:
	strData = str(int(math.floor(random.random()*10000)))+"|45"
	time.sleep(5)

    	print "Incoming punching - Send to arena:"
    	print strData
        radio.write(list(strData))
        Blink(int(1),float(0.2))

        if radio.isAckPayloadAvailable():
            pl_buffer=[]
            radio.read(pl_buffer, radio.getDynamicPayloadSize())
            #print ("Received back:"),
            #print (pl_buffer)
        else:
            print ("Sent")
       
except KeyboardInterrupt:  
    # here you put any code you want to run before the program   
    # exits when you press CTRL+C  
    print "\n"        
finally:  
    GPIO.cleanup()
    print "cleanup"
