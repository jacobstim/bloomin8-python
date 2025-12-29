# Bloomin8 API Module

A Python interface for interacting with Bloomin8 devices.

## Overview

The `bloomin8_api` module provides a high-level, user-friendly interface to control and manage Bloomin8 devices. It wraps the auto-generated API client with organized managers for different aspects of device control.

## Installation

```python
# Import the main class
from bloomin8_api import Bloomin8
```

## Quick Start

```python
from bloomin8_api import Bloomin8

# Connect to a device by IP address
device = Bloomin8("10.0.0.41")

# Get device information
info = device.system.get_device_info()

# List all galleries
galleries = device.galleries.list()

# Get images from a specific gallery
images = device.galleries.get_images("my_gallery")
```

## Architecture

The `Bloomin8` class is organized into four main managers:

### 1. **SystemManager** (`device.system`)
Handles device-level operations:
- `get_device_info()` - Get hardware and software details
- `get_state()` - Get current device state
- `get_whistle()` - Get whistle information
- `clear_screen()` - Clear the display
- `reboot()` - Reboot the device
- `update_settings(settings)` - Update device settings
- `show(body)` - Show content on the device
- `show_next()` - Show next item in playlist/gallery
- `sleep()` - Put device into sleep mode

### 2. **GalleryManager** (`device.galleries`)
Manages galleries and their images:
- `list()` - List all galleries
- `get(gallery_name, offset=0, limit=100)` - Get gallery details with images
- `get_images(gallery_name, offset=0, limit=100)` - Get images from a gallery (convenience method)
- `create_or_update(gallery_name, gallery_data)` - Create or update a gallery
- `delete(gallery_name)` - Delete a gallery

### 3. **ImageManager** (`device.images`)
Handles image uploads and deletions:
- `upload(body)` - Upload a single image
- `upload_multiple(body)` - Upload multiple images
- `upload_data(body)` - Upload raw image data
- `delete(body)` - Delete an image

### 4. **PlaylistManager** (`device.playlists`)
Manages playlists:
- `list()` - List all playlists
- `get(playlist_name)` - Get playlist details
- `create_or_update(playlist_name, playlist_data)` - Create or update a playlist
- `delete(playlist_name)` - Delete a playlist

## Usage Examples

### System Operations

```python
device = Bloomin8("10.0.0.41")

# Get device information
info = device.system.get_device_info()
print(f"Device: {info.name}, Version: {info.version}")

# Show next item
device.system.show_next()

# Clear screen
device.system.clear_screen()
```

### Gallery Management

```python
device = Bloomin8("10.0.0.41")

# List all galleries
galleries = device.galleries.list()
for gallery in galleries:
    print(f"Gallery: {gallery.name} ({gallery.image_count} images)")

# Get images from a specific gallery
images = device.galleries.get_images("vacation_photos", offset=0, limit=50)
for image in images:
    print(f"Image: {image.filename}")

# Get full gallery details
gallery = device.galleries.get("vacation_photos")
print(f"Gallery has {len(gallery.data)} images")

# Delete a gallery
device.galleries.delete("old_gallery")
```

### Image Operations

```python
device = Bloomin8("10.0.0.41")

# Upload a single image
image_data = {
    "gallery_name": "my_gallery",
    "filename": "photo.jpg",
    "data": image_bytes
}
device.images.upload(image_data)

# Upload multiple images
multi_data = {
    "gallery_name": "my_gallery",
    "images": [image1, image2, image3]
}
device.images.upload_multiple(multi_data)

# Delete an image
delete_data = {
    "gallery_name": "my_gallery",
    "image_id": "photo123"
}
device.images.delete(delete_data)
```

### Playlist Management

```python
device = Bloomin8("10.0.0.41")

# List all playlists
playlists = device.playlists.list()
for playlist in playlists:
    print(f"Playlist: {playlist.name}")

# Get playlist details
playlist = device.playlists.get("slideshow1")
print(f"Playlist type: {playlist.type}")

# Create or update a playlist
playlist_config = {
    "type": "sequential",
    "list": ["gallery1", "gallery2"],
    "duration": 5
}
device.playlists.create_or_update("my_playlist", playlist_config)

# Delete a playlist
device.playlists.delete("old_playlist")
```

## Advanced Usage

### Custom Configuration

```python
# Connect with custom settings
device = Bloomin8(
    host="10.0.0.41",
    port=8080,
    use_https=True,
    timeout=30.0,
    verify_ssl=True
)
```

### Access Raw Client

For operations not covered by the high-level API, you can access the underlying client:

```python
device = Bloomin8("10.0.0.41")
raw_client = device.client

# Use the raw client for advanced operations
from bloomin8_api.bloomin8_client.api.system_ap_is import get_whistle
result = get_whistle.sync_detailed(client=raw_client)
```

## Module Structure

```
bloomin8_api/
├── __init__.py                    # Main package exports
├── bloomin8.py                    # High-level Bloomin8 class
└── bloomin8_client/               # Auto-generated API client
    ├── client.py                  # Low-level client
    ├── errors.py                  # Error definitions
    ├── types.py                   # Type definitions
    ├── api/                       # API endpoints
    │   ├── gallery_ap_is/         # Gallery operations
    │   ├── image_ap_is/           # Image operations
    │   ├── playlist_ap_is/        # Playlist operations
    │   └── system_ap_is/          # System operations
    └── models/                    # Data models
```

## Best Practices

1. **Use the high-level API**: The `Bloomin8` class provides a clean, organized interface for most operations
2. **Handle exceptions**: Wrap API calls in try-except blocks for production code
3. **Use managers**: Access functionality through the appropriate manager (system, galleries, images, playlists)
4. **Pagination**: Use `offset` and `limit` parameters when retrieving large galleries
5. **Connection reuse**: Create one `Bloomin8` instance and reuse it for multiple operations

## Error Handling

```python
from bloomin8_api import Bloomin8

device = Bloomin8("10.0.0.41")

try:
    galleries = device.galleries.list()
    if galleries:
        print(f"Found {len(galleries)} galleries")
except Exception as e:
    print(f"Error: {e}")
```

## Command-Line Interface

The package includes a command-line script (`main.py`) for quick operations:

```bash
# List galleries on a device
python main.py --host 10.0.0.41 --verbose

# Use custom port
python main.py --host 10.0.0.41 --port 8080

# Use HTTPS
python main.py --host 10.0.0.41 --https
```

## Examples

See `examples.py` for a comprehensive demonstration of all API features.

## License

See LICENSE file for details.
