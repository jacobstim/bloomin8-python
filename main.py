#!/usr/bin/env python3
"""
Bloomin8 Image Synchronization Tool

This script synchronizes images from a local folder to a Bloomin8 device.
It manages galleries and uploads images to keep the device in sync with your local collection.
"""

import argparse
import logging
import sys
import time
from pathlib import Path

from bloomin8_api import Bloomin8, DeviceUnreachableError

# Set up logger
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Synchronize images from a local folder to a Bloomin8 device",
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
        "--source",
        type=Path,
        required=True,
        help="Source folder containing images to sync",
    )
    parser.add_argument(
        "--gallery",
        default="bloomin8-sync",
        help="Gallery name to synchronize to on the device",
    )
    parser.add_argument(
        "--no-wakeup",
        action="store_true",
        help="Skip Bluetooth wake-up attempt (default: attempt wake-up)",
    )
    parser.add_argument(
        "--device-name",
        default="BLOOMIN8",
        help="Full or partial Bluetooth device name to search for during wake-up",
    )
    parser.add_argument(
        "--ble-address",
        default=None,
        help="Bluetooth MAC address (skips scanning if provided)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt and proceed with synchronization",
    )
    parser.add_argument(
        "--mirror",
        action="store_true",
        help="Mirror mode: delete images from device that are not in source folder",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    return parser.parse_args()


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

    # Validate source folder
    if not args.source.exists():
        logger.error(f"Source folder does not exist: {args.source}")
        return 1
    
    if not args.source.is_dir():
        logger.error(f"Source path is not a directory: {args.source}")
        return 1

    logger.info(f"Source folder: {args.source}")

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
            
            if device.is_awake(timeout=0.2):
                logger.info("-> Device is already awake, skipping Bluetooth wake-up.")
            else:
                logger.info("-> Device appears to be asleep, attempting Bluetooth wake-up...")
                device.wake_device()
                
                # Display discovered BLE address if available
                if device.ble_address:
                    logger.info(f"-> BLE Address: {device.ble_address}")

        # Get list of galleries from device
        logger.info(f"Connecting to {args.host}:{args.port}...")
        logger.info("Retrieving galleries from device...")
        galleries = device.galleries.list()
        
        target_gallery = None
        if galleries is not None:
            logger.info(f"Found {len(galleries)} gallery(ies) on device:")
            for gallery in galleries:
                
                # Check if this is our target gallery
                if gallery.name == args.gallery:
                    target_gallery = gallery
                    marker = " [TARGET]" 
                else:
                    marker = ""

                # Get image list per gallery
                try:
                    images = device.galleries.get_images(gallery.name)
                    image_count = len(images) if images else 0
                    logger.info(f"  - {gallery.name} ({image_count} images){marker}")
                except Exception as e:
                    logger.debug(f"  - {gallery.name} (could not retrieve image count: {e})")
                    logger.info(f"  - {gallery.name}{marker}")
        else:
            logger.error("Failed to retrieve galleries from device")
            return 1
        
        # Check if target gallery exists
        if target_gallery is None:
            logger.info(f"\nTarget gallery '{args.gallery}' not found on device.")
            device_images = []
        else:
            logger.info(f"\nTarget gallery '{args.gallery}' found on device.")
            # Get images from the target gallery
            try:
                device_images = device.galleries.get_images(args.gallery)
                logger.debug(f"Retrieved {len(device_images)} images from target gallery")
            except Exception as e:
                logger.error(f"Failed to retrieve images from target gallery: {e}")
                return 1

        # Scan local source folder for image files
        logger.info(f"\nScanning source folder: {args.source}")
        supported_extensions = {'.jpg', '.jpeg'}            # '.png', '.gif', '.bmp', '.webp'
        local_files = []
        
        for file_path in args.source.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                local_files.append(file_path)
        
        logger.info(f"-> Found {len(local_files)} image file(s) in source folder")

        # Create sets of filenames for comparison
        local_filenames = {f.name for f in local_files}
        device_filenames = {img.name for img in device_images if hasattr(img, 'name')}
        
        # Categorize files
        new_files = [f for f in local_files if f.name not in device_filenames]
        existing_files = [f for f in local_files if f.name in device_filenames]
        removed_files = [name for name in device_filenames if name not in local_filenames]
        
        # Display overview
        logger.info("\n" + "=" * 60)
        logger.info("SYNCHRONIZATION OVERVIEW")
        logger.info("=" * 60)
        
        # Show gallery creation notice if target gallery doesn't exist
        if target_gallery is None:
            logger.info(f"\nGallery to create: {args.gallery}")
        
        logger.info(f"\nNew files to upload ({len(new_files)}):")
        if new_files:
            for f in new_files:
                logger.info(f"  + {f.name}")
        else:
            logger.info("  (none)")
        
        logger.info(f"\nExisting files (already on device) ({len(existing_files)}):")
        if existing_files:
            for f in existing_files:
                logger.info(f"  = {f.name}")
        else:
            logger.info("  (none)")
        
        logger.info(f"\nFiles to remove from device ({len(removed_files)}):")
        if removed_files:
            for name in removed_files:
                logger.info(f"  - {name}")
        else:
            logger.info("  (none)")
        
        logger.info("\n" + "=" * 60)

        # Let's start from a clean slate
        has_failures = False

        # Do we need to delete files?
        files_to_delete = removed_files if args.mirror else []

        # So, do we have work?
        if not new_files and not files_to_delete:
            logger.info("\nNo changes to synchronize. Everything is up to date.")
        else:
            # We have work to do; ask for confirmation unless --force is used
            continue_sync = False
            if not args.force:
                # Prompt for confirmation
                try:
                    response = input("\nProceed with synchronization? [y/N]: ").strip().lower()
                    if response not in ['y', 'yes']:
                        logger.info("Synchronization cancelled.")
                        continue_sync = False;
                    else:
                        continue_sync = True;
                except (KeyboardInterrupt, EOFError):
                    logger.info("\nSynchronization cancelled.")
                    continue_sync = False;
            else:
                logger.info("\n--force flag set, proceeding without confirmation...")
                continue_sync = True

            # User agrees we need to do work, let's go!
            if continue_sync:
                # Start synchronization
                logger.info("\n" + "=" * 60)
                logger.info("STARTING SYNCHRONIZATION")
                logger.info("=" * 60)
                
                total_bytes = 0
                uploaded_count = 0
                deleted_count = 0
                start_time = time.time()
                
                # Delete removed files if mirror mode is enabled
                if args.mirror and removed_files:
                    logger.info(f"\nDeleting {len(removed_files)} removed file(s) from device...")
                    
                    for idx, filename in enumerate(removed_files, 1):
                        logger.info(f"\n[{idx}/{len(removed_files)}] Deleting {filename}...")
                        
                        try:
                            delete_start = time.time()
                            
                            # Delete the image using the delete API
                            response = device.images.delete(image=filename, gallery=args.gallery)
                            
                            delete_time = time.time() - delete_start
                            logger.info(f"    ✓ Deleted in {delete_time:.2f}s")
                            deleted_count += 1
                            
                        except Exception as e:
                            logger.error(f"    ✗ Failed to delete {filename}: {e}")
                
                # Upload new files
                if new_files:
                    logger.info(f"\nUploading {len(new_files)} new file(s)...")
                    
                    for idx, file_path in enumerate(new_files, 1):
                        file_size = file_path.stat().st_size
                        total_bytes += file_size
                        
                        # Create progress indicator
                        file_size_mb = file_size / (1024 * 1024)
                        logger.info(f"\n[{idx}/{len(new_files)}] Uploading {file_path.name} ({file_size_mb:.2f} MB)...")
                        
                        try:
                            upload_start = time.time()
                            
                            # Upload the image using the simplified API
                            response = device.images.upload_from_file(file_path, args.gallery)
                
                            upload_time = time.time() - upload_start
                            upload_speed = (file_size / 1024 / 1024) / upload_time if upload_time > 0 else 0                    
                            logger.info(f"    ✓ Uploaded in {upload_time:.2f}s ({upload_speed:.2f} MB/s)")
                            uploaded_count += 1
                            
                        except Exception as e:
                            logger.error(f"    ✗ Failed to upload {file_path.name}: {e}")
                
                # Calculate and display statistics
                total_time = time.time() - start_time
                
                logger.info("\n" + "=" * 60)
                logger.info("SYNCHRONIZATION COMPLETE")
                logger.info("=" * 60)
                
                logger.info(f"\nFiles uploaded: {uploaded_count}/{len(new_files)}")
                
                if args.mirror and removed_files:
                    logger.info(f"Files deleted: {deleted_count}/{len(removed_files)}")
                
                if total_time > 0 and total_bytes > 0:
                    total_mb = total_bytes / (1024 * 1024)
                    avg_speed_mbps = (total_mb / total_time) if total_time > 0 else 0
                    avg_speed_kbps = avg_speed_mbps * 1024
                    
                    logger.info(f"Total time: {total_time:.2f} seconds")
                    logger.info(f"Total data transferred: {total_mb:.2f} MB")
                    
                    if avg_speed_mbps >= 1:
                        logger.info(f"Average upload speed: {avg_speed_mbps:.2f} MB/s")
                    else:
                        logger.info(f"Average upload speed: {avg_speed_kbps:.2f} KB/s")
                
                # Check for failures
                has_failures = uploaded_count < len(new_files)
                if args.mirror and removed_files:
                    has_failures = has_failures or (deleted_count < len(removed_files))
                
                if has_failures:
                    if uploaded_count < len(new_files):
                        logger.warning(f"\nWarning: {len(new_files) - uploaded_count} file(s) failed to upload")
                    if args.mirror and removed_files and deleted_count < len(removed_files):
                        logger.warning(f"Warning: {len(removed_files) - deleted_count} file(s) failed to delete")
                
        # Put device back to sleep
        logger.info("\nPutting device to sleep...")
        try:
            device.system.sleep()
            logger.debug("-> Device is now sleeping.")
        except Exception as e:
            logger.warning(f"Failed to put device to sleep: {e}")
        
        return 1 if has_failures else 0

    except DeviceUnreachableError as e:
        logger.error(f"Error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
