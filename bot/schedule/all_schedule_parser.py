import pandas as pd
import requests
from bs4 import BeautifulSoup
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def getScheduleNHTK_groups():
    url = 'https://расписание.нхтк.рф/группы.html#заголовок'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    group_columns = soup.find_all('a')
    groups = ([i.text for i in group_columns if len(i.text) < 10])
    groups_links = (['https://расписание.нхтк.рф/' + i.text + '.html#заголовок' for i in group_columns if len(i.text) < 10])
    df = pd.DataFrame({
        'GroupName': groups[1:],
        'GroupLink': groups_links[1:]})
    return df


def getScheduleNHTK_teachers():
    url = 'https://расписание.нхтк.рф/преподаватели.html#заголовок'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    group_columns = soup.find_all('a')
    name = ([i.text.replace('\xa0', ' ') for i in group_columns])
    links = []
    for i in group_columns:
        link = i.get('href').split(' ')
        links.append('https://расписание.нхтк.рф/' + link[0].replace(' ', '%C2%A0'))
    df = pd.DataFrame({
        'Name': name[3:],
        'Link': links[3:]})
    return df




# if __name__ == '__main__':
#     NHTK_lesson_number_parser()