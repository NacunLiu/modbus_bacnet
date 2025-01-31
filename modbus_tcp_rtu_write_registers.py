from pymodbus.client.sync import ModbusTcpClient
from pymodbus.client.sync import ModbusSerialClient  # ✅ Correct for pymodbus 2.x
import time

# change the IP according to your ip address
MODBUS_SERVER_IP = "192.168.61.139"  # Change to your Modbus device IP
MODBUS_PORT = 502  # Default Modbus TCP port


# Modbus RTU (Serial) Configuration
PORT = "COM4"  # Change this to your actual serial port (Linux: "/dev/ttyUSB0", Windows: "COMx")
BAUDRATE = 19200  # Match with your device settings
STOPBITS = 1
BYTESIZE = 8
PARITY = 'N'  # 'N' (None), 'E' (Even), 'O' (Odd)

# write data
SLAVE_ID = 1  # Modbus slave ID (default is usually 1)
START_ADDRESS = 17952  # Register address to read/write
WRITE_VALUES = [6, 47101, 0, 6775, 6, 52223, 0, 12060, 6, 63425, 0,
                                              2511, 0, 3200, 0, 49436, 0, 11760, 0, 35876, 0, 5567,
                                              0, 38094, 7, 18954, 7, 21871, 7, 21922]  # Data to write

connect = input("please input RTU or TCP based on your connect way")
if connect == "TCP":
   # Create Modbus client
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)

# Connect to Modbus server
    if client.connect():
        print("✅ Connected to Modbus server")
        
        time.sleep(1)

    # Write data to registers
        write_response = client.write_registers(START_ADDRESS, WRITE_VALUES, unit=SLAVE_ID)
        if write_response.isError():
            print(f"❌ Write failed: {write_response}")
        else:
            print(f"✅ Successfully wrote {WRITE_VALUES} to address {START_ADDRESS}")

    # Read back the values
        read_response = client.read_holding_registers(START_ADDRESS, len(WRITE_VALUES), unit=SLAVE_ID)
        if read_response.isError():
            print(f"❌ Read failed: {read_response}")
        else:
           print(f"✅ Read values from {START_ADDRESS}: {read_response.registers}")
           
        time.sleep(1)
        
    # Close the connection
        client.close()
        print("🔴 Disconnected from Modbus server")
    else:
        print("❌ Failed to connect to Modbus server")       


else:    
    # Initialize Modbus RTU client
    client = ModbusSerialClient(
        method="rtu", 
        port=PORT, 
        baudrate=BAUDRATE, 
        stopbits=STOPBITS, 
        bytesize=BYTESIZE, 
        parity=PARITY,
        timeout=3
    )

# Connect to Modbus RTU device
    if client.connect():
        print(f"✅ Connected to Modbus RTU device on {PORT}")
        
        time.sleep(1)

    # Write data to Modbus register
        write_response = client.write_registers(START_ADDRESS, WRITE_VALUES, unit=SLAVE_ID)
        if write_response.isError():
            print(f"❌ Write failed: {write_response}")
        else:
            print(f"✅ Successfully wrote {WRITE_VALUES} to address {START_ADDRESS}")

    # Wait a bit before reading (some devices need time to process)
        time.sleep(1)

    # Read back the written values
        read_response = client.read_holding_registers(START_ADDRESS, len(WRITE_VALUES), unit=SLAVE_ID)
        if read_response.isError():
            print(f"❌ Read failed: {read_response}")
        else:
            print(f"✅ Read values from {START_ADDRESS}: {read_response.registers}")

        time.sleep(1)
        
    # Close the connection
        client.close()
        print("🔴 Disconnected from Modbus RTU device")
    else:
        print(f"❌ Failed to connect to Modbus RTU device on {PORT}")





