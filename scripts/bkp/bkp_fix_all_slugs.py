"""
Hugo News Directory Folder Renamer

This script scans 'content/news' for post directories containing 'index.md'.
If a directory name exceeds 30 characters or contains non-ASCII characters 
(e.g., Cyrillic text), it renames the folder to a clean 'post-N' format.

Behavior on repeated runs:
- Skips already formatted 'post-N' directories.
- Increments the index (e.g., 'post-3') for newly added posts to avoid collisions.
- Only renames directories; it does NOT modify the front matter inside 'index.md'.
"""

import os
import re

# Target root
NEWS_DIR = 'content/news'

def slugify(text):
    # If the slug is already 'post-something', we keep it
    if re.match(r'^post-\d+', text):
        return text
    return None

def fix_all_folders():
    if not os.path.exists(NEWS_DIR):
        print("News directory not found!")
        return

    for root, dirs, files in os.walk(NEWS_DIR):
        # We only want to rename the actual post folders (the ones containing index.md)
        if 'index.md' in files:
            parent = os.path.dirname(root)
            old_name = os.path.basename(root)
            
            # If the name is longer than 30 chars or contains non-ascii
            if len(old_name) > 30 or not old_name.isascii():
                # Find current count of folders in this specific month to assign a number
                existing_posts = [d for d in os.listdir(parent) if os.path.isdir(os.path.join(parent, d))]
                new_index = len([d for d in existing_posts if 'post-' in d]) + 1
                
                new_name = f"post-{new_index}"
                new_path = os.path.join(parent, new_name)
                
                # Handle collision if post-1 already exists
                while os.path.exists(new_path):
                    new_index += 1
                    new_name = f"post-{new_index}"
                    new_path = os.path.join(parent, new_name)

                print(f"Renaming: {old_name[:30]}... -> {new_name}")
                os.rename(root, new_path)

if __name__ == "__main__":
    print("🚀 Fixing long/Cyrillic folder names...")
    fix_all_folders()
    print("✅ Done! Now try running 'hugo server' again.")