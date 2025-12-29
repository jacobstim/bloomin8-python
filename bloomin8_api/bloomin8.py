"""
Bloomin8 Device Manager

This module provides a high-level, user-friendly interface to interact with Bloomin8 devices.
It wraps the low-level API client with organized methods for device management, galleries,
images, and playlists.

Example:
    >>> from bloomin8_api import Bloomin8
    >>> device = Bloomin8("10.0.0.41")
    >>> info = device.system.get_device_info()
    >>> galleries = device.galleries.list()
    >>> images = device.galleries.get_images("my_gallery")
"""

from enum import Enum
from typing import Optional, TypeVar, Callable, Any, Union
from functools import wraps
from pathlib import Path
import logging

import httpx
import httpcore

from .bloomin8_client.client import Client
from .bloomin8_client.errors import DeviceUnreachableError
from .bloomin8_client.models.get_device_info_response_200 import GetDeviceInfoResponse200
from .bloomin8_client.types import File
from .bloomin8_client.models.post_upload_body import PostUploadBody
from .bloomin8_client.api.system_ap_is import (
    get_device_info,
    get_state,
    get_whistle,
    post_clear_screen,
    post_reboot,
    post_settings,
    post_show,
    post_show_next,
    post_sleep,
)
from .bloomin8_client.api.gallery_ap_is import (
    get_gallery_list,
    get_gallery,
    put_gallery,
    delete_gallery,
)
from .bloomin8_client.api.image_ap_is import (
    post_upload,
    post_image_upload_multi,
    post_image_data_upload,
    post_image_delete,
)
from .bloomin8_client.api.playlist_ap_is import (
    get_playlist_list,
    get_playlist,
    put_playlist,
    delete_playlist,
)


T = TypeVar('T')


class NetworkType(Enum):
    """Network connection type for the Bloomin8 device."""
    UNKNOWN = 0
    ETHERNET = 1
    WIFI = 2
    
    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return self.name.title().replace('Wifi', 'WiFi')


class DeviceInfo:
    """
    Enhanced device information wrapper with user-friendly property names.
    
    This wraps the raw API response and provides cleaner attribute names
    and enhanced types (like NetworkType enum).
    """
    
    def __init__(self, raw_info: GetDeviceInfoResponse200):
        """Initialize with raw device info from API."""
        self._raw = raw_info
    
    # Basic info properties
    @property
    def name(self) -> Optional[str]:
        """Device name."""
        return self._raw.name if hasattr(self._raw, 'name') else None
    
    @property
    def version(self) -> Optional[str]:
        """Firmware version."""
        return self._raw.version if hasattr(self._raw, 'version') else None
    
    # Hardware properties
    @property
    def board_model(self) -> Optional[str]:
        """Board model identifier."""
        return self._raw.board_model if hasattr(self._raw, 'board_model') else None
    
    @property
    def screen_model(self) -> Optional[str]:
        """Screen model identifier."""
        return self._raw.screen_model if hasattr(self._raw, 'screen_model') else None
    
    @property
    def width(self) -> Optional[int]:
        """Display width in pixels."""
        return self._raw.width if hasattr(self._raw, 'width') else None
    
    @property
    def height(self) -> Optional[int]:
        """Display height in pixels."""
        return self._raw.height if hasattr(self._raw, 'height') else None
    
    # Network properties (with cleaner names)
    @property
    def ip_address(self) -> Optional[str]:
        """Device IP address (cleaner alias for sta_ip)."""
        return self._raw.sta_ip if hasattr(self._raw, 'sta_ip') else None
    
    @property
    def ssid(self) -> Optional[str]:
        """WiFi SSID (cleaner alias for sta_ssid)."""
        return self._raw.sta_ssid if hasattr(self._raw, 'sta_ssid') else None
    
    @property
    def network_type(self) -> Optional[NetworkType]:
        """Network connection type as an enum."""
        if hasattr(self._raw, 'network_type') and self._raw.network_type is not None:
            try:
                return NetworkType(self._raw.network_type)
            except ValueError:
                return NetworkType.UNKNOWN
        return None
    
    # Storage properties
    @property
    def total_size(self) -> Optional[int]:
        """Total storage size in bytes."""
        return self._raw.total_size if hasattr(self._raw, 'total_size') else None
    
    @property
    def free_size(self) -> Optional[int]:
        """Free storage size in bytes."""
        return self._raw.free_size if hasattr(self._raw, 'free_size') else None
    
    # Power properties
    @property
    def battery(self) -> Optional[int]:
        """Battery level percentage (0-100)."""
        return self._raw.battery if hasattr(self._raw, 'battery') else None
    
    # Current state properties
    @property
    def gallery(self) -> Optional[str]:
        """Currently displayed gallery name."""
        return self._raw.gallery if hasattr(self._raw, 'gallery') else None
    
    @property
    def image(self) -> Optional[str]:
        """Currently displayed image path."""
        return self._raw.image if hasattr(self._raw, 'image') else None
    
    @property
    def playlist(self) -> Optional[str]:
        """Currently active playlist name."""
        return self._raw.playlist if hasattr(self._raw, 'playlist') else None
    
    @property
    def play_type(self) -> Optional[int]:
        """Play type: 0=single image, 1=gallery slideshow, 2=playlist."""
        return self._raw.play_type if hasattr(self._raw, 'play_type') else None
    
    # Configuration properties
    @property
    def sleep_duration(self) -> Optional[int]:
        """Sleep duration in seconds."""
        return self._raw.sleep_duration if hasattr(self._raw, 'sleep_duration') else None
    
    @property
    def max_idle(self) -> Optional[int]:
        """Maximum idle time in seconds."""
        return self._raw.max_idle if hasattr(self._raw, 'max_idle') else None
    
    @property
    def fs_ready(self) -> Optional[bool]:
        """Whether filesystem is ready."""
        return self._raw.fs_ready if hasattr(self._raw, 'fs_ready') else None
    
    @property
    def next_time(self) -> Optional[int]:
        """Next scheduled action time (Unix timestamp)."""
        return self._raw.next_time if hasattr(self._raw, 'next_time') else None


