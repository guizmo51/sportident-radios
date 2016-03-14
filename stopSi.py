from sireader import SIReader, SIReaderReadout, SIReaderControl

for i in range(0,4):
	try:
		si = SIReaderControl('',port='/dev/ttyUSB'+str(i)+'')
		si.poweroff()
	except: 
		pass
