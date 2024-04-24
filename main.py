from pprint import pprint

import requests
from bs4 import BeautifulSoup
cinema = {}

def amondo():
    url = 'https://kinoamondo.pl/repertuar/'
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    soup = soup.find(id='schedule-2024-04-24')
    title = soup.find_all(class_ ='no-underline')
    title = [i.text for i in title]
    time = soup.find_all(class_ = 'time')
    time = [i.text for i in time]
    wynik = result(title,time, 'AMONDO')
    return wynik
def iluzjon():
    url = 'https://www.iluzjon.fn.org.pl/repertuar.html'
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    soup = soup.find(class_='box wide')
    soup = soup.table
    time_and_hour = soup.find_all(class_ = 'hour')
    time_and_hour = [i.text.split(' - ') for i in time_and_hour]
    time = []
    title = []
    for i in range(0, len(time_and_hour)):
        time.append(time_and_hour[i][0])
        title.append(time_and_hour[i][1])
    wynik = result(title, time, 'ILUZJON')
    return wynik

def result(title, time, kino):
    cinema = {}
    for i in range(0, len(title), 1):
        help_l={}
        help_l['title'] = title[i]
        help_l['time'] = time[i]
        help_l['cinema'] = kino
        result = get_title(title[i])
        reating = get_reating(result)
        help_l['reating'] = 'N/A'
        cinema[title[i]] = help_l
    return cinema

def merge(dic_1, dic_2):
    final = {}
    for i in dic_1:
        for j in dic_2:
            if str(i) == str(j):
                help_l = {}
                help_l['title'] = dic_1[i]['title']
                help_l['time'] = dic_1[i]['time']
                help_l['cinema'] = f'{dic_1[i]['cinema']} & {dic_2[j]['cinema']}'
                help_l['reating'] = dic_1[i]['reating']
                cinema[dic_1[i]['title']] = help_l
    updated = {**dic_1, **dic_2}
    final = {**updated, **cinema}
    return final

def get_title(title):
    print(title)
    result = title.replace(' ', "_")
    return result

def get_reating(name):
    url = f'https://www.rottentomatoes.com/m/{name}'
    print(url)
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    #soup = soup.findAll('rt-link', {'theme':'medium'})
    #pprint(soup)

### TODO comparing dictionaries

AMONDO = amondo()
ILUZJON = iluzjon()
LISTA = merge(dic_1=AMONDO, dic_2=ILUZJON)
