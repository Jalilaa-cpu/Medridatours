#!/usr/bin/env python3
"""
Script to create a favicon from the company logo
"""
import os
from PIL import Image

def create_favicon():
    """Create favicon.ico from the company logo"""
    logo_path = "static/images/LOGO NOIR .jpg"
    favicon_path = "static/images/favicon.ico"
    
    if not os.path.exists(logo_path):
        print(f"Logo file not found: {logo_path}")
        return
    
    try:
        # Open the logo image
        with Image.open(logo_path) as img:
            # Convert to RGBA if necessary
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create different sizes for the favicon
            sizes = [(16, 16), (32, 32), (48, 48)]
            favicon_images = []
            
            for size in sizes:
                # Resize the image
                resized = img.resize(size, Image.Resampling.LANCZOS)
                favicon_images.append(resized)
            
            # Save as ICO file
            favicon_images[0].save(
                favicon_path,
                format='ICO',
                sizes=[(16, 16), (32, 32), (48, 48)],
                append_images=favicon_images[1:]
            )
            
            print(f"Favicon created successfully: {favicon_path}")
            
    except Exception as e:
        print(f"Error creating favicon: {e}")

if __name__ == "__main__":
    create_favicon()
