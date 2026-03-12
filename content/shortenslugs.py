import os

base = "news"

for year in os.listdir(base):
    year_path = os.path.join(base, year)
    if not os.path.isdir(year_path):
        continue

    for month in os.listdir(year_path):
        month_path = os.path.join(year_path, month)
        if not os.path.isdir(month_path):
            continue

        # Only keep directories (post folders)
        posts = [p for p in os.listdir(month_path) if os.path.isdir(os.path.join(month_path, p))]
        posts.sort()  # optional: sort alphabetically
        for i, post in enumerate(posts, 1):
            old = os.path.join(month_path, post)
            date_part = post[:10]  # assumes YYYY-MM-DD at the start
            new = os.path.join(month_path, f"{date_part}-post-{i}")
            print(f"Renaming:\n  {old}\n  -> {new}")
            os.rename(old, new)
