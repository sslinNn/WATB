import pandas as pd
from schedule.df2img import plot_dataframe, save_dataframe
from schedule.selected_schedule_parser import get_weekly_schedule_group
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
from schedule.table_styles import table_style

def df_to_png(df, output):
    new_df = weekday_division(df)
    row_count = len(new_df)
    colors = distant_colors(new_df)
    wigth = int((row_count * 21.25))
    fig = plot_dataframe(new_df, print_index=False,
                                fig_size=(1050, wigth),
                                col_width=[100, 600, 150, 50, 50, 100],
                         row_fill_colors=colors)
    save_dataframe(fig=fig, filename=output)


def weekday_division(df):
    arrays = df_to_array(df)
    column_names = arrays[0]
    data = arrays[1:]
    new_data = []
    for i in range(len(data)):
        if data[i][0] == data[i-1][0]:
            new_data.append(data[i])
        else:
            new_data.append(['', '', '', '', '', ''])
    res_df = pd.DataFrame(data, columns=column_names)
    return res_df


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
        elif 'Дьяченко' in row.TEACHER:
            colors.append('#F9F694')
        else:
            colors.append('#EBF0F8')
    return colors


if __name__ == '__main__':
    df = get_weekly_schedule_group('09.07.11')
    df_to_png(df, 'output/1.png')