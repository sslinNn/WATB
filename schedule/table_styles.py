from reportlab.platypus import TableStyle
from reportlab.lib import colors, styles



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
    ('FONTWEIGHT', (0, 0), (-1, -1), 'BOLD'),
])
