#!/usr/bin/env python3
"""
Command-line script to retrieve the list of images from a Bloomin8 device.

This script connects to a Bloomin8 device and retrieves the list of galleries
(which contain images) stored on the device.
"""

import argparse
import logging
import sys
from typing import Optional

from bloomin8_api import Bloomin8, DeviceUnreachableError, DeviceInfo

# Set up logger
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Retrieve information and galleries from a Bloomin8 device",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--host",
        default="10.0.0.70",
        help="IP address or hostname of the Bloomin8 device",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=80,
        help="Port number",
    )
    parser.add_argument(
        "--https",
        action="store_true",
        help="Use HTTPS instead of HTTP",
    )
    parser.add_argument(
        "--no-wakeup",
        action="store_true",
        help="Skip Bluetooth wake-up attempt (default: attempt wake-up)",
    )
    parser.add_argument(
        "--device-name",
        default="BLOOMIN8",
        help="Bluetooth device name to search for during wake-up",
    )
    parser.add_argument(
        "--ble-address",
        default=None,
        help="Bluetooth MAC address (skips scanning if provided)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    return parser.parse_args()


def display_device_info(device_info: DeviceInfo) -> None:
    """
    Display device information in a formatted manner.
    
    Args:
        device_info: DeviceInfo object to display
    """
    print("=" * 60)
    print("DEVICE INFORMATION")
    print("=" * 60)
    
    # Basic info
    if device_info.name:
        print(f"Device Name:      {device_info.name}")
    if device_info.version:
        print(f"Version:          {device_info.version}")
    
    # Hardware info
    if device_info.board_model:
        print(f"Board Model:      {device_info.board_model}")
    if device_info.screen_model:
        print(f"Screen Model:     {device_info.screen_model}")
    if device_info.width and device_info.height:
        print(f"Display Size:     {device_info.width} x {device_info.height}")
    
    # Network info
    if device_info.ip_address:
        print(f"IP Address:       {device_info.ip_address}")
    if device_info.ssid:
        print(f"WiFi SSID:        {device_info.ssid}")
    if device_info.network_type:
        print(f"Network Type:     {device_info.network_type}")
    
    # Storage info
    if device_info.total_size:
        total_gb = device_info.total_size / (1024**3)
        print(f"Total Storage:    {total_gb:.2f} GB")
    if device_info.free_size:
        free_gb = device_info.free_size / (1024**3)
        print(f"Free Storage:     {free_gb:.2f} GB")
    
    # Battery and power
    if device_info.battery is not None:
        print(f"Battery:          {device_info.battery}%")
    
    # Current display info
    if device_info.gallery:
        print(f"Current Gallery:  {device_info.gallery}")
    if device_info.image:
        print(f"Current Image:    {device_info.image}")
    if device_info.play_type is not None:
        play_types = {0: "Single Image", 1: "Gallery Slideshow", 2: "Playlist"}
        print(f"Play Type:        {play_types.get(device_info.play_type, f'Unknown ({device_info.play_type})')}")
    
    # Sleep settings
    if device_info.sleep_duration:
        sleep_hours = device_info.sleep_duration / 3600
        print(f"Sleep Duration:   {sleep_hours:.1f} hours")
    if device_info.max_idle:
        print(f"Max Idle Time:    {device_info.max_idle} seconds")
    
    print()


def display_galleries(galleries: list) -> None:
    """
    Display gallery list in a formatted manner.
    
    Args:
        galleries: List of gallery objects to display
    """
    print("=" * 60)
    print("GALLERIES")
    print("=" * 60)
    
    if not galleries:
        print("No galleries found on the device")
        return
    
    print(f"\nFound {len(galleries)} gallery(ies):\n")
    for idx, gallery in enumerate(galleries, 1):
        print(f"  Gallery {idx}:")
        if hasattr(gallery, "id"):
            print(f"    ID:     {gallery.id}")
        if hasattr(gallery, "name"):
            print(f"    Name:   {gallery.name}")
        if hasattr(gallery, "image_count"):
            print(f"    Images: {gallery.image_count}")
        print()
    
    print("=" * 60)


def display_gallery_images(device: Bloomin8, gallery) -> None:
    """Display images for a single gallery.
    
    Args:
        device: Bloomin8 device instance
        gallery: Single gallery object
    """
    gallery_name = gallery.name if hasattr(gallery, 'name') else gallery.id if hasattr(gallery, 'id') else "Unknown"
    
    print("=" * 60)
    print(f"IMAGES IN GALLERY: {gallery_name}")
    print("=" * 60)
    print()
    
    try:
        images = device.galleries.get_images(gallery_name)
        
        if images:
            print(f"  Total images: {len(images)}")
            print()
            for img_idx, image in enumerate(images, 1):
                print(f"  Image {img_idx}:")
                if hasattr(image, 'name'):
                    print(f"    Name: {image.name}")
                if hasattr(image, 'width') and hasattr(image, 'height'):
                    print(f"    Size: {image.width}x{image.height}")
                if hasattr(image, 'size'):
                    size_kb = image.size / 1024
                    print(f"    File Size: {size_kb:.2f} KB")
                print()
        else:
            print(f"  No images found")
            print()
    
    except Exception as e:
        print(f"  Error retrieving images: {e}")
        print()
    
    print("=" * 60)
    print()


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Configure logging based on verbosity
    # Set root logger to WARNING to suppress debug output from libraries
    logging.basicConfig(
        level=logging.WARNING,
        format='%(message)s'
    )
    
    # Configure main script logger based on verbose flag
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    
    # Suppress verbose output from third-party libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('bleak').setLevel(logging.WARNING)


    try:
        # Create the Bloomin8 device instance with BLE parameters
        device = Bloomin8(
            args.host,
            port=args.port,
            use_https=args.https,
            ble_name=args.device_name,
            ble_address=args.ble_address,
            logger=logger
        )

        # Attempt Bluetooth wake-up if not disabled
        if not args.no_wakeup:
            # Check if device is already awake with fast timeout
            logger.info("Checking if device is awake...")
            
            if device.is_awake():
                logger.info("-> Device is already awake, skipping Bluetooth wake-up.")
            else:
                logger.info("-> Device appears to be asleep, attempting Bluetooth wake-up...")
                device.wake_device()
                
                # Display discovered BLE address if available
                if device.ble_address:
                    logger.debug(f"-> BLE Address: {device.ble_address}")

        # Get and display device information
        logger.info(f"Retrieving device information from {args.host}:{args.port}...")

        device_info = device.system.get_device_info()
        if device_info:
            display_device_info(device_info)
        else:
            logger.error("Could not retrieve device information")
            print()

        # Get and display galleries
        galleries = device.galleries.list()
        if galleries is not None:
            display_galleries(galleries)
            # Display images for each gallery
            for gallery in galleries:
                display_gallery_images(device, gallery)
        else:
            logger.error("Failed to retrieve galleries from device")
            return 1

    except DeviceUnreachableError as e:
        logger.error(f"Error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
