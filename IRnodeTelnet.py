import telnetlib
import time
import datetime
import signal
import sys
import re

def signal_handler(signal, frame):
    print '> Closing TELNET connection...'
    session.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print ("Starting Client...")
#host    = input("Enter IP Address: ")
host = "10.231.21.100"
timeout = 10

samples = 1

print ("Connecting...")

try:
    session = telnetlib.Telnet(host, 23, timeout)
except socket.timeout:
    print ("socket timeout")
else:
    while True:
	
#	if samples > 1:
#		session = telnetlib.Telnet(host, 23, timeout)

	timestamp = datetime.datetime.now()

	session.write("@,g,e".encode('ascii'))
	output = session.read_eager()
#	print output

	irData = re.findall(r"[-+]?\d*\.\d+|\d+",output)
	
	if samples <= 2:
		print "> Aquiring Data..."
	else:
#		print irData
		ir2_raw = irData[0]
		ir2_float = float(ir2_raw)/10

		ir3_raw = irData[1]
		ir3_float = float(ir3_raw)/10

		outStr = "%s > IR2: %3.1f IR3: %3.1f\n" % (timestamp, ir2_float, ir3_float)
		
		print "[%d] %s > IR2: %3.1f IR3: %3.1f >> toLogFile.txt" % (samples, timestamp, ir2_float, ir3_float)
		
		file = open('optrisCT_arduNet_log.txt', 'a')
		file.write(outStr)
		file.close()

	samples += 1
#	session.close()
	if samples > 1:
		time.sleep(60)
	else:
		time.sleep(5)

session.close()
#time.sleep(1)
