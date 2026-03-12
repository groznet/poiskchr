import os
import re

def reset_numbers_here():
    # 1. Look in the current directory (.)
    path = "."
    
    # 2. Find only folders starting with 'post-'
    folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.startswith('post-')]

    # 3. Sort them numerically so post-30 is first, then post-31, etc.
    folders.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)

    if not folders:
        print("No 'post-' folders found here.")
        return

    print(f"Resetting {len(folders)} folders...")

    # 4. Rename to temp names first (prevents collision if post-1 already exists)
    temp_pairs = []
    for i, folder in enumerate(folders, start=1):
        temp_name = f"temp_idx_{i}"
        os.rename(folder, temp_name)
        temp_pairs.append((temp_name, i))

    # 5. Final rename to post-1, post-2...
    for temp_name, index in temp_pairs:
        new_name = f"post-{index}"
        os.rename(temp_name, new_name)
        print(f"✅ {new_name}")

if __name__ == "__main__":
    reset_numbers_here()