import glob
import os
from time import sleep
import Adafruit_DHT
from datetime import datetime
import time
import ADS1263
import RPi.GPIO as GPIO


class DS18B20:

    def __init__(self):
        self.base_dir = "/sys/bus/w1/devices/"
        self.device_folder = glob.glob(base_dir + "28*")[0]
        self.device_file = device_folder + "/w1_slave"
        self._ok = os.path.exists(self.device_file)

    def sensor_ok(self):
        return  self._ok

    def read_temp(self):
        lines = self._read_temp_raw()
        status = lines[0].strip()[-3:]
        while status != "YES":
            print(status)
            sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string)/1000.0
            self._ok = True
            return temp_c
        else:
            self._ok = False
            return None

    def _read_temp_raw(self):
        f = open(self.device_file, "r")
        lines = f.readlines()
        f.close()
        return lines

class DHT22TemperatureHumiditySensor:
    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22
        #self.sensor = Adafruit_DHT.DHT11

    def read(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return (humidity, temperature)

class ADS1263ADC:
    def __init__(self, reference, channels):
        self.ADC = ADS1263.ADS1263()
        self.reference = reference
        self.channels = channels
    
    def read(self):
        # The faster the rate, the worse the stability
        # and the need to choose a suitable digital filter(REG_MODE1)
        if (ADC.ADS1263_init_ADC1('ADS1263_400SPS') == -1):
            exit()
        ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel

        # ADC.ADS1263_DAC_Test(1, 1)      # Open IN6
        # ADC.ADS1263_DAC_Test(0, 1)      # Open IN7
        
        channelList = [0, 1, 2, 3, 4]  # The channel must be less than 10
        while(1):
            ADC_Value = ADC.ADS1263_GetAll(channelList)    # get ADC1 value
            for i in channelList:
                if(ADC_Value[i]>>31 ==1):
                    print("ADC1 IN%d = -%lf" %(i, (REF*2 - ADC_Value[i] * REF / 0x80000000)))  
                else:
                    print("ADC1 IN%d = %lf" %(i, (ADC_Value[i] * REF / 0x7fffffff)))   # 32bit
            for i in channelList:
                print("\33[2A")
        
            print("\33[11A")

        ADC.ADS1263_Exit()

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

#ds18B20 = DS18B20()
dht22 =  DHT22TemperatureHumiditySensor(4)

for i in range(3):
    dht22.read()
temp, humid = dht22.read()
print( f"{datetime.now()} {temp:.1f} {humid:.1f}" )

