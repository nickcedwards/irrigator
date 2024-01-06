from enum import Enum
import sqlite3


ADC_VREF = 4.79          # Read 4.9 on 2/10/23 (0V to 5V on pi header)
                         # fiddled to get the right answer
                         # external AVDD and AVSS(Default), or internal 2.5V

VBAT_ADC_CHANNEL = 0
# Should be 33k but when the battery voltage is 13V the SDC reads 2.7V (assuming 5.08 VREF)
VBAT_RLOW = 33_000
VBAT_RHIGH = 70_500

# This is the wPi GPIO number, not the BCM pin number as that is what ADAFuit uses
DHT22_GPIO = 4
# These are BCM pin numbers, because we're using the gpiozero library
PUMP_PIN = 20
VALVE_PIN = 21

DB = 'irrigator.db'
READINGS_TABLE = 'readings'

def get_cursor():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con.cursor()

class Frequencies(Enum):
    Off = "off"
    Once = "once"
    Daily = "daily"
    EveryTwoDays = "every2days"
    EveryThreeDays = "every3days"

class Actions(Enum):
    Nothing = "None"
    TurnOn = "TurnOn"
    TurnOff = "TurnOff"