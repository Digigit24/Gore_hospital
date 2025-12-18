
import glob
import re
import os

root_dir = r"d:\Gore 9-12-2025"
html_files = glob.glob(os.path.join(root_dir, "**/*.html"), recursive=True)

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
        continue
        
    original_content = content
    
    # Simple heuristic to identify hero/banner images to key as eager
    # We will look for images in the first 100 lines or within specific classes like "banner", "hero", "slider"
    
    def replacement(match):
        img_tag = match.group(0)
        
        # If already has loading attribute, skip
        if 'loading=' in img_tag:
            return img_tag
            
        # Heuristics to SKIP lazy loading (keep eager)
        # 1. Logo
        if 'logo' in img_tag.lower():
            return img_tag
            
        # 2. Hero/Banner classes (basic check)
        if 'banner' in img_tag.lower() or 'hero' in img_tag.lower() or 'slider' in img_tag.lower():
            return img_tag
            
        # 3. Very early in the file? (This script doesn't track line numbers easily in re.sub, 
        #    so we rely on class names mostly. However, standard optimization is "lazy load everything below the fold".)
        
        # Add loading="lazy"
        # Insert before the closing >
        return img_tag.replace('>', ' loading="lazy">', 1)

    # Regex for img tags
    # Matches <img [attributes] >
    img_pattern = re.compile(r'<img\s+[^>]*?>', re.IGNORECASE)
    
    new_content = img_pattern.sub(replacement, content)
    
    if new_content != original_content:
        # Save
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Optimized {file_path}")
        except Exception as e:
            print(f"Failed to save {file_path}: {e}")
