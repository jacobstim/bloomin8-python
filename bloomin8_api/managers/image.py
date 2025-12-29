"""Image manager for Bloomin8 device operations."""

from pathlib import Path
from typing import Union

from ..bloomin8_client.client import Client
from ..bloomin8_client.types import File
from ..bloomin8_client.models.post_upload_body import PostUploadBody
from ..bloomin8_client.api.image_ap_is import (
    post_upload,
    post_image_upload_multi,
    post_image_data_upload,
    post_image_delete,
)
from ..utils import handle_connection_errors


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
            return post_upload.sync_detailed(client=self._client, body=body)
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
            return post_image_upload_multi.sync_detailed(client=self._client, body=body)
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
            return post_image_data_upload.sync_detailed(client=self._client, body=body)
        return _call()

    def delete(self, image: str, gallery: str = "default"):
        """
        Delete an image from the device.

        Args:
            image: The filename of the image to delete
            gallery: The gallery containing the image (defaults to "default")

        Returns:
            Response from the device
            
        Raises:
            DeviceUnreachableError: If the device cannot be reached
        """
        @self._handle_errors
        def _call():
            return post_image_delete.sync_detailed(client=self._client, image=image, gallery=gallery)
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
            >>> from bloomin8_api import Bloomin8
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