def handle_connection_errors(host: str) -> Callable:
    """
    Decorator to handle connection errors gracefully.
    
    Converts low-level httpx/httpcore exceptions into user-friendly DeviceUnreachableError.
    
    Args:
        host: The host address for error messages
        
    Returns:
        Decorated function that handles connection errors
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except httpcore.ConnectTimeout:
                raise DeviceUnreachableError(host, "Connection timed out")
            except httpcore.ConnectError as e:
                raise DeviceUnreachableError(host, f"Connection failed: {e}")
            except httpx.ConnectTimeout:
                raise DeviceUnreachableError(host, "Connection timed out")
            except httpx.ConnectError as e:
                raise DeviceUnreachableError(host, f"Connection failed: {e}")
            except httpx.TimeoutException:
                raise DeviceUnreachableError(host, "Request timed out")
            except httpx.NetworkError as e:
                raise DeviceUnreachableError(host, f"Network error: {e}")
            except OSError as e:
                # Catch socket-level errors (connection refused, etc.)
                if "refused" in str(e).lower() or "unreachable" in str(e).lower():
                    raise DeviceUnreachableError(host, str(e))
                raise  # Re-raise if it's a different OSError
        return wrapper
    return decorator


class SystemManager:
    """Manages system-level operations on the Bloomin8 device."""

    def __init__(self, client: Client, host: str):
        """
        Initialize the SystemManager.

        Args:
            client: The underlying API client
            host: The host address for error messages
        """
        self._client = client
        self._host = host

    @property
    def _handle_errors(self):
        """Get the error handler decorator for this manager."""
        return handle_connection_errors(self._host)

    def get_device_info(self) -> Optional[DeviceInfo]:
        """
        Get device information including hardware and software details.

        Returns:
            Enhanced DeviceInfo object with user-friendly property names,
            or None if the request fails
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            raw_info = get_device_info.sync(client=self._client)
            return DeviceInfo(raw_info) if raw_info else None
        return _call()

    def get_state(self):
        """
        Get the current state of the device.

        Returns:
            Device state object
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return get_state.sync(client=self._client)
        return _call()

    def get_whistle(self):
        """
        Get whistle information from the device.

        Returns:
            Whistle information
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return get_whistle.sync(client=self._client)
        return _call()

    def clear_screen(self):
        """
        Clear the device screen.

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_clear_screen.sync(client=self._client)
        return _call()

    def reboot(self):
        """
        Reboot the device.

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        return post_reboot.sync(client=self._client)

    def update_settings(self, settings):
        """
        Update device settings.

        Args:
            settings: Settings object to update

        Returns:
            Response from the device
        """
        return post_settings.sync(client=self._client, body=settings)

    def show(self, body):
        """
        Show content on the device.

        Args:
            body: Show configuration object

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_show.sync(client=self._client, body=body)
        return _call()

    def show_next(self):
        """
        Show the next item in the current playlist or gallery.

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_show_next.sync(client=self._client)
        return _call()

    def sleep(self):
        """
        Put the device into sleep mode.

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_sleep.sync(client=self._client)
        return _call()


class GalleryManager:
    """Manages galleries and images on the Bloomin8 device."""

    def __init__(self, client: Client, host: str):
        """
        Initialize the GalleryManager.

        Args:
            client: The underlying API client
            host: The host address for error messages
        """
        self._client = client
        self._host = host
    
    @property
    def _handle_errors(self):
        """Get the error handler decorator for this manager."""
        return handle_connection_errors(self._host)

    def list(self):
        """
        List all galleries on the device.

        Returns:
            List of gallery objects
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return get_gallery_list.sync(client=self._client)
        return _call()

    def get(self, gallery_name: str, offset: int = 0, limit: int = 100):
        """
        Get details and images from a specific gallery.

        Args:
            gallery_name: Name of the gallery
            offset: Starting offset for pagination (default: 0)
            limit: Maximum number of images to return (default: 100)

        Returns:
            Gallery object with image data
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return get_gallery.sync(
                client=self._client,
                gallery_name=gallery_name,
                offset=offset,
                limit=limit,
            )
        return _call()

    def get_images(self, gallery_name: str, offset: int = 0, limit: int = 100):
        """
        Get images from a specific gallery (convenience method).

        Args:
            gallery_name: Name of the gallery
            offset: Starting offset for pagination (default: 0)
            limit: Maximum number of images to return (default: 100)

        Returns:
            List of image objects from the gallery
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        gallery = self.get(gallery_name, offset, limit)
        return gallery.data if gallery and hasattr(gallery, 'data') else []

    def create_or_update(self, gallery_name: str, gallery_data):
        """
        Create a new gallery or update an existing one.

        Args:
            gallery_name: Name of the gallery
            gallery_data: Gallery configuration data

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return put_gallery.sync(
                client=self._client,
                gallery_name=gallery_name,
                body=gallery_data,
            )
        return _call()

    def delete(self, gallery_name: str):
        """
        Delete a gallery from the device.

        Args:
            gallery_name: Name of the gallery to delete

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return delete_gallery.sync(client=self._client, gallery_name=gallery_name)
        return _call()


