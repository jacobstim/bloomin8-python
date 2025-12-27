# Bluetooth Wake-Up Feature

The Bloomin8 API includes Bluetooth wake-up functionality to wake devices from sleep mode before attempting HTTP connections.

## Installation

To enable Bluetooth wake-up support, install the `bleak` package:

```bash
pip install bleak
```

## Usage

### Instance Method (Recommended)

The Bloomin8 class includes a built-in `wake_device()` method:

```python
from bloomin8_api import Bloomin8

# Create instance with BLE device name
device = Bloomin8("10.0.0.41", ble_name="BLOOMIN8 eCanvas")

# Wake the device
device.wake_device()

# Use normally
info = device.system.get_device_info()
galleries = device.galleries.list()
```

### With Known MAC Address

If you know the Bluetooth MAC address, you can skip scanning:

```python
device = Bloomin8(
    "10.0.0.41",
    ble_name="BLOOMIN8 eCanvas",
    ble_address="AA:BB:CC:DD:EE:FF"
)

# Wake using the stored address (faster, no scanning)
device.wake_device()
```

### Updating BLE Settings

You can update BLE settings after creating the instance:

```python
device = Bloomin8("10.0.0.41")

# Set BLE parameters later
device.ble_name = "BLOOMIN8 eCanvas"
device.ble_address = "AA:BB:CC:DD:EE:FF"

# Wake device
device.wake_device(verbose=True)
```

### From Command Line (main.py)

By default, `main.py` will attempt to wake the device via Bluetooth before connecting:

```bash
# Default: attempts Bluetooth wake-up
python main.py --host 10.0.0.70

# Specify custom device name to search for
python main.py --host 10.0.0.70 --device-name "BLOOMIN8 eCanvas"

# Skip Bluetooth wake-up (faster if device is already awake)
python main.py --host 10.0.0.70 --no-wakeup

# Verbose mode shows Bluetooth scanning details
python main.py --host 10.0.0.70 --verbose
```

### Standalone Function (Legacy)

The standalone function is still available for backward compatibility:

```python
from bloomin8_api import wake_device_bluetooth

# Wake the device first
wake_success = wake_device_bluetooth("BLOOMIN8 eCanvas")

# Then connect normally
device = Bloomin8("10.0.0.41")
info = device.system.get_device_info()
```

### Advanced Usage

```python
from bloomin8_api import wake_device_bluetooth

# Search for device by name
wake_device_bluetooth(
    device_name="BLOOMIN8",
    scan_timeout=15.0,
    verbose=True
)

# Or use a known MAC address (skips scanning)
wake_device_bluetooth(
    device_address="AA:BB:CC:DD:EE:FF",
    verbose=True
)

# Silent mode (no output)
wake_device_bluetooth("BLOOMIN8", verbose=False)
```

## How It Works

1. **Scans** for nearby Bluetooth devices matching the specified name
2. **Connects** to the device via Bluetooth Low Energy (BLE)
3. **Reads services** which triggers the device to wake from sleep
4. **Waits** 2 seconds for the device to fully initialize
5. Device is now ready for HTTP API connections

## Troubleshooting

### "bleak not installed" warning

Install the bleak package:
```bash
pip install bleak
```

### Device not found via Bluetooth

- Ensure Bluetooth is enabled on your computer
- Check that the device is in range (typically <10 meters)
- Verify the device name with `--device-name` parameter
- Try increasing scan timeout in code: `scan_timeout=20.0`

### Permission errors (Linux)

On Linux, you may need to grant Bluetooth permissions:
```bash
sudo setcap cap_net_raw+ep $(which python)
```

### Still can't connect after wake-up

The device may need more time to initialize. Try:
- Adding a longer sleep after wake-up
- Using `--verbose` to see connection details
- Checking your network connection to the device

## Performance

- **With wake-up**: ~12-15 seconds total (10s scan + 2s wake + connection)
- **Without wake-up** (`--no-wakeup`): ~1-3 seconds (just HTTP connection)

**Recommendation**: Use `--no-wakeup` when you know the device is already awake for faster execution.

## Platform Support

The `bleak` library supports:
- ✅ Windows 10/11 (Bluetooth 4.0+)
- ✅ macOS (10.15+)
- ✅ Linux (BlueZ 5.43+)

## Example: Complete Workflow

```python
from bloomin8_api import Bloomin8, wake_device_bluetooth, DeviceUnreachableError

# Wake device via Bluetooth
print("Waking device...")
if wake_device_bluetooth("BLOOMIN8 eCanvas"):
    print("Device woken successfully")
else:
    print("Could not wake via Bluetooth, trying HTTP anyway...")

# Connect and use device
try:
    device = Bloomin8("10.0.0.41")
    info = device.system.get_device_info()
    print(f"Connected to {info.name}")
except DeviceUnreachableError:
    print("Device is not reachable")
```
