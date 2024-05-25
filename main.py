import datetime, imdb, requests
import operator
from audioop import reverse
from concurrent.futures.thread import ThreadPoolExecutor
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

ia = imdb.IMDb()
list_without_duplicates = []
url_amondo = 'https://kinoamondo.pl/repertuar/'
url_iluzjon = 'https://www.iluzjon.fn.org.pl/repertuar.html'

DAYS = {
    'TODAY': [datetime.datetime.now().date(), 0],
    'TOMORROW': [datetime.datetime.now().date() + datetime.timedelta(1), 1],
    'DAY AFTER TOMORROW': [datetime.datetime.now().date() + datetime.timedelta(2), 2]
}
app = Flask(__name__)


def html(url):
    response = requests.get(url)
    return response.text


def fetch_info_amondo(url, time):
    soup = BeautifulSoup(html(url), 'html.parser')
    title_1 = soup.find('h1').text
    year_list = [i.find_all_next('li') for i in soup.find_all('ul', class_='movie-info')]
    try:
        year_string = str(year_list[0][1])
        year = year_string[len(year_string) - 12:len(year_string) - 8]
    except IndexError:
        year = '0000'
    rating = get_rating(f'{title_1} ({year})')
    return {'rating': rating, 'time': time, 'cinema': 'AMONDO', 'title': title_1, 'link': url}


def fetch_info_iluzjon(title, time, year):
    rating = get_rating(f'{title} ({year})')
    return {'rating': rating, 'time': time, 'cinema': 'ILUZJON', 'title': title, 'link': url_iluzjon}


def get_rating(title_and_year):
    try:
        info = ia.get_movie(ia.search_movie(title_and_year)[0].getID())
        rating = info.data['rating']
        return rating
    except KeyError:
        return ''
    except IndexError:
        return ''


def get_year(year):
    try:
        int(year[-1])
        return year[-1].strip()
    except ValueError:
        return '0000'


def amondo(number):
    lista = []
    req = html(url_amondo)
    soup = BeautifulSoup(req, 'html.parser')
    box = soup.find(id=f'schedule-{number}')
    links = [i.find('a')['href'] for i in box.find_all('div', class_='col-md-2 col-sm-3')]
    time = [i.text for i in box.find_all(class_='time')]
    if len(links) == 0:
        return []
    with ThreadPoolExecutor(len(links)) as executor:
        for result in executor.map(fetch_info_amondo, links, time):
            lista.append(result)
    return lista


def iluzjon(number):
    lista = []
    lista_2 = []
    box = BeautifulSoup(html(url_iluzjon), 'html.parser').find_all('table')[number]
    time_and_title = [i.text.split(' - ') for i in box.find_all(class_='hour')]
    time = [time_and_title[i][0] for i in range(0, len(time_and_title), 1)]
    title = [time_and_title[i][1] for i in range(0, len(time_and_title), 1)]
    year = [i.text.split(',') for i in box.find_all('i')]
    with ThreadPoolExecutor(len(title)) as executor:
        for result in executor.map(get_year, year):
            lista.append(result)
    with ThreadPoolExecutor(len(title)) as executor:
        for result in executor.map(fetch_info_iluzjon, title, time, lista):
            lista_2.append(result)
    return lista_2


def merge(Amondo, Iluzjon):
    Amondo.extend(Iluzjon)
    return Amondo


@app.route('/')
def front():
    return render_template('help.html')


@app.route('/final', methods=['GET', 'POST'])
def final():
    day = DAYS[request.args.get('day')]
    Amondo = amondo(day[0])
    Iluzjon = iluzjon(day[1])
    LISTA = merge(Amondo, Iluzjon)
    LISTA.sort(key=lambda x: str(x['rating']), reverse=True)
    return render_template('index.html', post=LISTA)


if __name__ == '__main__':
    app.run(debug=True)
