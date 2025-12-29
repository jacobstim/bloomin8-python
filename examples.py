"""
Example usage of the Bloomin8 API

This file demonstrates how to use the Bloomin8 class to interact with a Bloomin8 device.
"""

from bloomin8_api import Bloomin8


def example_usage():
    """Demonstrate various operations with the Bloomin8 API."""
    
    # Initialize connection to the device
    device = Bloomin8("10.0.0.70")
    
    # Alternative: specify custom port and HTTPS
    # device = Bloomin8("10.0.0.70", port=8080, use_https=True)
    
    print("=" * 60)
    print("SYSTEM OPERATIONS")
    print("=" * 60)
    
    # Get device information
    print("\n1. Get Device Info:")
    device_info = device.system.get_device_info()
    if device_info:
        print(f"   Device info retrieved: {device_info}")
    
    # Get device state
    print("\n2. Get Device State:")
    state = device.system.get_state()
    if state:
        print(f"   Current state: {state}")
    
    # Clear screen (example - commented out for safety)
    # device.system.clear_screen()
    
    # Show next item
    # device.system.show_next()
    
    # Put device to sleep
    # device.system.sleep()
    
    # Reboot device 
    # device.system.reboot()
    
    print("\n" + "=" * 60)
    print("GALLERY OPERATIONS")
    print("=" * 60)
    
    # List all galleries
    print("\n3. List All Galleries:")
    galleries = device.galleries.list()
    if galleries:
        print(f"   Found {len(galleries)} gallery(ies)")
        for idx, gallery in enumerate(galleries, 1):
            print(f"   {idx}. Gallery ID: {getattr(gallery, 'id', 'N/A')}")
            if hasattr(gallery, 'name'):
                print(f"      Name: {gallery.name}")
            if hasattr(gallery, 'image_count'):
                print(f"      Images: {gallery.image_count}")
    
    # Get a specific gallery with its images
    print("\n4. Get Specific Gallery (example: 'my_gallery'):")
    # gallery = device.galleries.get("my_gallery", offset=0, limit=50)
    # if gallery:
    #     print(f"   Gallery data: {gallery}")
    print("   (Commented out - replace 'my_gallery' with actual gallery name)")
    
    # Get images from a gallery (convenience method)
    print("\n5. Get Images from Gallery (example: 'my_gallery'):")
    # images = device.galleries.get_images("my_gallery")
    # if images:
    #     print(f"   Found {len(images)} image(s)")
    #     for img in images:
    #         print(f"   - {img}")
    print("   (Commented out - replace 'my_gallery' with actual gallery name)")
    
    # Create or update a gallery
    print("\n6. Create/Update Gallery:")
    # gallery_data = {...}  # Gallery configuration
    # device.galleries.create_or_update("new_gallery", gallery_data)
    print("   (Commented out - provide gallery_data object)")
    
    # Delete a gallery
    print("\n7. Delete Gallery:")
    # device.galleries.delete("old_gallery")
    print("   (Commented out - use with caution)")
    
    print("\n" + "=" * 60)
    print("IMAGE OPERATIONS")
    print("=" * 60)
    
    # Upload a single image
    print("\n8. Upload Single Image:")
    # image_data = {...}  # Image upload data
    # device.images.upload(image_data)
    print("   (Commented out - provide image_data object)")
    
    # Upload multiple images
    print("\n9. Upload Multiple Images:")
    # multi_image_data = {...}  # Multiple image upload data
    # device.images.upload_multiple(multi_image_data)
    print("   (Commented out - provide multi_image_data object)")
    
    # Upload image data directly
    print("\n10. Upload Image Data:")
    # raw_image_data = {...}  # Raw image data
    # device.images.upload_data(raw_image_data)
    print("   (Commented out - provide raw image data)")
    
    # Delete an image
    print("\n11. Delete Image:")
    # device.images.delete(image="image.jpg", gallery="my_gallery")
    print("   (Commented out - provide image filename and gallery name)")
    
    print("\n" + "=" * 60)
    print("PLAYLIST OPERATIONS")
    print("=" * 60)
    
    # List all playlists
    print("\n12. List All Playlists:")
    playlists = device.playlists.list()
    if playlists:
        print(f"   Found {len(playlists)} playlist(s)")
        for idx, playlist in enumerate(playlists, 1):
            print(f"   {idx}. Playlist ID: {getattr(playlist, 'id', 'N/A')}")
            if hasattr(playlist, 'name'):
                print(f"      Name: {playlist.name}")
    
    # Get a specific playlist
    print("\n13. Get Specific Playlist (example: 'my_playlist'):")
    # playlist = device.playlists.get("my_playlist")
    # if playlist:
    #     print(f"   Playlist data: {playlist}")
    print("   (Commented out - replace 'my_playlist' with actual playlist name)")
    
    # Create or update a playlist
    print("\n14. Create/Update Playlist:")
    # playlist_data = {...}  # Playlist configuration
    # device.playlists.create_or_update("new_playlist", playlist_data)
    print("   (Commented out - provide playlist_data object)")
    
    # Delete a playlist
    print("\n15. Delete Playlist:")
    # device.playlists.delete("old_playlist")
    print("   (Commented out - use with caution)")
    
    print("\n" + "=" * 60)
    print("ADVANCED: Access to Raw Client")
    print("=" * 60)
    
    # Access the underlying client for advanced operations
    print("\n16. Access Raw Client:")
    raw_client = device.client
    print(f"   Raw client available: {raw_client}")
    print("   Use this for advanced operations not covered by the high-level API")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()
