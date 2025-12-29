# Refactoring Notes

## New File Structure

The `bloomin8_api` module has been refactored from a single 1095-line file into a modular structure:

```
bloomin8_api/
├── __init__.py           # Main package exports
├── client.py             # Bloomin8 main class (~200 lines)
├── types.py              # DeviceInfo, NetworkType (~170 lines)
├── bluetooth.py          # BLE wake functionality (~180 lines)
├── utils.py              # Error handling decorators (~50 lines)
├── managers/
│   ├── __init__.py       # Manager exports
│   ├── system.py         # SystemManager (~160 lines)
│   ├── gallery.py        # GalleryManager (~130 lines)
│   ├── image.py          # ImageManager (~170 lines)
│   └── playlist.py       # PlaylistManager (~110 lines)
└── bloomin8_client/      # Auto-generated API client (unchanged)
```

## Benefits

- **Modularity**: Each manager is self-contained and focused
- **Maintainability**: Easier to find and modify specific functionality
- **Testability**: Individual managers can be tested independently
- **Scalability**: Adding new features is clearer and simpler
- **Readability**: Files are 110-200 lines instead of 1095

## Public API

The public API remains unchanged. All imports still work:

```python
from bloomin8_api import Bloomin8, DeviceInfo, NetworkType
from bloomin8_api import wake_device_bluetooth, DeviceUnreachableError

device = Bloomin8("10.0.0.41")
device.system.get_device_info()
device.galleries.list()
device.images.upload_from_file("photo.jpg", "gallery")
device.playlists.create_or_update("playlist", data)
```

## What Changed Internally

1. **Moved classes to dedicated modules**:
   - `NetworkType`, `DeviceInfo` → `types.py`
   - `SystemManager` → `managers/system.py`
   - `GalleryManager` → `managers/gallery.py`
   - `ImageManager` → `managers/image.py`
   - `PlaylistManager` → `managers/playlist.py`
   - `Bloomin8` main class → `client.py`
   - BLE functions → `bluetooth.py`
   - `handle_connection_errors` → `utils.py`

2. **Updated imports**: All manager modules import from their new locations

3. **No breaking changes**: The public API surface is identical

## Old File

The original `bloomin8.py` file can be safely deleted as all functionality has been moved to the new structure.
