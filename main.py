import datetime,imdb, requests
import time
from pprint import pprint
from bs4 import BeautifulSoup
from flask import Flask, render_template

ia = imdb.IMDb()
app = Flask(__name__)

def amondo(data):
    url = 'https://kinoamondo.pl/repertuar/'
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    links = soup.find_all('div', class_ = 'col-md-2 col-sm-3')
    links = [i.find('a')['href'] for i in links ]
    soup = soup.find(id=f'schedule-{data}')
    title_p = soup.find_all(class_ ='no-underline')
    title_p = [i.text for i in title_p]
    time = soup.find_all(class_='time')
    time = [i.text for i in time]
    title = []
    for i in range(0,len(title_p)):
        soup_2 = requests.get(links[i]).text
        soup_2 = BeautifulSoup(soup_2, 'html.parser')
        year = soup_2.find_all('ul', class_='movie-info')
        year = [i.find_all_next('li') for i in year]
        year = str(year[0][1])
        l = len(year)
        year = year[l-12:l-8]
        title.append(f'{title_p[i]} ({year})')
    return result(title, time, 'AMONDO')
def iluzjon():
    time = []
    title_p = []
    title = []
    help_l = []
    url = 'https://www.iluzjon.fn.org.pl/repertuar.html'
    soup = requests.get(url).text
    soup = BeautifulSoup(soup, 'html.parser')
    soup = soup.find(class_='box wide')
    soup = soup.table
    time_and_hour = soup.find_all(class_ = 'hour')
    time_and_hour = [i.text.split(' - ') for i in time_and_hour]
    for i in range(0, len(time_and_hour)):
        time.append(time_and_hour[i][0])
        title_p.append(time_and_hour[i][1])
    year = soup.find_all('i')
    year = [i.text.split(',') for i in year]
    for i in range(0,len(year), 1):
        try:
            int(year[i][-1])
            help_l.append(year[i][-1].strip())
        except ValueError:
            help_l.append('0')
    for i in range(0, len(title_p)):
        title.append(f'{title_p[i]} ({int(help_l[i])})')
    return result(title, time, 'ILUZJON')

def result(title, time, kino):
    cinema = {}
    for i in range(0, len(title), 1):
        help_l = {
            'rating': get_rating(title[i]),
            'time': time[i],
            'cinema': kino
        }
        cinema[title[i]] = help_l
    return cinema

def merge(dic_1, dic_2):
    cinema = {}
    for i in dic_1:
        for j in dic_2:
            if str(i) == str(j):
                help_l = {
                    'rating': dic_1[i]['reating'],
                    'time': f'AMONDO: {dic_1[i]['cinema']}; ILUZJON: {dic_2[j]['cinema']}',
                    'cinema': f'{dic_1[i]['cinema']} & {dic_2[j]['cinema']}'
                    }
                cinema[dic_1[i]['title']] = help_l
    updated = {**dic_1, **dic_2}
    final = {**updated, **cinema}
    return final

def get_rating(name):
    search = ia.search_movie(name)
    if len(search) == 0:
        return 'N/A'
    else:
        search = search[0].getID()
        rating = ia.get_movie(search)
        rating = rating.data['rating']
        return rating

@app.route('/')
def hello():
    return render_template('help.html')
@app.route('/final')
def final():
    data = datetime.datetime.now().date()
    AMONDO = amondo(data)
    ILUZJON = iluzjon()
    LISTA = merge(dic_1=AMONDO, dic_2 = ILUZJON)
    return render_template('index.html', post = LISTA)



if __name__ == '__main__':
    app.run(debug = True)

