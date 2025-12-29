"""
Bloomin8 API Client

A Python library for interacting with Bloomin8 E-Ink Canvas devices.

Example:
    >>> from bloomin8_api import Bloomin8
    >>> device = Bloomin8("10.0.0.41")
    >>> info = device.system.get_device_info()
    >>> galleries = device.galleries.list()
"""

from .client import Bloomin8
from .types import DeviceInfo, NetworkType
from .bluetooth import wake_device_bluetooth
from .bloomin8_client.errors import DeviceUnreachableError
from .bloomin8_client.client import AuthenticatedClient, Client

__all__ = (
    "Bloomin8",
    "DeviceInfo",
    "NetworkType",
    "DeviceUnreachableError",
    "wake_device_bluetooth",
    "AuthenticatedClient",
    "Client",
)
