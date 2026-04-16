import os
import re
from datetime import datetime

SITEMAP_DIR = "/home/divineblisspuna/public_html/gorehospital.com/sitemap"

today = datetime.today().strftime("%Y-%m-%d")

for file in os.listdir(SITEMAP_DIR):
    if file.endswith(".xml"):
        path = os.path.join(SITEMAP_DIR, file)

        with open(path, "r") as f:
            content = f.read()

        content = re.sub(
            r"<lastmod>\d{4}-\d{2}-\d{2}</lastmod>",
            f"<lastmod>{today}</lastmod>",
            content
        )

        with open(path, "w") as f:
            f.write(content)

        print(f"Updated {file}")

print("All sitemap dates updated.")