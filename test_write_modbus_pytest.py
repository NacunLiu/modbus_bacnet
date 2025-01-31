from pymodbus.client import ModbusTcpClient
import pytest

# Modbus server connection details
MODBUS_SERVER_IP = "192.168.61.139"  # Change this to your actual Modbus server IP
MODBUS_PORT = 502  # Default Modbus TCP port

# Register address and values
START_ADDRESS = 17952
WRITE_VALUES = [
    6, 47101]

@pytest.fixture(scope="module")
def modbus_client():
    """Fixture to initialize and close Modbus client"""
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
    assert client.connect(), "Failed to connect to Modbus server"
    yield client
    client.close()

def test_modbus_write_read(modbus_client):
    """Test Modbus write and read functionality"""
    
    # Write data to registers
    write_response = modbus_client.write_registers(START_ADDRESS, WRITE_VALUES)
    assert not write_response.isError(), f"Write failed: {write_response}"

    # Read back the data
    read_response = modbus_client.read_holding_registers(START_ADDRESS, len(WRITE_VALUES))
    assert not read_response.isError(), f"Read failed: {read_response}"

    read_values = list(read_response.registers)  # Extract values from response

    # Assert that written values match read values
    assert read_values == WRITE_VALUES, f"Mismatch: Written {WRITE_VALUES}, Read {read_values}"

    print("✅ Modbus write and read test passed!")

if __name__ == "__main__":
    # Run test manually
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
    if client.connect():
        test_modbus_write_read(client)
        client.close()
    else:
        print("❌ Failed to connect to Modbus server")
