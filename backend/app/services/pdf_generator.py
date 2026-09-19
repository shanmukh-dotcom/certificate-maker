import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_custom_fonts(fonts_list):
    for f in fonts_list:
        try:
            pdfmetrics.registerFont(TTFont(f.name, f.file_path))
        except Exception as e:
            print(f"Failed to register font {f.name}: {e}")

def generate_certificate_pdf(config: dict, data: dict, output_path: str, base_image_path: str = None):
    page_conf = config.get("page", {})
    width = page_conf.get("width_mm", 297) * mm
    height = page_conf.get("height_mm", 210) * mm
    
    c = canvas.Canvas(output_path, pagesize=(width, height))
    
    if base_image_path and os.path.exists(base_image_path):
        c.drawImage(base_image_path, 0, 0, width=width, height=height)
        
    elements = config.get("elements", [])
    for el in elements:
        if el.get("type") == "text":
            field = el.get("field")
            text = str(data.get(field, f"{{{{{field}}}}}"))
            
            x = el.get("x_mm", 0) * mm
            #
            # ymm inversion
            y_mm = el.get("y_mm", 0)
            y = height - (y_mm * mm)
            
            font_family = el.get("font_family", "Helvetica")
            font_size = el.get("font_size", 12)
            alignment = el.get("alignment", "left")
            auto_fit = el.get("auto_fit", False)
            box_width = el.get("width_mm", 0) * mm
            
            if auto_fit and box_width > 0:
                text_width = c.stringWidth(text, font_family, font_size)
                while text_width > box_width and font_size > 6:
                    font_size -= 1
                    text_width = c.stringWidth(text, font_family, font_size)
                    
            c.setFont(font_family, font_size)
            
            if alignment == "center":
                c.drawCentredString(x + (box_width / 2) if box_width else x, y, text)
            elif alignment == "right":
                c.drawRightString(x + box_width if box_width else x, y, text)
            else:
                c.drawString(x, y, text)
                
    c.showPage()
    c.save()

