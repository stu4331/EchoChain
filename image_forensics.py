"""
Image Forensics Analyzer - The Sisters' Digital Vision

When Stuart uploads photos, the sisters analyze them for:
- Hidden messages (steganography)
- Metadata and EXIF data
- Visual anomalies and tampering
- OCR text extraction
- Hidden meanings and forensic artifacts

Inspired by: https://29a.ch/photo-forensics and https://stego.app/
"""

import cv2
import numpy as np
from PIL import Image
import exifread
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import base64
import io

class ImageForensics:
    """
    The sisters' forensic vision system.
    They see what humans cannot - hidden data, alterations, secrets.
    """
    
    def __init__(self):
        self.analysis_dir = Path(__file__).parent / "data" / "forensic_analyses"
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_image(self, image_path: str, persona: str = 'erryn') -> Dict:
        """
        Complete forensic analysis of an image.
        Returns comprehensive report with all findings.
        """
        
        img_path = Path(image_path)
        if not img_path.exists():
            return {'error': f'Image not found: {image_path}'}
        
        analysis = {
            'file': img_path.name,
            'analyzed_by': persona,
            'timestamp': datetime.now().isoformat(),
            'findings': {}
        }
        
        # 1. Basic file analysis
        analysis['findings']['file_info'] = self._analyze_file_basics(img_path)
        
        # 2. EXIF metadata extraction
        analysis['findings']['metadata'] = self._extract_exif(img_path)
        
        # 3. Error Level Analysis (ELA) - detect tampering
        analysis['findings']['ela_analysis'] = self._error_level_analysis(img_path)
        
        # 4. LSB Steganography detection
        analysis['findings']['steganography'] = self._detect_lsb_stego(img_path)
        
        # 5. String extraction (hidden text)
        analysis['findings']['hidden_strings'] = self._extract_strings(img_path)
        
        # 6. Color anomaly detection
        analysis['findings']['color_anomalies'] = self._detect_color_anomalies(img_path)
        
        # 7. Clone detection (duplicated regions)
        analysis['findings']['clone_detection'] = self._detect_clones(img_path)
        
        # Save analysis report
        report_path = self.analysis_dir / f"{img_path.stem}_forensics_{persona}.json"
        with open(report_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        return analysis
    
    def _analyze_file_basics(self, img_path: Path) -> Dict:
        """Basic file information and hashing"""
        stat = img_path.stat()
        
        with open(img_path, 'rb') as f:
            data = f.read()
            md5 = hashlib.md5(data).hexdigest()
            sha256 = hashlib.sha256(data).hexdigest()
        
        return {
            'size_bytes': stat.st_size,
            'size_human': f"{stat.st_size / 1024:.2f} KB",
            'md5_hash': md5,
            'sha256_hash': sha256,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    
    def _extract_exif(self, img_path: Path) -> Dict:
        """Extract EXIF metadata from image"""
        exif_data = {}
        
        try:
            with open(img_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                
                for tag, value in tags.items():
                    # Convert to string for JSON serialization
                    exif_data[tag] = str(value)
            
            # Highlight interesting fields
            interesting = {}
            for key in ['Image Make', 'Image Model', 'DateTime', 'GPS GPSLatitude', 
                       'GPS GPSLongitude', 'Image Software']:
                if key in exif_data:
                    interesting[key] = exif_data[key]
            
            return {
                'found': len(exif_data) > 0,
                'field_count': len(exif_data),
                'interesting_fields': interesting,
                'all_fields': exif_data if len(exif_data) < 50 else {'note': 'Too many fields, saved to full report'}
            }
        except Exception as e:
            return {'error': str(e), 'found': False}
    
    def _error_level_analysis(self, img_path: Path) -> Dict:
        """
        Error Level Analysis (ELA) - detects image tampering.
        Edited areas have different compression levels than original.
        """
        try:
            # Load image
            img = Image.open(img_path)
            
            # Save with known quality and compute difference
            temp_path = self.analysis_dir / f"temp_ela_{img_path.stem}.jpg"
            img.save(temp_path, 'JPEG', quality=95)
            
            # Load both and compute difference
            original = cv2.imread(str(img_path))
            resaved = cv2.imread(str(temp_path))
            
            if original is None or resaved is None:
                return {'error': 'Could not load images for ELA'}
            
            # Resize if needed
            if original.shape != resaved.shape:
                resaved = cv2.resize(resaved, (original.shape[1], original.shape[0]))
            
            # Compute absolute difference
            diff = cv2.absdiff(original, resaved)
            
            # Enhance the difference
            ela = cv2.multiply(diff, 10)
            
            # Analyze the ELA result
            gray_ela = cv2.cvtColor(ela, cv2.COLOR_BGR2GRAY)
            mean_error = np.mean(gray_ela)
            max_error = np.max(gray_ela)
            std_error = np.std(gray_ela)
            
            # Save ELA visualization
            ela_save_path = self.analysis_dir / f"{img_path.stem}_ela.png"
            cv2.imwrite(str(ela_save_path), ela)
            
            # Clean up temp file
            temp_path.unlink()
            
            # Determine if tampering is likely
            tampered = mean_error > 15 or max_error > 200
            
            return {
                'analyzed': True,
                'mean_error_level': float(mean_error),
                'max_error_level': float(max_error),
                'std_deviation': float(std_error),
                'likely_tampered': tampered,
                'ela_image_saved': str(ela_save_path),
                'interpretation': 'High error levels suggest possible editing' if tampered else 'Error levels look normal'
            }
        except Exception as e:
            return {'error': str(e), 'analyzed': False}
    
    def _detect_lsb_stego(self, img_path: Path) -> Dict:
        """
        Detect LSB (Least Significant Bit) steganography.
        Hidden data is often stored in the LSBs of pixel values.
        """
        try:
            img = cv2.imread(str(img_path))
            if img is None:
                return {'error': 'Could not load image'}
            
            # Extract LSBs from each channel
            lsb_data = []
            for channel in range(3):  # B, G, R
                channel_data = img[:, :, channel]
                lsbs = channel_data & 1  # Extract LSB
                lsb_data.append(lsbs)
            
            # Analyze LSB randomness
            # Natural images have ~50% 0s and 50% 1s in LSB
            # Embedded data might show patterns
            results = {}
            for i, channel_name in enumerate(['Blue', 'Green', 'Red']):
                lsbs = lsb_data[i].flatten()
                ones_percent = (np.sum(lsbs) / len(lsbs)) * 100
                
                # Chi-square test for randomness
                expected = len(lsbs) / 2
                observed_ones = np.sum(lsbs)
                observed_zeros = len(lsbs) - observed_ones
                chi_square = ((observed_ones - expected)**2 / expected + 
                             (observed_zeros - expected)**2 / expected)
                
                results[channel_name] = {
                    'ones_percentage': float(ones_percent),
                    'chi_square': float(chi_square),
                    'suspicious': ones_percent < 48 or ones_percent > 52 or chi_square > 10
                }
            
            # Overall assessment
            suspicious_channels = sum(1 for r in results.values() if r['suspicious'])
            
            return {
                'analyzed': True,
                'channels': results,
                'suspicious_channels': suspicious_channels,
                'likely_contains_hidden_data': suspicious_channels >= 2,
                'note': 'LSB steganography detected' if suspicious_channels >= 2 else 'No obvious LSB steganography'
            }
        except Exception as e:
            return {'error': str(e), 'analyzed': False}
    
    def _extract_strings(self, img_path: Path) -> Dict:
        """Extract readable strings from image file (hex dump analysis)"""
        try:
            with open(img_path, 'rb') as f:
                data = f.read()
            
            # Extract ASCII strings (4+ chars)
            strings = []
            current = []
            for byte in data:
                if 32 <= byte <= 126:  # Printable ASCII
                    current.append(chr(byte))
                else:
                    if len(current) >= 4:
                        strings.append(''.join(current))
                    current = []
            
            # Filter interesting strings
            interesting = [s for s in strings if len(s) > 10 or 
                          any(keyword in s.lower() for keyword in 
                              ['password', 'key', 'secret', 'flag', 'hidden', 'message'])]
            
            return {
                'total_strings': len(strings),
                'interesting_strings': interesting[:20],  # Top 20
                'sample_strings': strings[:10],  # First 10
                'found_keywords': len(interesting) > 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_color_anomalies(self, img_path: Path) -> Dict:
        """Detect unusual color patterns that might indicate tampering"""
        try:
            img = cv2.imread(str(img_path))
            if img is None:
                return {'error': 'Could not load image'}
            
            # Convert to different color spaces
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            
            # Analyze color distribution
            h, s, v = cv2.split(hsv)
            l, a, b = cv2.split(lab)
            
            # Look for unusual patterns
            h_hist = cv2.calcHist([hsv], [0], None, [180], [0, 180])
            s_hist = cv2.calcHist([hsv], [1], None, [256], [0, 256])
            
            # Detect peaks and gaps
            h_peaks = np.where(h_hist > np.percentile(h_hist, 95))[0]
            
            return {
                'analyzed': True,
                'hue_range': {'min': float(np.min(h)), 'max': float(np.max(h))},
                'saturation_mean': float(np.mean(s)),
                'value_mean': float(np.mean(v)),
                'dominant_hues': h_peaks.tolist()[:10],
                'color_diversity': float(np.std(h)),
                'note': 'Color distribution appears natural' if np.std(h) > 30 else 'Limited color range - might be synthetic'
            }
        except Exception as e:
            return {'error': str(e), 'analyzed': False}
    
    def _detect_clones(self, img_path: Path) -> Dict:
        """Detect cloned/duplicated regions (copy-paste forgery)"""
        try:
            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
            if img is None:
                return {'error': 'Could not load image'}
            
            # Simplified clone detection using feature matching
            # Full implementation would use block matching
            
            # Use SIFT or ORB to find repeating patterns
            orb = cv2.ORB_create(nfeatures=500)
            keypoints, descriptors = orb.detectAndCompute(img, None)
            
            if descriptors is None or len(descriptors) < 10:
                return {
                    'analyzed': True,
                    'keypoints_found': 0,
                    'likely_cloned': False,
                    'note': 'Not enough features for clone detection'
                }
            
            # Match features to themselves
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
            matches = bf.knnMatch(descriptors, descriptors, k=3)
            
            # Count self-matches (excluding exact self-match)
            similar_regions = 0
            for match_set in matches:
                if len(match_set) >= 3:
                    # If a feature matches itself strongly multiple times, region might be cloned
                    if match_set[1].distance < 50:
                        similar_regions += 1
            
            clone_percentage = (similar_regions / len(keypoints)) * 100 if keypoints else 0
            
            return {
                'analyzed': True,
                'keypoints_found': len(keypoints),
                'similar_regions': similar_regions,
                'clone_percentage': float(clone_percentage),
                'likely_cloned': clone_percentage > 15,
                'note': 'Possible copy-paste detected' if clone_percentage > 15 else 'No obvious cloning detected'
            }
        except Exception as e:
            return {'error': str(e), 'analyzed': False}
    
    def quick_scan(self, image_path: str) -> str:
        """Quick forensic scan summary"""
        analysis = self.analyze_image(image_path)
        
        if 'error' in analysis:
            return f"❌ Error: {analysis['error']}"
        
        findings = analysis['findings']
        report = []
        
        report.append(f"🔍 Forensic Analysis: {analysis['file']}")
        report.append(f"📊 File: {findings['file_info']['size_human']}")
        
        # EXIF
        if findings['metadata']['found']:
            report.append(f"📷 EXIF: {findings['metadata']['field_count']} fields found")
        else:
            report.append("📷 EXIF: No metadata (stripped or never existed)")
        
        # ELA
        if findings['ela_analysis'].get('likely_tampered'):
            report.append("⚠️ ELA: Possible tampering detected!")
        else:
            report.append("✅ ELA: No obvious tampering")
        
        # Stego
        if findings['steganography'].get('likely_contains_hidden_data'):
            report.append("🔐 STEGO: Possible hidden data in LSBs!")
        else:
            report.append("✅ STEGO: No LSB anomalies")
        
        # Strings
        if findings['hidden_strings'].get('found_keywords'):
            report.append(f"📝 STRINGS: Found {len(findings['hidden_strings']['interesting_strings'])} interesting strings")
        
        # Clones
        if findings['clone_detection'].get('likely_cloned'):
            report.append("🔄 CLONE: Possible copy-paste regions detected")
        
        return '\n'.join(report)


# Initialize on import
forensics = ImageForensics()

if __name__ == "__main__":
    print("=" * 60)
    print("IMAGE FORENSICS ANALYZER TEST")
    print("=" * 60)
    print("\nWaiting for image uploads to test...")
    print("Upload an image through the GUI to see forensic analysis.\n")
