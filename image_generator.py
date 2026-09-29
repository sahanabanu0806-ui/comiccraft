import requests
import os
from pathlib import Path
from PIL import Image
from io import BytesIO
import re
import time

PANELS_DIR = Path(__file__).resolve().parent.parent / "static" / "panels"
os.makedirs(PANELS_DIR, exist_ok=True)

def sanitize_filename(text):
    return re.sub(r'[^a-zA-Z0-9]', '_', text)[:50]

def generate_image(image_prompt, panel_num, art_style="anime"):
    try:
        safe_prompt = f"{image_prompt}, {art_style} art style, comic book panel, highly detailed"
        # Use Pollinations - FREE, no key, works on low RAM PC
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(safe_prompt)}?width=512&height=768&nologo=true&seed={panel_num}{int(time.time())%1000}"

        response = requests.get(url, timeout=60)
        response.raise_for_status()

        filename = f"panel_{panel_num}_{sanitize_filename(image_prompt)[:20]}.png"
        filepath = os.path.join(PANELS_DIR, filename)

        img = Image.open(BytesIO(response.content))
        img.save(filepath)
        print(f"Saved image: {filepath}")
        return f"/static/panels/{filename}"

    except Exception as e:
        print(f"Image gen error panel {panel_num}: {e}")
        # Create placeholder
        filename = f"panel_{panel_num}_placeholder.png"
        filepath = os.path.join(PANELS_DIR, filename)
        img = Image.new('RGB', (512, 768), color=(73, 109, 137))
        img.save(filepath)
        return f"/static/panels/{filename}"
