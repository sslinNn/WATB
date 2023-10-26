from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import os
import fitz
from PIL import Image


from schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_teacher, get_weekly_schedule_group
from schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers


def df_to_array(df):
    column_name = [i for i in df]
    result = []
    result.append(column_name)
    for row in range(len(df.values)):
        string_elements = [str(element).strip('[]') for element in df.values[row]]
        bef_elements = [str(element).strip('[]') for element in df.values[row-1]]
        if bef_elements[0] != string_elements[0] and row != 0:
            local_list = []
            for i in range(len(string_elements)):
                local_list.append('')
            result.append(local_list)
        result.append(string_elements)
    return result


def df_to_pdf(df, file_path):
    array_of_arrays = df_to_array(df)

    #settings
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))  # Замените 'Arial.ttf' на путь к вашему шрифту
    addMapping('Arial', 0, 0, 'Arial')
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    table = Table(array_of_arrays)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Задний фон для заголовков
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Цвет текста для заголовков
        ('FONTNAME', (0, 0), (-1, 0), 'Arial'),  # Шрифт для заголовков
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Размер шрифта для заголовков
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Отступ снизу для заголовков
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Задний фон для остальных ячеек
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Рамка для ячеек
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Выравнивание по центру для ячеек
        ('FONTNAME', (0, 1), (-1, -1), 'Arial'),  # Шрифт для остальных ячеек
        ('FONTSIZE', (0, 1), (-1, -1), 8.5),  # Размер шрифта для остальных ячеек
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Выравнивание по вертикали для ячеек
    ])

    table.setStyle(table_style)

    # Добавление таблицы на документ
    elements = [table]
    pdf.build(elements)


def df_to_png(df):
    df_to_pdf(df, 'output/output.pdf')
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    pdf_document = fitz.open('output/output.pdf')
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()
        image.save(os.path.join(output_dir, 'output.png'), "PNG")
    pdf_document.close()
    transparent_png('output/output.png', 'output/output.png')
    cut_png('output/output.png', 'output/output.png')
    return 'output/output.png'


def transparent_png(png_before, png_after):
    image = Image.open(png_before)
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []
    for item in data:
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    image.putdata(new_data)
    image.save(png_after)
    image.close()


def cut_png(png_before, png_after):
    image = Image.open(png_before)
    non_transparent_coords = [(x, y) for x in range(image.width) for y in range(image.height) if
                              image.getpixel((x, y))[3] != 0]
    left, top = min(non_transparent_coords, key=lambda p: p[0] + p[1])
    right, bottom = max(non_transparent_coords, key=lambda p: p[0] + p[1])
    image = image.crop((left, top, right, bottom))
    image.save(png_after)
    image.close()


if __name__ == '__main__':
    df = get_weekly_schedule_group('09.07.11')
    df_to_png(df)
