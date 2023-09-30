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
divider = VoltageDivider(config.VBAT_R1, config.VBAT_R2)
temp_humidity = DHT22TemperatureHumiditySensor(config.DHT22_PIN)

vsense, vbat_raw = adc.read()
vbat = divider.voltage(vsense)

# First few readings always seem a bit off
for i in range(3):
    temp_humidity.read()
temp, humidity = temp_humidity.read()

time = datetime.datetime.now()

if args.verbose:
    print(f"{time} {vbat} V {temp}degC {humidity}%")

con = sqlite3.connect(config.DB)
cur = con.cursor()
cur.execute(f"INSERT INTO {config.READINGS_TABLE} VALUES ({time.isoformat()}, {temp}, {humidity}, {vbat_raw}, {vbat})")
con.commit()
con.close()