class ImageManager:
    """Manages image uploads and deletions on the Bloomin8 device."""

    def __init__(self, client: Client, host: str):
        """
        Initialize the ImageManager.

        Args:
            client: The underlying API client
            host: The host address for error messages
        """
        self._client = client
        self._host = host
    
    @property
    def _handle_errors(self):
        """Get the error handler decorator for this manager."""
        return handle_connection_errors(self._host)

    def upload(self, body):
        """
        Upload a single image to the device.

        Args:
            body: Image upload data

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_upload.sync(client=self._client, body=body)
        return _call()

    def upload_multiple(self, body):
        """
        Upload multiple images to the device.

        Args:
            body: Multiple image upload data

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_image_upload_multi.sync(client=self._client, body=body)
        return _call()

    def upload_data(self, body):
        """
        Upload image data directly to the device.

        Args:
            body: Image data to upload

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_image_data_upload.sync(client=self._client, body=body)
        return _call()

    def delete(self, body):
        """
        Delete an image from the device.

        Args:
            body: Image deletion data (gallery name and image ID)

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_image_delete.sync(client=self._client, body=body)
        return _call()
    
    def upload_from_file(self, file_path: Union[str, Path], gallery_name: str):
        """
        Upload an image file from the local filesystem to the device.
        
        This is a convenience method that handles reading the file and creating
        the appropriate upload request.
        
        Args:
            file_path: Path to the image file (string or Path object)
            gallery_name: Name of the gallery to upload to
            
        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
            FileNotFoundError: If the file does not exist
            IOError: If there's an error reading the file
            
        Example:
            >>> device = Bloomin8("10.0.0.41")
            >>> device.images.upload_from_file("/path/to/photo.jpg", "my_gallery")
        """
        # Convert to Path object if string
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        # Verify file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
        
        # Read the file
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        # Create File object and upload body
        file_obj = File(payload=image_data, file_name=file_path.name)
        upload_body = PostUploadBody(image=file_obj)
        
        # Upload using the API endpoint directly with proper parameters
        @self._handle_errors
        def _call():
            return post_upload.sync_detailed(
                client=self._client,
                body=upload_body,
                filename=file_path.name,
                gallery=gallery_name
            )
        return _call()


