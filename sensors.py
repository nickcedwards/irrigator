import glob
import os
from time import sleep
import Adafruit_DHT
from datetime import datetime
import time
import waveshare.ADS1263 as ADS1263
import RPi.GPIO as GPIO

class DHT22TemperatureHumiditySensor:
    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22
        #self.sensor = Adafruit_DHT.DHT11

    def read(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return (temperature, humidity)

class ADS1263ADC:
    def __init__(self, reference, channels):
        self.reference = reference
        self.channels = channels

    def read(self):
        adc = ADS1263.ADS1263()
        adc.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel
        values = []
        # The faster the rate, the worse the stability
        # and the need to choose a suitable digital filter(REG_MODE1)
        if (adc.ADS1263_init_ADC2('ADS1263_ADC2_400SPS') != -1):
            ADC_Value = adc.ADS1263_GetAll_ADC2()
            for i, channel in enumerate(self.channels):
                if(ADC_Value[channel]>>23 ==1):
                    values.append( self.reference*2 - ADC_Value[i] * self.reference / 0x80000 )
                else:
                    values.append( ADC_Value[i] * self.reference / 0x7fffff )
        adc.ADS1263_Exit()
        return list(zip(values, ADC_Value))


class VoltageDivider:
    def __init__(self, rlow, rhigh):
        self.rlow = rlow
        self.rhigh = rhigh
    
    def voltage(self, vin):
        return vin * (self.rlow + self.rhigh)/self.rlow


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


if __name__ == "__main__":
    GPIO_PIN = 4
    dht22 =  DHT22TemperatureHumiditySensor(GPIO_PIN)

    for i in range(3):
        dht22.read()
    temp, humid = dht22.read()
    print( f"{datetime.now()} {temp:.1f} {humid:.1f}" )

