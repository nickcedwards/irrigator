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
temp_humidity = DHT22TemperatureHumiditySensor(config.DHT22_PIN)

values = adc.read()
vsense = values[0][0]
vbat_raw  = values[0][1]
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
insert_sql = f"INSERT INTO {config.READINGS_TABLE} VALUES (\"{time}\", {temp}, {humidity}, {vbat_raw}, {vbat})"
if args.verbose:
    print(insert_sql)
cur.execute(insert_sql)
con.commit()
con.close()


