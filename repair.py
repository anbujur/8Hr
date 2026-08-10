import re

filepath = r'c:\Users\AC\OneDrive - Cuculus India\Pictures\Automation-main\Screenshot-Automation\scrapper_new.py'

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Find the corrupted lines and remove them
fixed_lines = []
skip_corrupted = False
for i, line in enumerate(lines):
    # Skip lines with the corrupted escape sequence
    if '\"\"\")\n' in repr(line) or 'console.log' in line or 'getEventListeners' in line:
        skip_corrupted = True
        continue
    if skip_corrupted and ('# Secondary' in line or 'def _' in line):
        skip_corrupted = False
    if not skip_corrupted:
        fixed_lines.append(line)

content = ''.join(fixed_lines)

# Now replace the broken section with a clean version
pattern = r'def _find_refresh_button\(\):.*?return None\s+def _render_table_image'
clean_func = '''def _find_refresh_button():
        try:
            imgs = driver.find_elements(By.XPATH, "//img[contains(@class, 'icon')]")
            print(f"Found {len(imgs)} img.icon elements")
            for img in imgs:
                if img.is_displayed():
                    # Try to find parent button
                    try:
                        btn_xpaths = ["ancestor::button[1]", "ancestor::*[@role='button'][1]"]
                        for xpath in btn_xpaths:
                            parent = img.find_element(By.XPATH, xpath)
                            if parent and parent.is_displayed():
                                return parent
                    except:
                        pass
                    # Return img itself
                    return img
        except Exception as e:
            print(f"img search failed: {e}")
        
        # Fallback: find 3rd button in top area
        try:
            btns = driver.find_elements(By.XPATH, "//button | //div[@role='button']")
            visible_top = [b for b in btns if b.is_displayed() and b.location.get('y', 999) < 150]
            if len(visible_top) >= 3:
                return visible_top[2]
        except:
            pass
        return None

    def _render_table_image'''

content = re.sub(pattern, clean_func, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("File repaired successfully")
