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
import io
from IPython.display import display, Image
from datetime import datetime


def df_to_png(df):
    new_df = weekday_division(df)
    new_df = add_weekday_to_df(new_df)
    row_count = len(new_df)
    row_size = 21.25
    if row_count < 7:
        row_count += 2
    wigth = int((row_count * row_size))
    colors = distant_colors(new_df)
    fig = plot_dataframe(new_df, print_index=False,
                                fig_size=(1050, wigth),
                                col_width=[100, 600, 150, 50, 50, 100],
                         row_fill_colors=colors)

    byte = save_dataframe_byte(fig)
    return byte


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
    for i in range(len(df['DAY'])):
        if df['DAY'].loc[i] == '':
            df['DAY'].loc[i] = weekday_by_date(df['DAY'].loc[i+1])
    return df



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
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    pdf = SimpleDocTemplate(file_path, pagesize=letter)
    addMapping('Arial', 0, 0, 'Arial')
    table = Table(array_of_arrays)
    ts = table_style
    table.setStyle(ts)

    elements = [table]
    pdf.build(elements)


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


if __name__ == '__main__':
    # df = get_daily_schedule(name='09.07.11', date='19.12.2023')
    df = get_weekly_schedule_group('09.07.11')
    png_bytes = df_to_png(df)

