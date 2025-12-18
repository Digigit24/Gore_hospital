
import re
import os

file_path = r"d:\Gore 9-12-2025\index.html"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    print(f"Error reading {file_path}: {e}")
    exit(1)

# 1. Update CSS
new_css = """/* Doctor Card Styles from our-doctors.html */
    :root {
      --text: #1f1f25;
      --muted: #5b5b63;
      --card-bg: #ffffff;
      --card-bd: rgba(0, 0, 0, 0.06);
      --soft: 0 6px 24px rgba(0, 0, 0, 0.06);
      --soft-2: 0 12px 32px rgba(0, 0, 0, 0.07);
      --silver-gradient: linear-gradient(135deg,
          #f8f9fa 0%,
          #e9ecef 50%,
          #dee2e6 100%);
    }

    /* ---------- Doctors grid ---------- */
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
      /* Soft, premium shadow */
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
      /* Square - Professional & Consistent */
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
      /* Subtle zoom */
    }

    /* Details Section */
    .doc-body {
      padding: 24px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
      /* Center align for premium feel */
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
      /* Medical Blue accent */
      margin-top: 2px;
    }

    .doc-qual {
      font-size: 14px;
      color: #718096;
      margin: 0;
      line-height: 1.5;
      font-weight: 400;
    }

    /* ---------- Empty State (Creative & Professional) ---------- */
    .doc-card.no-image .doc-photo {
      background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
    }

    .doc-card.no-image .doc-photo img {
      position: static;
      width: 80px;
      height: 80px;
      opacity: 0.4;
      object-fit: contain;
      filter: grayscale(100%);
      animation: pulse-logo 3s infinite ease-in-out;
      display: block !important;
    }

    @keyframes pulse-logo {
      0% {
        opacity: 0.3;
        transform: scale(0.95);
      }

      50% {
        opacity: 0.5;
        transform: scale(1.05);
      }

      100% {
        opacity: 0.3;
        transform: scale(0.95);
      }
    }

    .doc-card.no-image .doc-photo img {
        display: none !important;
    }
    
    /* Ensure height for no-image cards */
    .doc-card.no-image {
        min-height: 400px; /* Force minimum height if flex layout fails */
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    /* The Scanner Bar Animation */
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

# CSS Regex: match between start marker and end marker
css_pattern = re.compile(r'/\*\s*Doctor Card Gradient Styles\s*\*/.*?/\*\s*Social Media Icons Styling\s*\*/', re.DOTALL)

if css_pattern.search(content):
    content = css_pattern.sub(new_css, content)
    print("Updated CSS")
else:
    print("CSS marker not found")


# 2. Update HTML Cards
# Pattern covers swiper-slide containing single-team-area-start
# Captured groups: 1=src, 2=name, 3=spec
html_pattern = re.compile(r'<div class="single-team-area-start">\s*<a href="our-doctors.html" class="thumbnail">\s*<img src="(.*?)" alt="team">\s*</a>\s*<div class="bottom">\s*<a href="our-doctors.html">\s*<h6 class="title">(.*?)</h6>\s*</a>\s*<p>\s*(.*?)\s*</p>\s*</div>\s*</div>', re.DOTALL)

def replace_card(match):
    src = match.group(1)
    name = match.group(2)
    spec = re.sub(r'\s+', ' ', match.group(3)).strip()
    
    # Handle placeholder images # or empty by creating standard doc-card structure
    # The JS will handle the no-image class addition, we just provide the structure.
    
    return f"""<article class="doc-card">
                            <div class="doc-photo">
                              <a href="our-doctors.html" style="display: block; width: 100%; height: 100%;">
                                <img src="{src}" alt="{name}">
                              </a>
                            </div>
                            <div class="doc-body">
                              <h3 class="doc-name"><a href="our-doctors.html" style="color: inherit; text-decoration: none;">{name}</a></h3>
                              <p class="doc-spec">{spec}</p>
                            </div>
                          </article>"""

if html_pattern.search(content):
    content = html_pattern.sub(replace_card, content)
    print("Updated HTML Cards")
else:
    print("HTML Card pattern not found")


# 3. Update JS script
new_script = """<!-- Doctor card gradient detection and reordering (UPDATED for doc-card) -->
  <script>
    (function () {
      const genericImages = ["01.jpg", "02.jpg", "03.jpg", "04.jpg"];
      const swiperWrapper = document.querySelector(
        ".team-swiper-container-h1 .swiper-wrapper"
      );

      if (!swiperWrapper) return;

      const slides = Array.from(
        swiperWrapper.querySelectorAll(".swiper-slide")
      );
      const slidesWithImages = [];
      const slidesWithoutImages = [];

      slides.forEach((slide) => {
        const card = slide.querySelector(".doc-card");
        if (!card) return; // Skip if no card found

        const img = slide.querySelector(".doc-photo img");
        const imgSrc = img ? img.getAttribute("src") : "";
        const filename = imgSrc ? imgSrc.split("/").pop() : "";

        // Check if image is generic or empty/hash
        if (genericImages.includes(filename) || imgSrc === "#" || imgSrc === "" || !imgSrc) {
          card.classList.add("no-image");
          
          // Add scanner line animation if not present
          if (!card.querySelector('.scan-line')) {
              const scanLine = document.createElement('div');
              scanLine.className = 'scan-line';
              const photoDiv = card.querySelector('.doc-photo');
              if(photoDiv) photoDiv.appendChild(scanLine);
          }

          slidesWithoutImages.push(slide);
        } else {
          slidesWithImages.push(slide);
        }
      });

      // Remove all slides
      slides.forEach((slide) => slide.remove());

      // Re-append in order: real images first
      slidesWithImages.forEach((slide) => swiperWrapper.appendChild(slide));
      slidesWithoutImages.forEach((slide) => swiperWrapper.appendChild(slide));
    })();
  </script>"""

js_pattern = re.compile(r'<!--\s*Doctor card gradient detection and reordering\s*-->.*?</script>', re.DOTALL)

if js_pattern.search(content):
    content = js_pattern.sub(new_script, content)
    print("Updated JS")
else:
    print("JS pattern not found, trying fallback matching")
    # Tring the existing content I saw in step 81
    fallback_pattern = re.compile(r'<script>\s*\(function \(\) \{\s*const genericImages = \["01\.jpg", "02\.jpg".*?\}\)\(\);\s*</script>', re.DOTALL)
    if fallback_pattern.search(content):
        content = fallback_pattern.sub(new_script, content)
        print("Updated JS (Fallback)")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
