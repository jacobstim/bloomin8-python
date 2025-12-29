# bloomin8-python
Generic Python library for interfacing with the BLOOMIN8 e-Ink Canvas

## Example script
Perform synchronization of a local folder to the BLOOMIN8 device at IP address 10.0.0.70:

```python
python main.py --source P:\Pictureframe\device --host 10.0.0.70
```

If you want the device to be awakened, you can use the Bluetooth name you specify in the Mobile App; this will do a Bluetooth discovery and search for the BLE device with this name.

```python
python main.py --source P:\Pictureframe\device --host 10.0.0.70 --device-name "BLOOMIN8"
```

If you know the BLE MAC address (which you will see in the previous command), speed up the process next time by providing it directly:

```python
python main.py --source P:\Pictureframe\device --host 10.0.0.70 --ble-address "F4:90:72:19:6F:71"
```

Perform a full synchronization, including deletion of files on the device, that were removed from the source folder.

```python
python main.py --source P:\Pictureframe\device --host 10.0.0.70 --ble-address "F4:90:72:19:6F:71" --mirror 
```

Run unattended and perform all synchronization actions

```python
python main.py --source P:\Pictureframe\device --host 10.0.0.70 --ble-address "F4:90:72:19:6F:71" --mirror --force
```
