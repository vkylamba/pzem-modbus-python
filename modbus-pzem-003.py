#!/usr/bin/env python3
import serial
import minimalmodbus


### Modbus addresses
### Datasheet: https://solar-thailand.com/pdf/PZEM-003-Manual.pdf
"""
    RegAddr Description                 Resolution
    0x0000  Voltage value               1LSB correspond to 0.1V
    0x0001  Current value               1LSB correspond to 0.1A
    0x0002  Power value low 16 bits     1LSB correspond to 0.1W
    0x0003  Power value high 16 bits
    0x0004  Energy value low 16 bits    1LSB correspond to 1Wh
    0x0005  Energy value high 16 bits
    0x0006  High voltage alarm status   0xFFFF is alarm 0x0000 is not alarm
    0x0007  Low voltage alarm status   0xFFFF is alarm 0x0000 is not alarm
"""

ADDR_VOLTAGE                   = 0x0000
ADDR_CURRENT                   = 0x0001
ADDR_POWER                     = 0x0002
ADDR_ENERGY                    = 0x0004
ADDR_HIGH_VOLTAGE_ALARM_STATUS = 0x0006
ADDR_LOW_VOLTAGE_ALARM_STATUS  = 0x0007

SALVE_ADDRESS = 0x01
SALVE_ADDRESS_CALIBRATION = 0xF8

instrument = minimalmodbus.Instrument('/dev/tty.usbserial-120', SALVE_ADDRESS)  # port name, slave address

# set comm params
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 2
instrument.serial.timeout  = 0.5 # seconds


def read_voltage():
    ## Read voltage 
    value = instrument.read_register(
        ADDR_VOLTAGE, 1,
        functioncode=0x04
    )
    return round(value / 10, 2)

def read_current():
    ## Read current 
    value = instrument.read_register(
        ADDR_CURRENT, 1,
        functioncode=0x04
    )
    return round(value / 10, 3)

def read_power():
    ## Read power 
    value = instrument.read_register(
        ADDR_POWER, 2,
        functioncode=0x04
    )
    return round(value, 2)

def read_energy():
    ## Read energy 
    value = instrument.read_register(
        ADDR_ENERGY, 2,
        functioncode=0x04
    )
    return round(value, 2)


voltage = read_voltage()
current = read_current()
power = read_power()
energy = read_energy()
print(f"Voltage: {voltage} V")
print(f"Current: {current} A")
print(f"Power: {power} W")
print(f"Energy: {energy} WH")