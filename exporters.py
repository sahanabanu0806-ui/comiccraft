import os
from fpdf import FPDF
from datetime import datetime
import requests
from PIL import Image

EXPORTS_DIR = "app/static/exports"
os.makedirs(EXPORTS_DIR, exist_ok=True)

class ComicPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ComicCraft - AI Comic', 0, 1, 'C')

def save_pdf(layout, character_name="Hero"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comic_{sanitize(character_name)}_{timestamp}.pdf"
    filepath = os.path.join(EXPORTS_DIR, filename)

    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}", ln=True, align='C')
        pdf.ln(5)

        # Image
        try:
            # image_path is /static/panels/xxx -> need real path
            real_img_path = panel['image_path'].replace("/static/", "app/static/")
            if os.path.exists(real_img_path):
                pdf.image(real_img_path, x=15, w=180)
            pdf.ln(5)
        except Exception as e:
            print(f"PDF image error: {e}")

        # Scene description
        pdf.set_font("Arial", "I", 11)
        pdf.multi_cell(0, 8, f"Scene: {panel['scene_description']}")
        pdf.ln(3)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, f"Caption: {panel['caption']}")
        pdf.ln(2)
        pdf.multi_cell(0, 8, f"Narration: {panel['narration']}")

    pdf.output(filepath)
    return f"/static/exports/{filename}", filepath

def sanitize(text):
    return "".join(c if c.isalnum() else "_" for c in text)[:20]
