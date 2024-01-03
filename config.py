
ADC_VREF = 4.79          # Read 4.9 on 2/10/23 (0V to 5V on pi header)
                         # fiddled to get the right answer
                         # external AVDD and AVSS(Default), or internal 2.5V

VBAT_ADC_CHANNEL = 0
# Should be 33k but when the battery voltage is 13V the SDC reads 2.7V (assuming 5.08 VREF)
VBAT_RLOW = 33_000
VBAT_RHIGH = 70_500

DHT22_PIN = 4

DB = 'irrigator.db'
READINGS_TABLE = 'readings'

