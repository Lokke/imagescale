from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image, ImageOps
import io
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)  # Enable CORS for all routes

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
    
    # Custom bounding box calculation that respects alpha threshold
    # PIL's getbbox() might not work correctly with our alpha threshold logic
    width, height = white_img.size
    min_x, min_y, max_x, max_y = width, height, 0, 0
    
    # Find bounds of pixels that are truly opaque (alpha > alpha_threshold)
    pixels = list(white_img.getdata())
    found_content = False
    
    for y in range(height):
        for x in range(width):
            pixel_alpha = pixels[y * width + x][3]
            if pixel_alpha > alpha_threshold:  # Only consider pixels above threshold
                found_content = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    
    if not found_content:
        # If no content found, return empty transparent image
        result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        return result
    
    # Create custom bounding box
    bbox = (min_x, min_y, max_x + 1, max_y + 1)
    
    # Crop to content (tight crop around visible white pixels)
    cropped = white_img.crop(bbox)
    
    # Calculate scaling to fit in target size while maintaining aspect ratio
    crop_w, crop_h = cropped.size
    
    # Make it a square automatically
    if crop_w != crop_h:
        # Use the larger dimension to create a square
        max_dim = max(crop_w, crop_h)
        square_img = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
        x_offset = (max_dim - crop_w) // 2
        y_offset = (max_dim - crop_h) // 2
        square_img.paste(cropped, (x_offset, y_offset), cropped)
        cropped = square_img
        crop_w, crop_h = max_dim, max_dim
    
    # Scale to final size with high quality resampling
    scale = min(size / crop_w, size / crop_h)
    new_w = int(crop_w * scale)
    new_h = int(crop_h * scale)
    
    # Use the best resampling method for scaling down
    if scale < 1.0:
        # Scaling down - use LANCZOS for best quality
        resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    else:
        # Scaling up - use LANCZOS as well, but this should be rare now
        resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create final image with transparent background
    result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # Center the resized image
    x = (size - new_w) // 2
    y = (size - new_h) // 2
    result.paste(resized, (x, y), resized)
    
    return result

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
        img = Image.open(file.stream)
        
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
        return send_file(output, mimetype='image/png', as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': f'Image processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=8724)
else:
    # Production server (Gunicorn)
    pass
