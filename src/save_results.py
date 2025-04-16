#save_results.py
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

RESULTS_DIR = "data"
TEMP_DIR = "temp"
FONTS_DIR = "fonts"
FONT_NAME = "Royal_Arial"

pdfmetrics.registerFont(TTFont(FONT_NAME, os.path.join(FONTS_DIR, "Royal_Arial.ttf")))

def _extract_section(lines, start_pattern, stop_on_blank=True, include_start=True):
    section = []
    collecting = False
    for line in lines:
        if not collecting:
            if start_pattern in line:
                collecting = True
                if include_start:
                    section.append(line.rstrip())
        else:
            if stop_on_blank and line.strip() == "":
                break
            section.append(line.rstrip())
    return section

def _extract_age_mortality(lines):
    section = []
    collecting = False
    for line in lines:
        if "Children:" in line or "Young Adults:" in line or "Middle Aged:" in line or "Senior:" in line:
            group_name = line.strip().split(":")[0]
            for next_line in lines[lines.index(line) + 1:]:
                if "Загальна кількість" in next_line:
                    total_deaths = next_line.strip()
                    section.append(f"{group_name}: {total_deaths}")
                    break
    return section

def save_results_to_pdf():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    txt_path = os.path.join(TEMP_DIR, "simulation_results.txt")
    if os.path.exists(txt_path):
        with open(txt_path, encoding="utf-8") as f:
            lines = f.readlines()
    else:
        lines = []

    text_pdf_path = os.path.join(RESULTS_DIR, "text_report.pdf")
    c_text = canvas.Canvas(text_pdf_path, pagesize=letter)
    width, height = letter

    if lines:
        text = c_text.beginText(40, height - 40)
        text.setFont(FONT_NAME, 10)
        for ln in lines:
            if text.getY() < 40:
                c_text.drawText(text)
                c_text.showPage()
                text = c_text.beginText(40, height - 40)
                text.setFont(FONT_NAME, 10)
            text.textLine(ln.rstrip())
        c_text.drawText(text)
    else:
        c_text.setFont(FONT_NAME, 10)
        c_text.drawString(40, height - 40, "simulation_results.txt не знайдено.")
    c_text.save()

    graphs_pdf_path = os.path.join(RESULTS_DIR, "charts_report.pdf")
    c_graphs = canvas.Canvas(graphs_pdf_path, pagesize=letter)

    specs = {
        "results.png": {
            "title": "Результати симуляції",
            "section": [lines[i].rstrip() for i in range(8) if i not in (1, 2)]
        },
        "population_gender_distribution.png": {
            "title": "Розподіл населення за статтю",
            "section": [ln.rstrip() for ln in lines
                        if ln.startswith("Кількість чоловіків") or ln.startswith("Кількість жінок")]
        },
        "gender_mortality.png": {
            "title": "Розподіл смертності за статтю",
            "section": _extract_section(lines, "Смертність за статтю (загалом):")
        },
        "age_mortality.png": {
            "title": "Динаміка смертності за віковими групами",
            "section": _extract_age_mortality(lines)
        },
        "age_gender_mortality.png": {
            "title": "Смертність за віковими групами і статтю",
            "section": _extract_section(lines, "Смертність за віковими групами:")
        },
        "infection_durations.png": {
            "title": "Середній час перебування в інфекції",
            "section": _extract_section(lines, "Середня тривалість інфекції")
        },
        "vaccine_quarantine_effects.png": {
            "title": "Ефект вакцинації та карантину",
            "section": list(dict.fromkeys(
                [ln.rstrip() for ln in lines
                 if ln.startswith("Вакциновано") or ln.startswith("Під карантином")]
                + _extract_section(lines, "Зменшення інфікування:")
                + _extract_section(lines, "Зменшення смертності:")
            ))
        },
        "cumulative_infected.png": {
            "title": "Кумулятивна кількість інфікованих",
            "section": [ln.rstrip() for ln in lines
                        if "інфікованих (накопичено)" in ln]
        },
        "peak_infected.png": {
            "title": "Пік інфекції",
            "section": [ln.rstrip() for ln in lines
                        if ln.startswith("Максимальна кількість інфікованих за день")]
        }
    }

    for img_name, spec in specs.items():
        img_path = os.path.join(TEMP_DIR, img_name)
        if not os.path.exists(img_path):
            continue

        c_graphs.setFont(FONT_NAME, 14)
        title_width = c_graphs.stringWidth(spec["title"], FONT_NAME, 14)
        c_graphs.drawString((width - title_width) / 2, height - 40, spec["title"])

        img = ImageReader(img_path)
        img_w, img_h = img.getSize()

        max_w = width - 80 
        scale = max_w / img_w 
        disp_w = img_w * scale
        disp_h = img_h * scale

        img_y = height - 80 - disp_h

        img_x = (width - disp_w) / 2

        c_graphs.drawImage(img, img_x, img_y, width=disp_w, height=disp_h)

        if spec["section"]:
            text = c_graphs.beginText(40, img_y - 20)
            text.setFont(FONT_NAME, 10)
            for ln in spec["section"]:
                if text.getY() < 40:
                    c_graphs.drawText(text)
                    c_graphs.showPage()
                    text = c_graphs.beginText(40, height - 40)
                    text.setFont(FONT_NAME, 10)
                text.textLine(ln)
            c_graphs.drawText(text)

        c_graphs.showPage()
    
    c_graphs.save()
    return text_pdf_path, graphs_pdf_path
