import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
# from all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers
from bot.schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers
from datetime import datetime
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def convert_parse_date_to_normal_date(date):
    months = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12
    }
    parts = date.split(", ")
    day, month_name = parts[1].split()
    month = months[month_name]
    date = datetime(year=2023, month=month, day=int(day))
    formatted_date = date.strftime("%d.%m.%Y")
    return formatted_date


def get_weekly_schedule_group(name):
    df = getScheduleNHTK_groups()
    link = df[df['GroupName'] == name][['GroupLink']].values[0]
    requests.packages.urllib3.disable_warnings()
    response = requests.get(link[0], verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    schedule = soup.find('table', class_='расписание')
    time_lesson = soup.find_all('span', class_='время-подсказка без-переносов')
    days = []
    lesson_number = []
    retention_time = []
    lessons = []
    cabinet = []
    teachers = []
    for i in schedule:
        try:
            if i.get('class')[0] == 'дата':
                day = convert_parse_date_to_normal_date(i.text)
            if i.get('class')[0] == 'занятие':
                for j in i.find_next('td'):
                    lesson_number.append(j.text[0])
                    retention_time.append(j.text[1:])
                td = i.find_all('td')
                teachers.append(td[3].text.replace('\xad', '').replace('\xa0', ' '))
                lessons.append(td[2].text.replace('\xad', ''))
                cabinet.append(td[4].text)
                days.append(day)

        except Exception:
            pass
    df = pd.DataFrame({'DAY': days,
                       'LESSON': lessons,
                       'TEACHER': teachers,
                       'CAB': cabinet,
                       'N': lesson_number,
                       'TIME': retention_time})
    return df


def get_weekly_schedule_teacher(name):
    df = getScheduleNHTK_teachers()
    link = df[df['Name'] == name][[
        'Link']].values[0]
    requests.packages.urllib3.disable_warnings()
    response = requests.get(link[0], verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    schedule = soup.find('table', class_='расписание')
    time_lesson = soup.find_all('span', class_='время-подсказка без-переносов')
    days = []
    lesson_number = []
    retention_time = []
    group = []
    lessons = []
    cabinet = []

    for i in schedule:
        try:
            if i.get('class')[0] == 'дата':
                day = convert_parse_date_to_normal_date(i.text)
            if i.get('class')[0] == 'занятие':
                for j in i.find_next('td'):
                    lesson_number.append(j.text[0])
                    retention_time.append(j.text[1:])
                td = i.find_all('td')
                group.append(td[2].text.replace('\xad', ''))
                lessons.append(td[3].text.replace('\xad', ''))
                cabinet.append(td[4].text)
                days.append(day)

        except Exception:
            pass
        df = pd.DataFrame({'DAY': days,
                           'LESSON': lessons,
                           'GROUP': group,
                           'CAB': cabinet,
                           'N': lesson_number,
                           'TIME': retention_time})
    return df


def get_daily_schedule(name, date):
    import re
    pattern = r'\d{2}\.\d{2}\.\d{2}[A-Za-zА-Яа-я]?'
    pattern_in_message = re.findall(pattern, name)
    if name in pattern_in_message:
        df = get_weekly_schedule_group(name)
        schedule = df[df['DAY'] == date][[
            'DAY',
            'LESSON',
            'TEACHER',
            'CAB',
            'N',
            'TIME']]#.to_numpy()
        if len(schedule) == 0:
            return 'Указанная неверная дата или выходной'
        else:
            return schedule
    else:
        df = get_weekly_schedule_teacher(name)
        schedule = df[df['DAY'] == date][['DAY', 'LESSON', 'GROUP', 'CAB', 'N', 'TIME']]#.to_numpy()
        if len(schedule) == 0:
            return 'Указанная неверная дата или выходной'
        else:
            return schedule


def parse_all_subjects():
    df = getScheduleNHTK_teachers()
    iterator = 0
    result = []
    for i in df['Name']:
        teacher_df = get_weekly_schedule_teacher(i)
        for lesson in teacher_df['LESSON'].unique().tolist():
            result.append(lesson)
    return result


def parse_subject_teacher():
    df = getScheduleNHTK_teachers()
    iterator = 0
    result = {}
    for i in df['Name']:
        teacher_df = get_weekly_schedule_teacher(i)
        lessons = teacher_df['LESSON'].unique().tolist()
        k = 0
        for lesson in lessons:
            result[f'{i}/{k}'] = lesson
            k += 1
    return result



if __name__ == '__main__':
    print(datetime.now())
    print(parse_subject_teacher())
    print(datetime.now())