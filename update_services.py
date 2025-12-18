
import glob
import re
import os

services_dir = r"d:\Gore 9-12-2025\services"
files = glob.glob(os.path.join(services_dir, "*.html"))

new_css = """/* ---------- Doctors grid ---------- */
    .doc-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 30px;
      margin: 40px 0 80px;
    }

    .doc-card {
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      position: relative;
      height: 100%;
      border: 1px solid rgba(0, 0, 0, 0.02);
    }

    .doc-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
    }

    .doc-photo {
      position: relative;
      width: 100%;
      aspect-ratio: 1 / 1;
      background: #f8f9fa;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .doc-photo img {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      display: block;
      transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .doc-card:hover .doc-photo img {
      transform: scale(1.08);
    }

    .doc-body {
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 6px;
      flex-grow: 1;
      background: #fff;
      z-index: 5;
      position: relative;
    }

    .doc-name {
      font-weight: 500;
      font-size: 19px;
      line-height: 1.3;
      margin: 0;
      color: #1a202c;
      letter-spacing: -0.3px;
    }

    .doc-spec {
      font-weight: 600;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #007bff;
      margin-top: 2px;
    }

    .doc-qual {
      font-size: 14px;
      color: #718096;
      margin: 0;
      line-height: 1.5;
      font-weight: 400;
    }

    .doc-card.no-image .doc-photo {
      background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
    }

    .doc-card.no-image .doc-photo img {
      display: none !important;
    }

    .scan-line {
      position: absolute;
      top: -10%;
      left: 0;
      width: 100%;
      height: 15%;
      background: linear-gradient(180deg,
          transparent 0%,
          rgba(255, 255, 255, 0.9) 50%,
          transparent 100%);
      filter: blur(4px);
      opacity: 0.7;
      z-index: 2;
      box-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    }

    .doc-card.no-image .doc-body {
      background: #ffffff;
      justify-content: flex-start;
      height: auto;
      min-height: 110px;
    }
"""

new_script = """    // Auto-detect generic images and convert to gradient cards
    (function () {
      const genericImages = ["01.jpg", "02.jpg", "03.jpg", "04.jpg"];
      const grid = document.querySelector(".doc-grid");
      if (!grid) return;

      const cards = Array.from(document.querySelectorAll(".doc-card"));

      const cardsWithImages = [];
      const cardsWithoutImages = [];

      cards.forEach((card) => {
        const img = card.querySelector(".doc-photo img");
        const imgSrc = img ? img.getAttribute("src") : "";
        const filename = imgSrc ? imgSrc.split("/").pop() : "";

        // Check if image is generic or empty
        if (genericImages.includes(filename) || !imgSrc || imgSrc === "#" || imgSrc.trim() === "") {
          card.classList.add("no-image");

          // Add scanner line animation if not present
          if (!card.querySelector('.scan-line')) {
              const scanLine = document.createElement('div');
              scanLine.className = 'scan-line';
              const photoDiv = card.querySelector('.doc-photo');
              if(photoDiv) photoDiv.appendChild(scanLine);
          }

          cardsWithoutImages.push(card);
        } else {
          cardsWithImages.push(card);
        }
      });

      // Clear the grid and reorder cards
      grid.innerHTML = "";
      cardsWithImages.forEach((card) => grid.appendChild(card));
      cardsWithoutImages.forEach((card) => grid.appendChild(card));
    })();"""

for file_path in files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue
    
    if 'doc-card' not in content:
        continue
    
    print(f"Updating {file_path}")
    
    # Update CSS
    css_pattern = re.compile(r'/\* ---------- Doctors grid ---------- \*/.*?(?=/\* Scroll reveal)', re.DOTALL)
    if css_pattern.search(content):
        content = css_pattern.sub(new_css, content)
    else:
        print(f"CSS pattern not found in {file_path}")

    # Update Script
    script_pattern = re.compile(r'(?:(?://\s*Auto-detect generic images)|(?:<!--\s*Doctor Cards Auto-conversion Script\s*-->)).*?\)\(\);', re.DOTALL)
    if script_pattern.search(content):
        content = script_pattern.sub(new_script, content)
    else:
        print(f"Script pattern not found in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
