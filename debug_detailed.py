#!/usr/bin/env python3
"""
Detailed debug script for alpha threshold logic
"""

from PIL import Image
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def debug_pixel_processing():
    """Debug the exact pixel processing logic"""
    print("=== DETAILED PIXEL PROCESSING DEBUG ===")
    
    # Create simple test: white center, gray border
    img = Image.new('RGB', (5, 5), (128, 128, 128))  # Gray
    # White center pixel
    img.putpixel((2, 2), (255, 255, 255))  # White
    img = img.convert('RGBA')
    
    print("Original image:")
    for y in range(5):
        row = []
        for x in range(5):
            pixel = img.getpixel((x, y))
            row.append(f"RGB{pixel[:3]}")
        print("  " + " | ".join(row))
    
    # Convert to grayscale manually like in process_image
    gray = img.convert('L')
    print("\nGrayscale values:")
    for y in range(5):
        row = []
        for x in range(5):
            gray_val = gray.getpixel((x, y))
            row.append(f"{gray_val:3d}")
        print("  " + " | ".join(row))
    
    # Simulate our processing logic
    threshold = 50
    alpha_threshold = 60
    
    print(f"\nProcessing with threshold={threshold}, alpha_threshold={alpha_threshold}")
    print("Pixel-by-pixel analysis:")
    
    gray_data = list(gray.getdata())
    rgba_data = list(img.getdata())
    result_data = []
    
    for i, pixel_brightness in enumerate(gray_data):
        x = i % 5
        y = i // 5
        
        # Get original alpha channel
        original_alpha = rgba_data[i][3] if len(rgba_data[i]) == 4 else 255
        
        print(f"  Pixel ({x},{y}): brightness={pixel_brightness}, original_alpha={original_alpha}")
        
        # If original pixel was transparent or nearly transparent, keep it transparent
        if original_alpha <= alpha_threshold:
            final_alpha = 0
            print(f"    -> Original alpha too low, setting to 0")
        elif pixel_brightness > threshold:
            # Bright enough → white pixel with original opacity
            final_alpha = original_alpha
            print(f"    -> Bright enough, keeping alpha={final_alpha}")
        else:
            # Too dark → make transparent
            calculated_alpha = max(0, min(255, int((pixel_brightness / threshold) * 255)))
            final_alpha = min(calculated_alpha, original_alpha)
            print(f"    -> Too dark, calculated_alpha={calculated_alpha}, final_alpha={final_alpha}")
            
            # Check if calculated alpha would be too low
            test_alpha = int((pixel_brightness / threshold) * 255)
            if test_alpha <= alpha_threshold:
                final_alpha = 0
                print(f"    -> Test alpha {test_alpha} <= {alpha_threshold}, forcing to 0")
        
        # Final threshold check
        if final_alpha <= alpha_threshold:
            final_alpha = 0
            print(f"    -> Final alpha check: {final_alpha} <= {alpha_threshold}, setting to 0")
        
        result_data.append((255, 255, 255, final_alpha))
        print(f"    -> RESULT: Alpha = {final_alpha}")
    
    # Create result image
    result_img = Image.new('RGBA', (5, 5))
    result_img.putdata(result_data)
    
    print("\nFinal alpha values:")
    for y in range(5):
        row = []
        for x in range(5):
            pixel = result_img.getpixel((x, y))
            row.append(f"{pixel[3]:3d}")
        print("  " + " | ".join(row))

if __name__ == "__main__":
    debug_pixel_processing()
