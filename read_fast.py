import datetime
from sensors import DHT22TemperatureHumiditySensor, ADS1263ADC, VoltageDivider
import config
import argparse
import sqlite3

parser = argparse.ArgumentParser(
                    prog='read_sensors',
                    description='Read temperature, humidity and 12V battery voltage',
                    )
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()


adc = ADS1263ADC(config.ADC_VREF, (config.VBAT_ADC_CHANNEL,))
divider = VoltageDivider(config.VBAT_RLOW, config.VBAT_RHIGH)

while 1:
    values = adc.read()
    vsense = values[0][0]
    vbat_raw  = values[0][1]
    vbat = divider.voltage(vsense)
    print(f"{vbat:.3f}")

