#!/usr/bin/python

# Dirty HOBUB clock
# =================
# This code triggers 3 analog gauges connected to the current output of 3 HOBUB PCBs with the pressure simulation telegram.
# ID001 = Hour, ID002 = Minute, ID003 = Second
#
# 2016-07-20 // 0.1 // mgo

import datetime
import time
import serial

pressureRangeHour = 10000
pressureRangeMinute = 10000
pressureRangeSecond = 10000

# To get the internal device name enter at console: python -m serial.tools.list_ports -v
ser = serial.Serial('/dev/cu.usbserial-FTZ5BROF')  # open serial port
print(ser.name) # check which port was really used

while (True):
    # Get local time from PC
    currentTime = datetime.datetime.now() # print("Local current time :", str(currentTime))

    # Assemble hour telegram for ID001:
    # Combine data for telegram
    stringHour = 'ID001,P=' + str(int(pressureRangeHour/24*currentTime.hour))
    # Calculate NMEA Ckecksum
    calcCksum = 0
    for s in stringHour:
        calcCksum ^= ord(s)
    # Combine final NMEA string
    stringNMEAhour = '$' + stringHour + '\r' + '\n' # + '*' + str(hex(calcCksum)[2:]) + '\r' + '\n'

    # Assemble minute telegram for ID002:
    # Combine data for telegram
    stringMinute = 'ID002,P=' + str(int(pressureRangeMinute/60*currentTime.minute))
    # Calculate NMEA Ckecksum
    calcCksum = 0
    for s in stringMinute:
        calcCksum ^= ord(s)
    # Combine final NMEA string
    stringNMEAminute = '$' + stringMinute + '\r' + '\n' # + '*' + str(hex(calcCksum)[2:]) + '\r' + '\n'

    # Assemble second telegram for ID003:
    # Combine data for telegram
    stringSecond = 'ID003,P=' + str(int(pressureRangeSecond/60*currentTime.second))
    # Calculate NMEA Ckecksum
    calcCksum = 0
    for s in stringSecond:
        calcCksum ^= ord(s)
    # Combine final NMEA string
    stringNMEAsecond = '$' + stringSecond + '\r' + '\n' # + '*' + str(hex(calcCksum)[2:]) + '\r' + '\n'

    print(stringNMEAhour.upper())
    print(stringNMEAminute.upper())
    print(stringNMEAsecond.upper())

    ser.write((stringNMEAhour.upper()).encode())
    time.sleep(0.3)
    ser.write((stringNMEAminute.upper()).encode())
    time.sleep(0.3)
    ser.write((stringNMEAsecond.upper()).encode())
    time.sleep(0.3)
