#!/usr/bin/env python3
"""
Debug script for alpha threshold logic
"""

from PIL import Image
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from app import process_image

def create_test_image():
    """Create a test image: white center, gray border"""
    img = Image.new('RGB', (100, 100), 'gray')
    
    # Create white center
    for x in range(30, 70):
        for y in range(30, 70):
            img.putpixel((x, y), (255, 255, 255))
    
    return img.convert('RGBA')

def debug_alpha_threshold(threshold_value, alpha_threshold_value):
    """Debug the alpha threshold logic"""
    print(f"\n=== DEBUGGING: threshold={threshold_value}, alpha_threshold={alpha_threshold_value} ===")
    
    # Create test image
    test_img = create_test_image()
    print(f"Created test image: {test_img.size}")
    
    # Process with different alpha thresholds
    result = process_image(test_img, size=100, threshold=threshold_value, 
                          invert=False, alpha_threshold=alpha_threshold_value)
    
    # Analyze result
    pixels = list(result.getdata())
    
    # Count different alpha values
    alpha_counts = {}
    for pixel in pixels:
        alpha = pixel[3]
        alpha_counts[alpha] = alpha_counts.get(alpha, 0) + 1
    
    print(f"Alpha value distribution:")
    for alpha, count in sorted(alpha_counts.items()):
        print(f"  Alpha {alpha}: {count} pixels")
    
    # Find bounding box manually
    width, height = result.size
    min_x, min_y, max_x, max_y = width, height, 0, 0
    found_content = False
    
    for y in range(height):
        for x in range(width):
            pixel_alpha = pixels[y * width + x][3]
            if pixel_alpha > alpha_threshold_value:
                found_content = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    if found_content:
        bbox = (min_x, min_y, max_x + 1, max_y + 1)
        print(f"Custom bounding box: {bbox}")
        print(f"Width: {bbox[2] - bbox[0]}, Height: {bbox[3] - bbox[1]}")
    else:
        print("No content found!")
    
    # Compare with PIL's getbbox
    pil_bbox = result.getbbox()
    print(f"PIL bounding box: {pil_bbox}")
    
    return result

if __name__ == "__main__":
    print("ALPHA THRESHOLD DEBUGGING")
    print("=" * 50)
    
    # Test different alpha thresholds
    for alpha_thresh in [0, 30, 60, 100]:
        debug_alpha_threshold(50, alpha_thresh)
        
    print("\nDebugging complete!")
