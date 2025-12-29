"""Gallery manager for Bloomin8 device operations."""

from ..bloomin8_client.client import Client
from ..bloomin8_client.api.gallery_ap_is import (
    get_gallery_list,
    get_gallery,
    put_gallery,
    delete_gallery,
)
from ..utils import handle_connection_errors


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
