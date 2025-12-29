"""System manager for Bloomin8 device operations."""

from typing import Optional, Callable
from functools import wraps

from ..bloomin8_client.client import Client
from ..bloomin8_client.api.system_ap_is import (
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
from ..types import DeviceInfo
from ..utils import handle_connection_errors


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
            return post_clear_screen.sync_detailed(client=self._client)
        return _call()

    def reboot(self):
        """
        Reboot the device.

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        return post_reboot.sync_detailed(client=self._client)

    def update_settings(self, settings):
        """
        Update device settings.

        Args:
            settings: Settings object to update

        Returns:
            Response from the device
        """
        return post_settings.sync_detailed(client=self._client, body=settings)

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
            return post_show.sync_detailed(client=self._client, body=body)
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
            return post_show_next.sync_detailed(client=self._client)
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
            return post_sleep.sync_detailed(client=self._client)
        return _call()
