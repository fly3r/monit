import time
import serial
import binascii
import datetime
import collections

bufferLenght = 60

ir0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ir1 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)

print "> Optris CT Sensor Ports IR[0:1]:"
print ir0.portstr
print ir1.portstr

sample = 0

ir0_cbuff = collections.deque(maxlen=bufferLenght)
ir1_cbuff = collections.deque(maxlen=bufferLenght)

timePast = time.time()

while True:
	timestamp = datetime.datetime.now()
	timeNow = time.time()

######################################################################################

	ir0.write(chr(0x01))
	ir0_raw = ir0.read(2)
	ir0_hex = binascii.hexlify(ir0_raw)
	ir0_C = (float((int(ir0_hex,16)-1000)/10.0)-32)*5/9

	ir0_cbuff.append(ir0_C)
	ir0_filtered = sum(ir0_cbuff)/bufferLenght

######################################################################################

	ir1.write(chr(0x01))
        ir1_raw = ir1.read(2)
        ir1_hex = binascii.hexlify(ir1_raw)
        ir1_C = (float((int(ir1_hex,16)-1000)/10.0)-32)*5/9

	ir1_cbuff.append(ir1_C)
	ir1_filtered = sum(ir1_cbuff)/bufferLenght

######################################################################################
	sample += 1

	if abs(timeNow-timePast) >= bufferLenght:
		timePast = timeNow
		if sample >= 60:
			outStr = "%s > IR0: %3.1f IR1: %3.1f\n" % (timestamp, ir0_filtered, ir1_filtered)
			file = open('optrisCT_log.txt', 'a')
			file.write(outStr)
			file.close()

			#print "[%d] %s > IR0: %3.1f IR1: %3.1f >> toLogFile.txt" % (count, timestamp, ir0_filtered, ir1_filtered)

			if (ir0_C >= (1.2*ir0_filtered) or ir1_C >= (1.2*ir1_filtered)):
		        	outStr = "%s > IR0: %3.1f [%3.1f] IR1: %3.1f [%3.1f]  >> RAW DATA - WARNING: TEMP RISING - << \n" % (timestamp, ir0_C, ir0_filtered, ir1_C, ir1_filtered)
        	        	print "[%d] %s > IR0: %3.1f [%3.1f] IR1: %3.1f [%3.1f] >> toEventsFile.txt >> RAW DATA - WARNING: TEMP RISING - << \n" % (sample, timestamp, ir0_C, ir0_filtered, ir1_C, ir1_filtered)

                		file = open('optrisCT_events.txt', 'a')
		                file.write(outStr)
		                file.close()
			else:
				print "[%d] %s > IR0: %3.1f IR1: %3.1f >> toLogFile.txt" % (sample, timestamp, ir0_filtered, ir1_filtered)

		#else:
			#print "[%d] [%2.0d] [IR0: %3.1f IR1: %3.1f] Aquiring Data... %d to go " % (count, abs(timeNow-timePast) ,ir0_C, ir1_C, bufferLenght-count)

	print "[sample: %d] [%02d] > IR0: %3.1f [%03.1f]  IR1: %3.1f [%03.1f]" % (sample, abs(timeNow-timePast) , ir0_C, abs((ir0_C-ir0_filtered)/ir0_filtered*100), ir1_C, abs((ir1_C-ir1_filtered)/ir1_filtered*100))

#	if (ir0_C >= (1.2*ir0_filtered) or ir1_C >= (1.2*ir1_filtered)):
#
#		outStr = "%s > IR0: %3.1f [%3.1f] IR1: %3.1f [%3.1f]  >> RAW DATA - WARNING: TEMP RISING - << \n" % (timestamp, ir0_C, ir0_filtered, ir1_C, ir1_filtered)
#		print "[%d] %s > IR0: %3.1f [%3.1f] IR1: %3.1f [%3.1f] >> toLogFile.txt >> RAW DATA - WARNING: TEMP RISING - << \n" % (count, timestamp, ir0_C, ir0_filtered, ir1_C, ir1_filtered)
#
#		file = open('eventsOptrisCT.txt', 'a')
#                file.write(outStr)
#                file.close()

	
	time.sleep(1)
