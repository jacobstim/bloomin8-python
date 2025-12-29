"""
Main Bloomin8 client class.

This module provides the main entry point for interacting with Bloomin8 devices.
"""

import logging
from typing import Optional

import httpx

from .bloomin8_client.client import Client
from .managers import SystemManager, GalleryManager, ImageManager, PlaylistManager
from .bluetooth import wake_device_bluetooth


class Bloomin8:
    """
    High-level interface for interacting with a Bloomin8 device.

    This class provides a clean, organized API for all device operations,
    grouped into logical managers for system, galleries, images, and playlists.

    Attributes:
        system: SystemManager for device-level operations
        galleries: GalleryManager for managing galleries and their images
        images: ImageManager for uploading and deleting images
        playlists: PlaylistManager for managing playlists

    Example:
        >>> from bloomin8_api import Bloomin8
        >>> device = Bloomin8("10.0.0.41", ble_name="BLOOMIN8 eCanvas")
        >>> device.wake_device()  # Wake via Bluetooth
        >>> device.system.get_device_info()
        >>> device.galleries.list()
        >>> device.images.upload_from_file("photo.jpg", "my_gallery")
        >>> device.playlists.create_or_update("my_playlist", config)
    """

    def __init__(
        self,
        host: str,
        port: int = 80,
        use_https: bool = False,
        timeout: float = 10.0,
        verify_ssl: bool = False,
        ble_name: Optional[str] = None,
        ble_address: Optional[str] = None,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize a Bloomin8 device connection.

        Args:
            host: IP address or hostname of the Bloomin8 device
            port: Port number (default: 80)
            use_https: Use HTTPS instead of HTTP (default: False)
            timeout: Request timeout in seconds (default: 10.0)
            verify_ssl: Verify SSL certificates (default: False for local IoT devices)
            ble_name: Bluetooth device name for wake-up (default: None, uses "BLOOMIN8" if wake_device is called)
            ble_address: Bluetooth MAC address if known (optional, skips scanning)
            logger: Optional logger instance for logging messages (default: None, creates a NullHandler logger)
        """
        self._host = host
        self._ble_name = ble_name
        self._ble_address = ble_address
        self._logger = logger or logging.getLogger(__name__)
        if logger is None:
            # If no logger provided, add a NullHandler to suppress output by default
            self._logger.addHandler(logging.NullHandler())
        
        protocol = "https" if use_https else "http"
        base_url = f"{protocol}://{host}:{port}"

        self._client = Client(
            base_url=base_url,
            timeout=timeout,
            verify_ssl=verify_ssl,
        )

        # Initialize managers with host for error messages
        self.system = SystemManager(self._client, self._host)
        self.galleries = GalleryManager(self._client, self._host)
        self.images = ImageManager(self._client, self._host)
        self.playlists = PlaylistManager(self._client, self._host)

    @property
    def client(self) -> Client:
        """
        Get the underlying API client for advanced usage.

        Returns:
            The raw Client instance
        """
        return self._client
    
    @property
    def ble_name(self) -> Optional[str]:
        """Get the Bluetooth device name for wake-up."""
        return self._ble_name
    
    @ble_name.setter
    def ble_name(self, value: Optional[str]):
        """Set the Bluetooth device name for wake-up."""
        self._ble_name = value
    
    @property
    def ble_address(self) -> Optional[str]:
        """Get the Bluetooth MAC address."""
        return self._ble_address
    
    @ble_address.setter
    def ble_address(self, value: Optional[str]):
        """Set the Bluetooth MAC address."""
        self._ble_address = value

    def is_awake(self, timeout: float = 0.5) -> bool:
        """Check if the device is awake and responsive.
        
        This method attempts a quick connection to the device using get_state()
        with a short timeout to determine if the device is awake or asleep.
        
        Args:
            timeout: Connection timeout in seconds (default: 0.5)
            
        Returns:
            True if device responds within timeout, False otherwise
            
        Example:
            >>> device = Bloomin8("10.0.0.41")
            >>> if not device.is_awake():
            >>>     device.wake_device()
            >>> info = device.system.get_device_info()
        """
        try:
            # Create a temporary httpx client with short timeout
            # We create a new client to ensure timeout is properly applied
            short_timeout = httpx.Timeout(
                connect=timeout,
                read=timeout,
                write=timeout,
                pool=timeout
            )
            
            # Make a direct HTTP request with the short timeout
            with httpx.Client(timeout=short_timeout, verify=self._client._verify_ssl) as client:
                response = client.get(f"{self._client._base_url}/state")
                return response.status_code == 200
            
        except (httpx.TimeoutException, httpx.ConnectTimeout, httpx.ReadTimeout, 
                httpx.ConnectError, httpx.NetworkError, Exception):
            # Any timeout or connection error means device is likely asleep
            return False

    def wake_device(self, scan_timeout: float = 10.0) -> bool:
        """
        Wake the device from sleep using Bluetooth.
        
        This method scans for the device by name (or uses the provided address),
        connects via Bluetooth, and sends a wake signal. If a device is discovered
        during scanning, its MAC address is stored for future use.
        
        Args:
            scan_timeout: How long to scan for devices in seconds (default: 10.0)
            
        Returns:
            True if wake signal was sent successfully, False otherwise
            
        Example:
            >>> device = Bloomin8("10.0.0.41", ble_name="BLOOMIN8 eCanvas")
            >>> device.wake_device()
            >>> print(device.ble_address)  # MAC address stored after discovery
            >>> info = device.system.get_device_info()
            
        Note:
            Requires the 'bleak' package: pip install bleak
        """
        device_name = self._ble_name or "BLOOMIN8"
        success, discovered_address = wake_device_bluetooth(
            device_name=device_name,
            device_address=self._ble_address,
            scan_timeout=scan_timeout,
            logger=self._logger
        )
        
        # Store discovered address if we didn't have one before
        if discovered_address and not self._ble_address:
            self._ble_address = discovered_address
        
        return success

    def __repr__(self) -> str:
        """Return string representation of the Bloomin8 instance."""
        return f"Bloomin8(base_url='{self._client._base_url}')"
