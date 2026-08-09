"""
Hugo Remote Media Manifest Generator (generate_galleries.py)

This script scans Hugo page bundles in 'content/news/' for image assets.
For each post bundle, it generates a 'gallery.json' file mapping local image 
filenames to their corresponding remote CDN URLs on files.groznet.com.

Output JSON Structure:
- remote_base_url: The full CDN URL path pointing to the post's 'images/' directory.
- featured_image: Full CDN URL of the post's main/cover image (found in post root).
- images: Naturally sorted list of gallery filenames found in the 'images/' subfolder.
"""

import os
import json
import re

# ==========================================
# SITE CONFIGURATION
# ==========================================
SITE_SLUG = "poiskchr"                             # Unique identifier for the site on CDN
MEDIA_SERVER_BASE = "https://files.groznet.com"     # Base domain of the external media server
CONTENT_SECTION = "news"                            # Target Hugo content directory name

# Absolute path resolution relative to the script location (assumes script lives in a subfolder like 'scripts/')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, f"../content/{CONTENT_SECTION}"))

# Supported image formats for detection
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif', '.svg')


def natural_sort_key(s):
    """
    Sorts strings containing numbers in human/natural order.
    Example: Ensures 'image2.jpg' comes before 'image10.jpg' instead of lexicographical order.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def process_post(post_dir):
    """
    Scans a single post directory (page bundle), identifies local image assets,
    and writes a gallery.json file containing remote CDN mappings.
    """
    # Get relative path from content root (e.g., "2026/07/post-1") and normalize backslashes for URLs
    rel_post_path = os.path.relpath(post_dir, CONTENT_DIR).replace('\\', '/')
    
    # 1. Construct the base CDN URL path for this specific post
    post_remote_base = f"{MEDIA_SERVER_BASE}/{SITE_SLUG}/{CONTENT_SECTION}/{rel_post_path}"
    
    # 2. Locate the featured/cover image directly in the post root folder
    # (Ignores subdirectories like 'images/')
    featured_img_name = None
    for entry in os.scandir(post_dir):
        if entry.is_file() and entry.name.lower().endswith(IMAGE_EXTENSIONS):
            featured_img_name = entry.name
            break  # Grab the first image found in the root directory as the featured image
            
    # Construct full remote URL for featured image if one was found
    featured_img_url = f"{post_remote_base}/{featured_img_name}" if featured_img_name else ""

    # 3. Scan the 'images/' subfolder for secondary gallery images
    images_dir = os.path.join(post_dir, "images")
    gallery_images = []

    if os.path.exists(images_dir) and os.path.isdir(images_dir):
        for entry in os.scandir(images_dir):
            if entry.is_file() and entry.name.lower().endswith(IMAGE_EXTENSIONS):
                gallery_images.append(entry.name)

    # 4. Generate gallery.json if any image assets exist for this post
    if gallery_images or featured_img_url:
        # Sort gallery images naturally (1, 2, 10 instead of 1, 10, 2)
        gallery_images.sort(key=natural_sort_key)
        
        # Prepare JSON payload
        output_data = {
            "remote_base_url": f"{post_remote_base}/images/",
            "featured_image": featured_img_url,
            "images": gallery_images
        }

        # Write formatted JSON file into the post bundle folder
        json_path = os.path.join(post_dir, "gallery.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)

        print(f"✅ Generated: {CONTENT_SECTION}/{rel_post_path}/gallery.json ({len(gallery_images)} images)")


if __name__ == '__main__':
    print(f"🚀 Scanning local bundle media for site: [{SITE_SLUG}]...")
    
    # Sanity check: Ensure target content directory exists before running
    if not os.path.exists(CONTENT_DIR):
        print(f"❌ Error: Content directory not found at {CONTENT_DIR}")
        exit(1)

    # Traverse all directories in the content folder
    for root, dirs, files in os.walk(CONTENT_DIR):
        # Identify Hugo Page Bundles (directories containing .md files, excluding section indexes like '_index.md')
        if any(f.endswith('.md') and not f.startswith('_index') for f in files):
            process_post(root)