class PlaylistManager:
    """Manages playlists on the Bloomin8 device."""

    def __init__(self, client: Client, host: str):
        """
        Initialize the PlaylistManager.

        Args:
            client: The underlying API client
            host: The host address for error messages
        """
        self._client = client
        self._host = host
    
    @property
    def _handle_errors(self):
        """Get the error handler decorator for this manager."""
        return handle_connection_errors(self._host)

    def list(self):
        """
        List all playlists on the device.

        Returns:
            List of playlist objects
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return get_playlist_list.sync(client=self._client)
        return _call()

    def get(self, playlist_name: str):
        """
        Get details of a specific playlist.

        Args:
            playlist_name: Name of the playlist

        Returns:
            Playlist object with configuration
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return get_playlist.sync(client=self._client, playlist_name=playlist_name)
        return _call()

    def create_or_update(self, playlist_name: str, playlist_data):
        """
        Create a new playlist or update an existing one.

        Args:
            playlist_name: Name of the playlist
            playlist_data: Playlist configuration data

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return put_playlist.sync(
                client=self._client,
                playlist_name=playlist_name,
                body=playlist_data,
            )
        return _call()

    def delete(self, playlist_name: str):
        """
        Delete a playlist from the device.

        Args:
            playlist_name: Name of the playlist to delete

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return delete_playlist.sync(client=self._client, playlist_name=playlist_name)
        return _call()


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
        >>> device = Bloomin8("10.0.0.41", ble_name="BLOOMIN8 eCanvas")
        >>> device.wake_device()  # Wake via Bluetooth
        >>> device.system.get_device_info()
        >>> device.galleries.list()
        >>> device.images.upload(image_data)
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
            timeout: Connection timeout in seconds (default: 0.2)
            
        Returns:
            True if device responds within timeout, False otherwise
            
        Example:
            >>> device = Bloomin8("10.0.0.41")
            >>> if not device.is_awake():
            >>>     device.wake_device()
            >>> info = device.system.get_device_info()
        """
        import httpx
        
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


# Bluetooth Wake-up Functionality
# Note: This requires the 'bleak' package to be installed

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
        from bleak import BleakScanner
        
        log.info(f"Scanning for Bluetooth device '{device_name}'...")
        devices = await BleakScanner.discover(timeout=timeout)
        
        for device in devices:
            if device.name and device_name.lower() in device.name.lower():
                log.info(f"Found device: {device.name} ({device.address})")
                return device.address
        
        log.warning(f"Device '{device_name}' not found")
        return None
        
    except ImportError:
        log.error("Warning: 'bleak' package not installed. Install with: pip install bleak")
        return None
    except Exception as e:
        log.error(f"Bluetooth scan error: {e}")
        return None


async def _send_wake_signal_async(address: str, logger: Optional[logging.Logger] = None) -> bool:
    """
    Send a wake signal to the device via Bluetooth.
    
    Sends a magic BLE packet (0x01) to the wake-up characteristic to wake the device,
    then after 3 seconds sends 0x00 to reset the wakeup function.
    
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
        from bleak import BleakClient
        import asyncio
        
        log.info(f"Connecting to device at {address}...")
        async with BleakClient(address, timeout=10.0) as client:
            if client.is_connected:
                log.debug("Connected via Bluetooth")
                
                # Send wake-up signal (0x01)
                log.debug(f"Sending wake-up signal to {WAKEUP_CHARACTERISTIC_UUID}...")
                await client.write_gatt_char(WAKEUP_CHARACTERISTIC_UUID, WAKEUP_PAYLOAD)
                log.debug("Wake-up signal sent (0x01)")
                
                # Wait 100ms before sending reset
                log.debug("Waiting 100ms...")
                await asyncio.sleep(0.1)
                
                # Send reset signal (0x00)
                log.debug(f"Sending reset signal to {WAKEUP_CHARACTERISTIC_UUID}...")
                await client.write_gatt_char(WAKEUP_CHARACTERISTIC_UUID, WAKEUP_RESET_PAYLOAD)
                log.debug("Reset signal sent (0x00)")
                
                return True
            else:
                log.error("Failed to connect via Bluetooth")
                return False
                
    except ImportError:
        log.error("Warning: 'bleak' package not installed. Install with: pip install bleak")
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
    connects to it via Bluetooth, and sends a wake signal by reading services.
    
    Args:
        device_name: Name of the device to search for (default: "BLOOMIN8")
        device_address: Optional MAC address if known (skips scanning)
        scan_timeout: How long to scan for devices in seconds (default: 10.0)
        logger: Optional logger instance (default: None)
        
    Returns:
        Tuple of (success: bool, discovered_address: Optional[str])
        
    Example:
        >>> from bloomin8_api import wake_device_bluetooth
        >>> wake_device_bluetooth("BLOOMIN8 eCanvas")
        >>> # Then connect normally
        >>> device = Bloomin8("10.0.0.41")
        
    Note:
        Requires the 'bleak' package: pip install bleak
    """
    import asyncio
    
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
        discovered_address = None
        if device_address is None:
            device_address = loop.run_until_complete(
                _scan_for_device_async(device_name, scan_timeout, log)
            )
            discovered_address = device_address
            
            if device_address is None:
                log.warning(f"Could not find device '{device_name}' via Bluetooth")
                return False, None
        
        # Send wake signal
        success = loop.run_until_complete(_send_wake_signal_async(device_address, log))
        
        if success:
            log.info("Wake signal sent successfully. Device should now be awake.")
        
        return success, discovered_address
        
    except Exception as e:
        log.error(f"Bluetooth wake-up failed: {e}")
        return False, None
