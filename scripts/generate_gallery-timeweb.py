import os
import json
import requests
from bs4 import BeautifulSoup

# Configuration
BASE_REMOTE_URL = 'https://files.groznet.com/poiskchr/news/'
CONTENT_DIR = os.path.join(os.path.dirname(__file__), '../content/news')
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.gif')
FORCE_REFRESH = False
TARGET_YEAR = "2025"  # Set this to None if you want to scan EVERYTHING again

def is_image(filename):
    return filename.lower().endswith(IMAGE_EXTENSIONS)

def process_post(post_dir):
    json_path = os.path.join(post_dir, 'gallery.json')
    if not FORCE_REFRESH and os.path.exists(json_path):
        return

    rel_path = os.path.relpath(post_dir, CONTENT_DIR).replace('\\', '/')
    remote_images_url = f"{BASE_REMOTE_URL}{rel_path}/images/"
    
    try:
        response = requests.get(remote_images_url, timeout=5)
        if response.status_code != 200: return

        soup = BeautifulSoup(response.text, 'html.parser')
        images = [link.get('href').split('/')[-1] for link in soup.find_all('a') 
                  if link.get('href') and is_image(link.get('href'))]

        if images:
            images.sort(key=lambda x: [int(c) if c.isdigit() else c.lower() for c in filter(None, x.split('.'))])
            output = {
                "remote_base_url": remote_images_url,
                "featured_image": f"{BASE_REMOTE_URL}{rel_path}/feature.jpg",
                "images": images
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4)
            print(f"✅ Generated: {rel_path}/gallery.json")
    except Exception:
        pass

def walk_content(root_dir):
    # Get immediate subdirectories (the Year folders)
    years = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    
    for year in years:
        # If TARGET_YEAR is set, skip any folder that doesn't match
        if TARGET_YEAR and year != TARGET_YEAR:
            continue
            
        year_path = os.path.join(root_dir, year)
        print(f"📂 Scanning year: {year}...")
        
        for dirpath, dirnames, filenames in os.walk(year_path):
            if any(f.endswith('.md') for f in filenames):
                process_post(dirpath)

if __name__ == "__main__":
    print(f"🚀 Starting focused scan for {TARGET_YEAR if TARGET_YEAR else 'all years'}...")
    if os.path.exists(CONTENT_DIR):
        walk_content(CONTENT_DIR)