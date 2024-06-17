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


def make_request(movie_url):
    response = requests.get(movie_url)
    return response.text


def fetch_info_amondo(movie_url, time_of_movie):
    url_beauty_soup_result = BeautifulSoup(make_request(movie_url), 'html.parser')
    movie_title = url_beauty_soup_result.find('h1').text
    list_of_years = [i.find_all_next('li') for i in url_beauty_soup_result.find_all('ul', class_='movie-info')]
    try:
        year_as_string = str(list_of_years[0][1])
        production_year = year_as_string[len(year_as_string) - 12:len(year_as_string) - 8]
    except IndexError:
        production_year = '0000'
    rating = get_rating(f'{movie_title} ({production_year})')
    return {'rating': rating, 'time': time_of_movie, 'cinema': 'AMONDO', 'title': movie_title, 'link': movie_url}

def fetch_info_iluzjon(movie_title, time_of_movie, production_year):
    rating = get_rating(f'{movie_title} ({production_year})')
    return {'rating': rating, 'time': time_of_movie,
            'cinema': 'ILUZJON', 'title': movie_title, 'link': url_iluzjon}


def get_rating(title_and_year):
    try:
        info = ia.get_movie(ia.search_movie(title_and_year)[0].getID())
        rating = info.data['rating']
        return rating
    except KeyError:
        return ''
    except IndexError:
        return ''


def get_year(production_year):
    try:
        int(production_year[-1])
        return production_year[-1].strip()
    except ValueError:
        return '0000'


def amondo(day):
    list_results = []
    url_beauty_soup_result = BeautifulSoup(make_request(url_amondo), 'html.parser')
    box_result = url_beauty_soup_result.find(id=f'schedule-{day}')
    try:
        list_links = [i.find('a')['href'] for i in box_result.find_all('div', class_='col-md-2 col-sm-3')]
        list_times = [i.text for i in box_result.find_all(class_='time')]
        if len(list_links) == 0:
            return []
        with ThreadPoolExecutor(len(list_links)) as executor:
            for result in executor.map(fetch_info_amondo, list_links, list_times):
                list_results.append(result)
        return list_results
    except AttributeError:
        return []


def iluzjon(day):
    list_result = []
    list_final_result = []
    list_h3 = BeautifulSoup(make_request(url_iluzjon), 'html.parser').find_all('h3')
    try:
        day_number = [int(i.text[0:2]) for i in list_h3].index(day)
        box = BeautifulSoup(make_request(url_iluzjon), 'html.parser').find_all('table')[day_number]
        list_title_and_time = [i.text.split(' - ') for i in box.find_all(class_='hour')]
        list_time = [list_title_and_time[i][0] for i in range(0, len(list_title_and_time), 1)]
        list_title = [list_title_and_time[i][1] for i in range(0, len(list_title_and_time), 1)]
        list_year = [i.text.split(',') for i in box.find_all('i')]
        with ThreadPoolExecutor(len(list_title)) as executor:
            for result in executor.map(get_year, list_year):
                list_result.append(result)
        with ThreadPoolExecutor(len(list_title)) as executor:
            for result in executor.map(fetch_info_iluzjon, list_title, list_time, list_result):
                list_final_result.append(result)
        return list_final_result
    except ValueError:
        return []


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
    Iluzjon = iluzjon(day=int(day[0].day))
    LISTA = merge(Amondo, Iluzjon)
    LISTA.sort(key=lambda x: str(x['rating']), reverse=True)
    return render_template('index.html', post=LISTA)


if __name__ == '__main__':
    app.run(debug=True)
