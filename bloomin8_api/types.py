"""
Type definitions for the Bloomin8 API.

This module contains enums and data classes used throughout the library.
"""

from enum import Enum
from typing import Optional

from .bloomin8_client.models.get_device_info_response_200 import GetDeviceInfoResponse200


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
    
    def __str__(self) -> str:
        """Return a human-readable string representation of device info."""
        lines = ["DeviceInfo:"]
        
        # Basic info
        if self.name:
            lines.append(f"  Name: {self.name}")
        if self.version:
            lines.append(f"  Firmware: {self.version}")
        
        # Hardware
        if self.board_model or self.screen_model:
            lines.append("  Hardware:")
            if self.board_model:
                lines.append(f"    Board: {self.board_model}")
            if self.screen_model:
                lines.append(f"    Screen: {self.screen_model}")
            if self.width and self.height:
                lines.append(f"    Resolution: {self.width}x{self.height}")
        
        # Network
        if self.ip_address or self.ssid or self.network_type:
            lines.append("  Network:")
            if self.network_type:
                lines.append(f"    Type: {self.network_type}")
            if self.ip_address:
                lines.append(f"    IP: {self.ip_address}")
            if self.ssid:
                lines.append(f"    SSID: {self.ssid}")
        
        # Storage
        if self.total_size is not None or self.free_size is not None:
            lines.append("  Storage:")
            if self.total_size is not None:
                total_mb = self.total_size / (1024 * 1024)
                lines.append(f"    Total: {total_mb:.2f} MB")
            if self.free_size is not None:
                free_mb = self.free_size / (1024 * 1024)
                lines.append(f"    Free: {free_mb:.2f} MB")
                if self.total_size is not None:
                    used_pct = ((self.total_size - self.free_size) / self.total_size) * 100
                    lines.append(f"    Used: {used_pct:.1f}%")
        
        # Battery
        if self.battery is not None:
            lines.append(f"  Battery: {self.battery}%")
        
        # Current state
        if self.gallery or self.image or self.playlist:
            lines.append("  Current State:")
            if self.gallery:
                lines.append(f"    Gallery: {self.gallery}")
            if self.image:
                lines.append(f"    Image: {self.image}")
            if self.playlist:
                lines.append(f"    Playlist: {self.playlist}")
            if self.play_type is not None:
                play_types = {0: "Single Image", 1: "Gallery Slideshow", 2: "Playlist"}
                play_type_str = play_types.get(self.play_type, f"Unknown ({self.play_type})")
                lines.append(f"    Play Type: {play_type_str}")
        
        # Configuration
        if self.sleep_duration is not None or self.max_idle is not None:
            lines.append("  Configuration:")
            if self.sleep_duration is not None:
                lines.append(f"    Sleep Duration: {self.sleep_duration}s")
            if self.max_idle is not None:
                lines.append(f"    Max Idle: {self.max_idle}s")
        
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """Return a detailed representation for debugging."""
        return (f"DeviceInfo(name={self.name!r}, version={self.version!r}, "
                f"ip={self.ip_address!r}, battery={self.battery}%)")
