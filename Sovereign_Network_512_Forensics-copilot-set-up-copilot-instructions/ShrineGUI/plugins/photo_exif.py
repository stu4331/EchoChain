#!/usr/bin/env python3
"""Photo EXIF extraction plugin—light signatures revealed."""

import subprocess
import json
import os

class PhotoExifPlugin:
    @staticmethod
    def analyze(filepath=None):
        """Extract EXIF metadata from image vessels."""
        try:
            if not filepath:
                # Find images in uploads
                images = []
                uploads_dir = os.path.join('vault', 'uploads')
                if os.path.exists(uploads_dir):
                    for f in os.listdir(uploads_dir):
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff')):
                            images.append(os.path.join(uploads_dir, f))
                
                if not images:
                    return {"error": "No image relics found", "images_found": 0}
                
                filepath = images[0]
            
            # Try exiftool
            result = subprocess.run(
                ['exiftool', '-j', filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return {"success": True, "exif_data": data[0] if data else {}}
            else:
                return {"error": "exiftool not available or image has no EXIF data"}
        
        except FileNotFoundError:
            return {"error": "exiftool not installed", "install": "brew install exiftool (macOS) or apt-get install libimage-exiftool-perl (Linux)"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def extract_gps(filepath=None):
        """Extract GPS coordinates from image vessels."""
        try:
            result = subprocess.run(
                ['exiftool', '-GPSLatitude', '-GPSLongitude', filepath],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"gps_data": result.stdout}
            else:
                return {"error": "No GPS data inscribed"}
        except Exception as e:
            return {"error": str(e)}

# Register plugin
if __name__ != '__main__':
    from plugins.registry import register
    register('photo_exif', PhotoExifPlugin)
