"""
Bluetooth wake-up functionality for Bloomin8 devices.

This module provides functions to wake a device from sleep using Bluetooth LE.
Requires the 'bleak' package: pip install bleak
"""

import asyncio
import logging
from typing import Optional
from bleak import BleakClient
from bleak import BleakScanner

async def _scan_for_device_async(device_name: str, timeout: float = 10.0, logger: Optional[logging.Logger] = None) -> Optional[str]:
    """
    Scan for a Bluetooth device by name and return its address.
    
    Args:
        device_name: The name of the device to search for
        timeout: Scan timeout in seconds
        logger: Optional logger instance
        
    Returns:
        Device MAC address if found, None otherwise
    """
    log = logger or logging.getLogger(__name__)
    
    try:
        log.info(f"Scanning for Bluetooth device '{device_name}'...")
        devices = await BleakScanner.discover(timeout=timeout)
        
        for device in devices:
            if device.name and device_name.lower() in device.name.lower():
                log.info(f"Found device: {device.name} ({device.address})")
                return device.address
        
        log.warning(f"Device '{device_name}' not found")
        return None

    except Exception as e:
        log.error(f"Bluetooth scan error: {e}")
        return None


async def _send_wake_signal_async(address: str, logger: Optional[logging.Logger] = None) -> bool:
    """
    Send a wake signal to the device via Bluetooth.
    
    Sends a magic BLE packet (0x01) to the wake-up characteristic to wake the device,
    then after 100ms sends 0x00 to reset the wakeup function.
    
    Args:
        address: Bluetooth MAC address of the device
        logger: Optional logger instance
        
    Returns:
        True if successful, False otherwise
    """
    log = logger or logging.getLogger(__name__)
    
    # Wake-up BLE characteristic UUID
    WAKEUP_CHARACTERISTIC_UUID = "0000f001-0000-1000-8000-00805f9b34fb"
    
    # Wake-up payloads
    WAKEUP_PAYLOAD = bytes([0x01])  # Magic BLE wake packet
    WAKEUP_RESET_PAYLOAD = bytes([0x00])  # Reset wakeup function
    
    try:
        log.debug(f"Connecting to device at {address}...")
        async with BleakClient(address, timeout=10.0) as client:
            if client.is_connected:
                log.debug("Connected via Bluetooth")
                
                # Send wake-up signal (0x01)
                log.debug(f"-> Sending wake-up signal to {WAKEUP_CHARACTERISTIC_UUID}...")
                await client.write_gatt_char(WAKEUP_CHARACTERISTIC_UUID, WAKEUP_PAYLOAD)
                log.debug("-> Wake-up signal sent (0x01)")
                
                # Wait 100ms before sending reset
                log.debug("-> Waiting 100ms...")
                await asyncio.sleep(0.1)
                
                # Send reset signal (0x00)
                log.debug(f"-> ending reset signal to {WAKEUP_CHARACTERISTIC_UUID}...")
                await client.write_gatt_char(WAKEUP_CHARACTERISTIC_UUID, WAKEUP_RESET_PAYLOAD)
                log.debug("-> Reset signal sent (0x00)")
                
                return True
            else:
                log.error("Failed to connect via Bluetooth")
                return False

    except Exception as e:
        log.error(f"Bluetooth connection error: {e}")
        return False


def wake_device_bluetooth(
    device_name: str = "BLOOMIN8",
    device_address: Optional[str] = None,
    scan_timeout: float = 10.0,
    logger: Optional[logging.Logger] = None
) -> tuple[bool, Optional[str]]:
    """
    Wake a Bloomin8 device from sleep using Bluetooth.
    
    This function scans for the device by name (or uses a provided address),
    connects to it via Bluetooth, and sends a wake signal.
    
    Args:
        device_name: Name of the device to search for (default: "BLOOMIN8")
        device_address: Optional MAC address if known (skips scanning)
        scan_timeout: How long to scan for devices in seconds (default: 10.0)
        logger: Optional logger instance (default: None)
        
    Returns:
        Tuple of (success: bool, discovered_address: Optional[str])
        
    Example:
        >>> from bloomin8_api.bluetooth import wake_device_bluetooth
        >>> success, address = wake_device_bluetooth("BLOOMIN8 eCanvas")
        >>> # Then connect normally
        >>> from bloomin8_api import Bloomin8
        >>> device = Bloomin8("10.0.0.41")
        
    Note:
        Requires the 'bleak' package: pip install bleak
    """
    # Use provided logger or create a new one
    log = logger or logging.getLogger(__name__)

    try:
        # Get or create event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Find device if address not provided
        if device_address is None:
            device_address = loop.run_until_complete(
                _scan_for_device_async(device_name, scan_timeout, log)
            )
            
            if device_address is None:
                log.warning(f"Could not find device '{device_name}' via Bluetooth")
                return False, None
        
        # Send wake signal
        success = loop.run_until_complete(_send_wake_signal_async(device_address, log))
        
        if success:
            log.debug("Wake signal sent successfully. Device should now be awake.")
        
        return success, device_address
        
    except Exception as e:
        log.error(f"Bluetooth wake-up failed: {e}")
        return False, None
