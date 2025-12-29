"""Playlist manager for Bloomin8 device operations."""

from ..bloomin8_client.client import Client
from ..bloomin8_client.api.playlist_ap_is import (
    get_playlist_list,
    get_playlist,
    put_playlist,
    delete_playlist,
)
from ..utils import handle_connection_errors


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
