import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
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
    groups = ([i.text.replace(' ', ' ') for i in group_columns])
    groups_links = []
    for i in group_columns:
        link = i.get('href').split(' ')
        groups_links.append('https://расписание.нхтк.рф/' + link[0].replace(' ', '%C2%A0'))
    df = pd.DataFrame({
        'Name': groups[3:],
        'Link': groups_links[3:]})
    return df

if __name__ == '__main__':
    print(getScheduleNHTK_teachers())
