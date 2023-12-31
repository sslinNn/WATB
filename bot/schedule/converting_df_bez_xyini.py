import pandas as pd
from bot.schedule.df2img import plot_dataframe, save_dataframe, save_dataframe_byte
from bot.schedule.selected_schedule_parser import get_weekly_schedule_group, get_daily_schedule
from matplotlib.backends.backend_agg import FigureCanvasAgg
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
from bot.schedule.table_styles import table_style
from io import BytesIO
from IPython.display import display, Image
from datetime import datetime


def df_to_png(df):
    new_df = weekday_division(df)
    new_df, bold = add_weekday_to_df(new_df)
    bold_count = bold.count(True)
    row_count = len(df['DAY'])
    long_lesson_title = [1 for i in df['LESSON'] if len(i) > 65]
    row_count += (bold_count * 1.45) + 2 + (sum(long_lesson_title) * 1.22)
    row_size = 21
    height = int((row_count * row_size))
    colors = distant_colors(new_df)
    fig = plot_dataframe(new_df, print_index=False,
                                fig_size=(1050, height),
                                col_width=[100, 600, 150, 50, 50, 100],
                         row_fill_colors=colors,
                         text_thickness=12,
                         bold_rows=bold)
    byte_ = save_dataframe_byte(fig)
    return byte_

def weekday_division(df):
    arrays = df_to_array(df)
    column_names = arrays[0]
    data = arrays[1:]
    data.insert(0, ['', '', '', '', '', ''])
    res_df = pd.DataFrame(data, columns=column_names)
    return res_df


def weekday_by_date(date):
    date_object = datetime.strptime(date, "%d.%m.%Y")
    day_of_week = date_object.weekday()
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[day_of_week]


def add_weekday_to_df(df):
    bold = []
    for i in range(len(df['DAY'])):
        if df['DAY'].loc[i] == '':
            df['DAY'].loc[i] = weekday_by_date(df['DAY'].loc[i+1])
            bold.append(True)
        else:
            bold.append(False)
    return df, bold



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


def df_to_pdf(df):
    new_df = weekday_division(df)
    new_df, bold = add_weekday_to_df(new_df)
    pdf_buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    addMapping('Arial', 0, 0, 'Arial')
    table = Table([new_df.columns.tolist()] + new_df.values.tolist())
    ts = table_style
    table.setStyle(ts)
    elements = [table]
    pdf.build(elements)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_bytes


def distant_colors(df):
    colors = []
    for row in df.itertuples():
        if 'дист' in row.CAB:
            colors.append('#8AF5C4')
        elif 'ЭКЗАМЕН' in row.LESSON:
            colors.append('#E1707C')
        elif 'Дьяченко' in row[3]:
            colors.append('#F9F694')
        else:
            colors.append('#EBF0F8')
    return colors


def df_to_xlsx(df):
    excel_buffer = BytesIO()
    excel_writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')
    df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
    excel_writer.close()
    excel_data = excel_buffer.getvalue()
    return excel_data


if __name__ == '__main__':
    # df = get_daily_schedule(name='09.07.11', date='19.12.2023')
    df = get_weekly_schedule_group('09.07.11')
    png_bytes = df_to_xlsx(df)

