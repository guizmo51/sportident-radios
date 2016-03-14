from sireader import SIReader, SIReaderReadout, SIReaderControl
# connect to station
import time
si = SIReaderControl('',port='/dev/ttyUSB0')
print(si.get_station_code())
while True:
    time.sleep(1)
    punch = si.poll_punch()
    
    if (len(punch)>0):
        print punch[0][0]

    
    

