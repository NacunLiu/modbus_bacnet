from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time

# Initialize the Modbus serial client
meter_rs485 = ModbusSerialClient(
    method='rtu',
    port='COM4',
    baudrate=115200,
    bytesize=8,  # Data bits
    parity='N',
    stopbits=1,
    timeout=0.05  # Increase timeout to 1 second
)

# Counters for success and failure
nSuccess_rs485 = 0
nFail_rs485 = 0

# Check connection
if not meter_rs485.connect():
    print(" Unable to connect to COM4. Please check the port and device.")
    exit(1)
else:
    print(" Successfully connected to COM4.")

# Test a single read operation
print(" Testing single read operation...")
try:
    test_response = meter_rs485.read_holding_registers(address=38144, count=1, unit=1)
    if test_response and not test_response.isError():
        print(f" Test successful, register value: {test_response.registers[0]}")
    else:
        print(" Test failed, device did not respond or incorrect address.")
except Exception as e:
    print(f" Test read error: {e}")

# Perform 100 read operations
for i in range(100):
    try:
        response = meter_rs485.read_holding_registers(address=38144, count=1, unit=1)

        if response and not response.isError():
            nSN1 = response.registers[0]
            nSuccess_rs485 += 1
            print(f"Read success times:{nSuccess_rs485} reboot times: {nSN1}")
            print(f"read fail times: {nFail_rs485}")
        else:
            raise ModbusIOException(" Read failed")

    except (ModbusIOException, Exception) as modbus_err:
        nFail_rs485 += 1
        print(f"Read success times:{nSuccess_rs485}")
        print(f"read fail time: {nFail_rs485}")

# Close the connection
meter_rs485.close()
print("Connection closed.")
print(f"data packet loss rate {nFail_rs485}%")
