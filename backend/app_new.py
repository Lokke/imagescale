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

def process_image(img, size=300, threshold=50, invert=False):
    """Process image: convert all colors to white, make transparent based on brightness"""
    # Convert to RGBA if not already
    img = img.convert('RGBA')
    
    # Convert to grayscale to measure brightness/darkness
    gray = img.convert('L')
    
    # Create result image: all visible pixels become white
    result_data = []
    gray_data = gray.getdata()
    
    for pixel_brightness in gray_data:
        # Apply inversion if requested
        if invert:
            pixel_brightness = 255 - pixel_brightness
            
        if pixel_brightness > threshold:
            # Bright enough → white pixel with full opacity
            result_data.append((255, 255, 255, 255))
        else:
            # Too dark → transparent
            # Optional: gradual transparency based on brightness
            alpha = max(0, min(255, int((pixel_brightness / threshold) * 255)))
            result_data.append((255, 255, 255, alpha))
    
    # Create new image with white + transparency
    white_img = Image.new('RGBA', img.size)
    white_img.putdata(result_data)
    
    # Get bounding box of non-transparent pixels
    bbox = white_img.getbbox()
    if not bbox:
        # If no content found, return empty transparent image
        result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        return result
    
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
    
    scale = min(size / crop_w, size / crop_h)
    new_w = int(crop_w * scale)
    new_h = int(crop_h * scale)
    
    # Resize with high quality
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
    version = request.form.get('version', 'normal')
    
    try:
        img = Image.open(file.stream)
        
        # Process with or without inversion
        if version == 'inverted':
            processed_img = process_image(img, size, threshold, invert=True)
            filename = f'band_logo_inverted_{size}x{size}.png'
        else:
            processed_img = process_image(img, size, threshold, invert=False)
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
