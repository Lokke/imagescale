from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageOps
import io
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Enable CORS for all routes

# Global debug log collector
debug_logs = []

def debug_print(message):
    """Custom debug print that collects logs"""
    print(message)  # Still print to console
    debug_logs.append(message)

def clear_debug_logs():
    """Clear the debug log"""
    global debug_logs
    debug_logs = []

def get_debug_logs():
    """Get current debug logs"""
    return debug_logs.copy()

@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files from frontend folder"""
    return send_from_directory('../frontend', filename)

def process_image(img, size=300, threshold=50, invert=False, alpha_threshold=30):
    """Process image: convert all colors to white, make transparent based on brightness
    Uses high-resolution processing to avoid pixelation in larger outputs
    alpha_threshold: Pixels with alpha below this value become fully transparent (0-255)
    """
    
    # Convert to RGBA if not already
    img = img.convert('RGBA')
    
    # For better quality, process at higher resolution if the original is large enough
    # or if output size is large
    original_w, original_h = img.size
    max_original_dim = max(original_w, original_h)
    
    # Determine processing resolution - use at least 2x the output size or original size, whichever is larger
    processing_size = max(size * 2, max_original_dim, 1024)
    
    # Only upscale if original is significantly smaller than processing size
    if max_original_dim < processing_size * 0.8:
        # Upscale original image for better processing quality
        scale_factor = processing_size / max_original_dim
        new_w = int(original_w * scale_factor)
        new_h = int(original_h * scale_factor)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Convert to grayscale to measure brightness/darkness
    gray = img.convert('L')
    
    # Create result image: all visible pixels become white, preserve original transparency
    result_data = []
    gray_data = gray.getdata()
    rgba_data = img.getdata()
    
    alpha_threshold = alpha_threshold  # Use the parameter value instead of hardcoded
    
    for i, pixel_brightness in enumerate(gray_data):
        # Get original alpha channel
        original_alpha = rgba_data[i][3] if len(rgba_data[i]) == 4 else 255
        
        # If original pixel was transparent or nearly transparent, keep it transparent
        if original_alpha <= alpha_threshold:
            result_data.append((255, 255, 255, 0))
            continue
            
        # Apply inversion if requested
        if invert:
            pixel_brightness = 255 - pixel_brightness
            
        if pixel_brightness > threshold:
            # Bright enough → white pixel with original opacity
            final_alpha = original_alpha
        else:
            # Too dark → make transparent, but respect original transparency
            # Gradual transparency based on brightness for smoother edges
            calculated_alpha = max(0, min(255, int((pixel_brightness / threshold) * 255)))
            # Use the minimum of calculated and original alpha to preserve transparency
            final_alpha = min(calculated_alpha, original_alpha)
        
        # KRITISCH: Apply alpha threshold to ALL final results
        # This prevents grayscale areas from interfering with bounding box
        if final_alpha <= alpha_threshold:
            final_alpha = 0
        
        # ZUSÄTZLICH: Auch bei der Helligkeitsbewertung Alpha-Schwelle anwenden
        # Wenn das resultierende Alpha zu schwach wäre, mache Pixel komplett transparent
        if pixel_brightness <= threshold:
            # Für dunkle Pixel: Prüfe ob die berechnete Transparenz über der Schwelle liegt
            test_alpha = int((pixel_brightness / threshold) * 255)
            if test_alpha <= alpha_threshold:
                final_alpha = 0  # Komplett transparent wenn zu schwach
            
        result_data.append((255, 255, 255, final_alpha))
    
    # Create new image with white + transparency
    white_img = Image.new('RGBA', img.size)
    white_img.putdata(result_data)
    
    # Scale to final size FIRST, then apply bounding box logic
    # Calculate scaling to fit in target size while maintaining aspect ratio
    img_w, img_h = white_img.size
    scale = min(size / img_w, size / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    
    # Resize the processed image to target size
    if scale != 1.0:
        resized_img = white_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    else:
        resized_img = white_img
    
    # Create final canvas
    result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Center the resized image on canvas
    x_offset = (size - new_w) // 2
    y_offset = (size - new_h) // 2
    result.paste(resized_img, (x_offset, y_offset), resized_img)
    
    # NOW apply the new smart bounding box logic on the final result
    # Use alpha_threshold as brightness threshold (0-100 -> 150-240 mapping)
    # This ensures even high values still find bright content
    brightness_threshold = 150 + (alpha_threshold * 0.9)  # Map 0-100 to 150-240
    debug_print(f"Mapped alpha_threshold {alpha_threshold} to brightness_threshold {int(brightness_threshold)}")
    return apply_smart_bounding_box(result, size, int(brightness_threshold))

def apply_smart_bounding_box(img, target_size, brightness_threshold=200):
    """
    Apply smart bounding box that only considers very bright pixels
    with 5 pixel padding around the content
    """
    debug_print(f"Applying smart bounding box with brightness_threshold={brightness_threshold}")
    
    # Convert to grayscale to find bright pixels
    gray = img.convert('L')
    width, height = img.size
    
    # Find all very bright pixels (brightness > threshold)
    min_x, min_y, max_x, max_y = width, height, 0, 0
    found_bright = False
    
    for y in range(height):
        for x in range(width):
            # Check if pixel is bright enough and not transparent
            gray_val = gray.getpixel((x, y))
            alpha_val = img.getpixel((x, y))[3] if img.mode == 'RGBA' else 255
            
            if gray_val > brightness_threshold and alpha_val > 100:  # Bright and opaque
                found_bright = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    if not found_bright:
        debug_print(f"No pixels found above brightness {brightness_threshold}, trying fallback with 200")
        # Fallback: Try with lower threshold
        fallback_threshold = 200
        for y in range(height):
            for x in range(width):
                gray_val = gray.getpixel((x, y))
                alpha_val = img.getpixel((x, y))[3] if img.mode == 'RGBA' else 255
                
                if gray_val > fallback_threshold and alpha_val > 100:
                    found_bright = True
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
        
        if not found_bright:
            debug_print("Even fallback threshold failed, returning original")
            return img
        else:
            debug_print(f"Fallback successful with threshold {fallback_threshold}")
    
    # Add 5 pixel padding around bright content
    padding = 5
    crop_x1 = max(0, min_x - padding)
    crop_y1 = max(0, min_y - padding)
    crop_x2 = min(width, max_x + 1 + padding)
    crop_y2 = min(height, max_y + 1 + padding)
    
    crop_bbox = (crop_x1, crop_y1, crop_x2, crop_y2)
    debug_print(f"Bright pixel bounds: ({min_x}, {min_y}, {max_x}, {max_y})")
    debug_print(f"Crop with padding: {crop_bbox}")
    
    # Crop to bright content with padding
    cropped = img.crop(crop_bbox)
    
    # Make it square and center it
    crop_w, crop_h = cropped.size
    if crop_w != crop_h:
        max_dim = max(crop_w, crop_h)
        square_img = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
        x_center = (max_dim - crop_w) // 2
        y_center = (max_dim - crop_h) // 2
        square_img.paste(cropped, (x_center, y_center), cropped)
        cropped = square_img
    
    # Scale to final target size
    final_result = cropped.resize((target_size, target_size), Image.Resampling.LANCZOS)
    
    debug_print(f"Final result size: {final_result.size}")
    return final_result

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    # Get optional parameters
    size = int(request.form.get('size', 300))
    threshold = int(request.form.get('threshold', 50))
    alpha_threshold = int(request.form.get('alpha_threshold', 30))
    version = request.form.get('version', 'normal')
    
    try:
        clear_debug_logs()  # Clear previous logs
        img = Image.open(file.stream)
        debug_print(f"Original image size: {img.size}, mode: {img.mode}")
        debug_print(f"Parameters - size={size}, threshold={threshold}, alpha_threshold={alpha_threshold}")
        
        # Process with or without inversion
        if version == 'inverted':
            processed_img = process_image(img, size, threshold, invert=True, alpha_threshold=alpha_threshold)
            filename = f'band_logo_inverted_{size}x{size}.png'
        else:
            processed_img = process_image(img, size, threshold, invert=False, alpha_threshold=alpha_threshold)
            filename = f'band_logo_{size}x{size}.png'
            
        output = io.BytesIO()
        processed_img.save(output, format='PNG')
        output.seek(0)
        
        # Create response with debug logs
        response = send_file(output, mimetype='image/png', as_attachment=True, download_name=filename)
        
        # Add debug logs as custom header (JSON encoded)
        import json
        debug_data = json.dumps(get_debug_logs())
        response.headers['X-Debug-Logs'] = debug_data
        
        return response
    except Exception as e:
        debug_print(f"ERROR: {str(e)}")
        return jsonify({'error': f'Image processing failed: {str(e)}', 'debug_logs': get_debug_logs()}), 500

@app.route('/debug-logs', methods=['GET'])
def get_debug_logs_endpoint():
    """Get current debug logs as JSON"""
    return jsonify({'logs': get_debug_logs()})

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=8724)
else:
    # Production server (Gunicorn)
    pass
