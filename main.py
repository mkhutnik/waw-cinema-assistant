import datetime, imdb, requests
from concurrent.futures.thread import ThreadPoolExecutor
from pprint import pprint
from bs4 import BeautifulSoup
from flask import Flask, render_template

ia = imdb.IMDb()
list_without_duplicates = []
url_amondo = 'https://kinoamondo.pl/repertuar/'
url_iluzjon = 'https://www.iluzjon.fn.org.pl/repertuar.html'
app = Flask(__name__)


def html(url):
    response = requests.get(url)
    return response.text


def fetch_info_amondo(url, time):
    request = html(url)
    soup = BeautifulSoup(request, 'html.parser')
    title_1 = soup.find('h1').text
    year_list = [i.find_all_next('li') for i in soup.find_all('ul', class_='movie-info')]
    year_string = str(year_list[0][1])
    year = year_string[len(year_string) - 12:len(year_string)- 8]
    rating = get_rating(f'{title_1} ({year})')
    return {'rating': rating, 'time': time, 'cinema': 'AMONDO', 'title': title_1}

def fetch_info_iluzjon(title_p, time_p, year):
    title = title_p
    time = time_p
    rating = get_rating(f'{title_p} ({year})')
    return {'rating': rating, 'time': time, 'cinema': 'ILUZJON', 'title': title}


def get_rating(name):
    search = ia.search_movie(name)
    if len(search) == 0:
        return '0000'
    else:
        search = search[0].getID()
        rating = ia.get_movie(search)
        rating = rating.data['rating']
        return rating

def get_year(year):
    try:
        int(year[-1])
        return year[-1].strip()
    except ValueError:
        return '0000'


def amondo(data):
    lista =[]
    request = html(url_amondo)
    soup = BeautifulSoup(request, 'html.parser')
    box = soup.find(id=f'schedule-{data}')
    links = [i.find('a')['href'] for i in box.find_all('div', class_='col-md-2 col-sm-3')]
    time = [i.text for i in box.find_all(class_='time')]
    with ThreadPoolExecutor(len(links)) as executor:
        for result in executor.map(fetch_info_amondo, links, time):
            lista.append(result)
    return lista


def iluzjon():
    lista = []
    lista_2 = []
    request = html(url_iluzjon)
    box = BeautifulSoup(request, 'html.parser').table
    time_and_title = [i.text.split(' - ') for i in box.find_all(class_='hour')]
    time = [time_and_title[i][0] for i in range(0,len(time_and_title),1)]
    title = [time_and_title[i][1] for i in range(0, len(time_and_title), 1)]
    year = [i.text.split(',') for i in box.find_all('i')]
    with ThreadPoolExecutor(len(title)) as executor:
        for result in executor.map(get_year, year):
            lista.append(result)
    with ThreadPoolExecutor(len(title)) as executor:
        for result in executor.map(fetch_info_iluzjon, title, time, lista):
            lista_2.append(result)
    return lista_2


def merge(dic_1, dic_2):
    dic_1.extend(dic_2)
    pprint(dic_1)
    return dic_1


@app.route('/')
def front():
    return render_template('help.html')


@app.route('/final')
def final():
    AMONDO = amondo(datetime.datetime.now().date())
    ILUZJON = iluzjon()
    LISTA = merge(dic_1=AMONDO, dic_2=ILUZJON)
    return render_template('index.html', post=LISTA)

if __name__ == '__main__':
    app.run(debug=True)
