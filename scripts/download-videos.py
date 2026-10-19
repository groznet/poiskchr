#!/usr/bin/env python3
"""
Download YouTube videos and prepare for upload to files.groznet.com
"""

import json
import subprocess
import os
import sys
from pathlib import Path

def load_videos(json_path):
    """Load video data from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def download_videos(videos, output_dir='videos'):
    """Download all videos using yt-dlp"""
    Path(output_dir).mkdir(exist_ok=True)

    results = {
        'success': [],
        'failed': [],
        'skipped': []
    }

    for i, video in enumerate(videos, 1):
        title = video['title']
        video_id = video['url']
        yt_url = f"https://www.youtube.com/watch?v={video_id}"

        output_path = Path(output_dir) / f"{title}.mp4"

        # Skip if already downloaded
        if output_path.exists():
            print(f"[{i}/{len(videos)}] ⏭️  {title} (already exists)")
            results['skipped'].append(title)
            continue

        print(f"[{i}/{len(videos)}] ⬇️  Downloading {title}...")

        try:
            cmd = [
                'yt-dlp',
                '-f', 'bv*[height<=720]+ba/b[height<=720]/b',  # Max 720p
                '--merge-output-format', 'mp4',
                '--cookies-from-browser', 'chrome',
                '-o', str(output_path),
                yt_url
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"         ✅ Success")
                results['success'].append(title)
            else:
                print(f"         ❌ Failed: {result.stderr.strip()[-300:]}")
                results['failed'].append((title, result.stderr))

        except Exception as e:
            print(f"         ❌ Error: {str(e)[:100]}")
            results['failed'].append((title, str(e)))

    return results

def generate_updated_json(videos, base_url='https://files.groznet.com/poiskchr/videos'):
    """Generate updated JSON with permanent URLs"""
    updated = []
    for video in videos:
        title = video['title']
        video_id = video['url']
        # Keep original ID for reference, add permanent URL
        updated.append({
            'title': title,
            'url': video_id,  # Keep original ID
            'permanent_url': f"{base_url}/{title}.mp4"
        })
    return updated

def print_summary(results, videos):
    """Print download summary"""
    print("\n" + "="*60)
    print("📊 DOWNLOAD SUMMARY")
    print("="*60)
    print(f"✅ Successful: {len(results['success'])}")
    print(f"⏭️  Skipped:    {len(results['skipped'])}")
    print(f"❌ Failed:     {len(results['failed'])}")
    print(f"📹 Total:      {len(videos)}")

    if results['failed']:
        print("\n❌ Failed downloads:")
        for title, error in results['failed']:
            print(f"  - {title}: {error[:60]}")

    print("\n💾 Videos saved to: ./videos/")
    print("📤 Ready to upload to: https://files.groznet.com/poiskchr/videos/")

if __name__ == '__main__':
    json_path = 'themes/poiskchr/data/videos.json'

    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found")
        sys.exit(1)

    print("📂 Loading videos.json...")
    videos = load_videos(json_path)
    print(f"✅ Loaded {len(videos)} videos\n")

    print("⬇️  Starting downloads...\n")
    results = download_videos(videos)

    print_summary(results, videos)

    # Save updated JSON with permanent URLs
    updated_json = generate_updated_json(videos)
    with open('data/videos-updated.json', 'w', encoding='utf-8') as f:
        json.dump(updated_json, f, ensure_ascii=False, indent=2)
    print("\n📝 Updated JSON saved to: data/videos-updated.json")
    print("   (use this after uploading videos to files.groznet.com)")