from __future__ import print_function
import qwiic_ccs811
import qwiic_bme280
import time
import sys
from tmp102 import TMP102
import serial
import datetime
import requests
import smbus

from postRequest import *
from initData import *

########################### PM ####################################
def readIndex(bus, index):
    try:
        block = bus.read_i2c_block_data(0x12, 0, 32)
        highindex = index
        lowindex = highindex+1
        data = block[highindex]*256 + block[lowindex] 
        return data
    except IOError:
        return {'pm1.0': 11 , 'pm2.5': 18, 'pm10': 18 }
    
    
def readFromPM(bus):
    
    pm1_0 = readIndex(bus, 4)
    pm2_5 = readIndex(bus, 6)
    pm10 = readIndex(bus, 8)
    return {'pm1.0': pm1_0 , 'pm2.5': pm2_5, 'pm10': pm10 }
    


def checkSensor(mySensor) :
    if mySensor.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

def readFromMPL(bus):
    data = bus.read_i2c_block_data(0x60, 0x00, 6)
    tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
    altitude = tHeight / 16.0
    cTemp = temp / 16.0
    pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
    pressure = (pres / 4.0) / 1000.0
    return {'temperature': cTemp, 'altitude': altitude, 'pressure': pressure}

def readFromHIH(bus):
    data = bus.read_i2c_block_data(0x27, 0x00, 4)
    humidity = ((((data[0] & 0x3F) * 256) + data[1]) * 100.0) / 16383.0
    temp = (((data[2] & 0xFF) * 256) + (data[3] & 0xFC)) / 4
    cTemp = (temp / 16384.0) * 165.0 - 40.0
    return {'temperature': cTemp, 'humidity': humidity}

def readFromMS(bus):
    data = bus.read_i2c_block_data(0x77, 0xA2, 2)
    C1 = data[0] * 256 + data[1]

    # Read pressure offset
    data = bus.read_i2c_block_data(0x77, 0xA4, 2)
    C2 = data[0] * 256 + data[1]

    # Read temperature coefficient of pressure sensitivity
    data = bus.read_i2c_block_data(0x77, 0xA6, 2)
    C3 = data[0] * 256 + data[1]

    # Read temperature coefficient of pressure offset
    data = bus.read_i2c_block_data(0x77, 0xA8, 2)
    C4 = data[0] * 256 + data[1]

    # Read reference temperature
    data = bus.read_i2c_block_data(0x77, 0xAA, 2)
    C5 = data[0] * 256 + data[1]

    # Read temperature coefficient of the temperature
    data = bus.read_i2c_block_data(0x77, 0xAC, 2)
    C6 = data[0] * 256 + data[1]

    # MS5803_14BA address, 0x77(119)
    #       0x40(64)    Pressure conversion(OSR = 256) command
    bus.write_byte(0x77, 0x40)

    time.sleep(0.5)
.sleep(delay)
    # Read digital pressure value
    # Read data back from 0x00(0), 3 bytes
    # D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(0x77, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]

    # MS5803_14BA address, 0x77(119)
    #       0x50(64)    Temperature conversion(OSR = 256) command
    bus.write_byte(0x77, 0x50)

    time.sleep(0.5)

    # Read digital temperature value
    # Read data back from 0x00(0), 3 bytes
    # D2 MSB2, D2 MSB1, D2 LSB
    value = bus.read_i2c_block_data(0x77, 0x00, 3)
    D2 = value[0] * 65536 + val.sleep(delay)ue[1] * 256 + value[2]

    dT = D2 - C5 * 256
    TEMP = 2000 + dT * C6 / 8388608
    OFF = C2 * 65536 + (C4 * dT) / 128
    SENS = C1 * 32768 + (C3 * dT ) / 256
    T2 = 0
    OFF2 = 0
    SENS2 = 0

    if TEMP > 2000 :
        T2 = 7 * (dT * dT)/ 137438953472
        OFF2 = ((TEMP - 2000) * (TEMP - 2000)) / 16
        SENS2= 0
    elif TEMP < 2000 :
        T2 = 3 * (dT * dT) / 8589934592
        OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        if TEMP < -1500:
            OFF2 = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
            SENS2 = SENS2 + 4 * ((TEMP + 1500) * (TEMP + 1500))

    TEMP = TEMP - T2
    OFF = OFF - OFF2
    SENS = SENS - SENS2
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
    cTemp = TEMP / 100.0.sleep(delay)

    return {'temperature': cTemp, 'pressure':pressure}

def run():
    #BME280
    mySensor280 = qwiic_bme280.QwiicBme280()
    checkSensor(mySensor280)
    mySensor280.begin()

    #CS811 falla lectura
    #mySensorCS811 = qwiic_ccs811.QwiicCcs811()
    #checkSensor(mySensorCS811)
    #mySensorCS811.begin()

    #TMP102
    tmp = TMP102('C', 0x48, 1)

    bus = smbus.SMBus(1)
    #MPL
    initMPL(bus)

    #HIH
    initHIH(bus)

    #MS
    initMS(bus)

    #ADPS
    #lux = adps9300()


    while True:
#       mySensorCS811.real_algorithm_results()
        print("Reading Data...")
        mpl = readFromMPL(bus)
        hih = readFromHIH(bus)
        ms = readFromMS(bus)
        pm = readFromPM(bus)
        data = {
            'dateObserved': {
                'type': 'Text',
                'value': datenow()
            },
            'humidity':{
                'type': 'Float',
                'value': mySensor280.humidity
            },
            'pressure':{
                'type': 'Float',
                'value':mySensor280.pressure
            },
            'altitude':{
                'type': 'Float',
                'value': mySensor280.altitude_feet
            },
            'temperature2':{
                'type': 'Float',
                'value': mySensor280.temperature_celsius
            },
            #'co2':{
             #   'type': 'Float',
              #  'value': #mySensorCS811.CO2
            #},
            #'tvoc':{
             #   'type': 'Float',
             #   'value': #mySe.sleep(delay)nsorCS811.TVOC
            #},
            'temperature':{
                'type': 'Float',
                'value': tmp.readTemperature()
            },
            'tempMPL':{
                'type': 'Float',
                'value': mpl['temperature']
            },
            'altitudeMPL':{
                'type': 'Float',
                'value': mpl['altitude']
            },
            'pressureMPL':{
                'type': 'Float',
                'value': mpl['pressure']
            },
            'tempHIH':{
                'type': 'Float',
                'value': hih['temperature']
            },
            'humidityHIH':{
                'type': 'Float',
                'value': hih['humidity']
            },
            'tempMS':{
                'type': 'Float',
                'value': ms['temperature']
            },
            'pressureMS':{
                'type': 'Float',
                'value': ms['pressure']
            },
            #'luminosity':{
             #   'type': 'Float',
              #  'value': lux.read_lux()
            #},
            'pm1.0':{
                'type': 'Float',
                'value': pm['pm1.0']
            },
            'pm2.5':{
                'type': 'Float',
                'value': pm['pm2.5']
            },
            'pm10':{
                'type': 'Float',
                'value': pm['pm10']
            }
            
        }
        print(data)
#        post(data)
        time.sleep(delay)


if __name__ == '__main__':
    try:
        run()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding...")
        sys.exit(0)

