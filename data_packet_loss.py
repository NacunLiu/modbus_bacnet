#!/usr/bin/env python3

import minimalmodbus
import serial
import time

# Initialize the Modbus instrument
meter_rs485 = minimalmodbus.Instrument('COM4', 1)  # COM port and slave address

# Configure the serial connection
meter_rs485.serial.baudrate = 115200
meter_rs485.serial.bytesize = 8
meter_rs485.serial.parity = serial.PARITY_NONE
meter_rs485.serial.stopbits = 1
meter_rs485.serial.timeout = 0.05  # Timeout in seconds

# Set Modbus communication mode
meter_rs485.mode = minimalmodbus.MODE_RTU
meter_rs485.clear_buffers_before_each_transaction = True

# Initialize counters for packet success and failures
nSuccess_rs485 = 0 
nFail_rs485 = 0

# Loop to read register 5000 times
for _ in range(5000):
    try:
        # Read a register (adjust register number and parameters as needed)
        nSN1 = meter_rs485.read_register(38144, 0, 3)  # Registernumber, number of decimals, function code

        nSuccess_rs485 += 1
        print("************** RS485 **************")
        print(f"Packet success_rs485: {nSuccess_rs485}, result is {nSN1}")
        print(f"Packet error_rs485: {nFail_rs485}")
    except IOError:
        nFail_rs485 += 1
        print("************** RS485 **************")
        print(f"Packet success_rs485: {nSuccess_rs485}")
        print(f"Packet error_rs485: {nFail_rs485}")
        # Measure and print roundtrip time
        nRoundtriptime_rs485 = meter_rs485.roundtrip_time
        print(f"Roundtrip time_rs485: {nRoundtriptime_rs485:.6f}")
