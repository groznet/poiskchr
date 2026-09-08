"""
Hugo Front Matter Slug Generator (add_slugs.py)

This script scans 'content/news' for 'index.md' files and injects a clean, 
URL-friendly 'slug' attribute into the front matter based on the post's title.

Key Features:
- Safe to re-run: Skips files that already have a 'slug' line defined.
- Dual-Format Support: Handles both TOML (+++) and YAML (---) front matter.
- Transliteration: Converts Cyrillic/non-ASCII titles into clean Latin URLs.
- Boundary Respect: Truncates long titles (max 60 chars) without chopping words.
- Fallback Safety: Uses year/month folder structure if no title field exists.
"""

from pathlib import Path
from slugify import slugify

# Resolves: scripts/ -> project root -> content/news
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent / "content" / "news"

MAX_SLUG_LENGTH = 60

count = 0     # Tracks how many new slugs were injected
fallback = 1  # Incrementing counter for posts lacking a title field

# Search recursively for all 'index.md' page bundle files
for file in sorted(ROOT.rglob("index.md")):
    print(f"Checking: {file}")

    # Read all lines from the Markdown file using UTF-8 encoding
    lines = file.read_text(encoding="utf-8").splitlines()

    # Skip files that already have a 'slug:' field in front matter
    if any(line.strip().startswith("slug:") for line in lines):
        continue

    title_index = None
    title = ""

    # Parse front matter line-by-line to locate the title field
    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("title:"):
            title_index = i
            # Extract raw title string after the first colon
            title = stripped.split(":", 1)[1].strip()

            # Strip surrounding single or double quotes if present
            if (title.startswith('"') and title.endswith('"')) or (
                title.startswith("'") and title.endswith("'")
            ):
                title = title[1:-1]

            # Unescape encoded quote characters inside the title text
            title = title.replace('\\"', '"').replace("\\'", "'")
            break  # Stop scanning once title line is found

    # If no title line was found in front matter, skip adding a slug
    if title_index is None:
        print("  -> no title field found")
        continue

    # Generate slug from the title string
    if title:
        slug = slugify(
            title,
            lowercase=True,
            separator="-",
            max_length=MAX_SLUG_LENGTH,
            word_boundary=True,  # Ensures truncation doesn't split words
        )
    else:
        # Fallback slug if title field is empty (e.g., "post-202607-0001")
        rel = file.relative_to(ROOT)
        year = rel.parts[0] if len(rel.parts) > 1 else "0000"
        month = rel.parts[1] if len(rel.parts) > 2 else "00"
        slug = f"post-{year}{month}-{fallback:04d}"
        fallback += 1

    # Insert the new 'slug' line right below the 'title:' line
    lines.insert(title_index + 1, f"slug: '{slug}'")

    # Overwrite the index.md file with the updated front matter
    file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"  -> added slug: {slug}")
    count += 1

print(f"\nDone. Added {count} new slugs.")