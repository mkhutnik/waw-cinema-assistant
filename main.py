import datetime
import time
from concurrent.futures.thread import ThreadPoolExecutor

from flask import Flask, render_template, request

from Amondo import Amondo
from CinemaScraper import CinemaScraper
from Iluzjon import Iluzjon

DAYS = {
    'TODAY': datetime.datetime.now().date(),
    'TOMORROW': datetime.datetime.now().date() + datetime.timedelta(1),
    'DAY AFTER TOMORROW': datetime.datetime.now().date() + datetime.timedelta(2)
}

result = []
app = Flask(__name__)


def fetch_movie_info(url, time):
    cinema = CinemaScraper.Movie(base_url=url, time=time)
    cinema.set_title()
    cinema.set_year()
    cinema.set_cinema('Amondo')
    cinema.set_rating()
    return cinema.to_dictionary()

def amondo(number):
    cinema = Amondo()
    CinemaScraper.result = []
    box = cinema.html_parser().find(id=f'schedule-{number}')
    try:
        url_list = [i.find('a')['href'] for i in box.find_all('div', class_='col-md-2 col-sm-3')]
        if len(url_list) == 0:
            return []
    except AttributeError:
        return []
    time_list = [i.text for i in box.find_all(class_='time')]
    with ThreadPoolExecutor(len(url_list)) as executor:
        for mapa in executor.map(fetch_movie_info, url_list, time_list):
            CinemaScraper.result.append(mapa)
    return 0


def iluzjon(day_number):
    cinema = Iluzjon()
    headings = cinema.html_parser().find_all('h3')
    try:
        counter = [int(i.text[0:2]) for i in headings].index(day_number)
    except ValueError:
        return []
    show_table = cinema.find_elements_by_tag('table')[counter]
    show_table_hour = show_table.find_all(class_='hour')
    time_and_title = [i.text.split(' - ') for i in show_table_hour]
    list_times = [i[0] for i in time_and_title]
    list_title = [i[1] for i in time_and_title]
    years = [i.text.split(',') for i in show_table.find_all('i')]
    show_years = cinema.get_shows_list(years)
    cinema.get_result_map(list_times, list_title, show_years)
    return 0


@app.route('/')
def front():
    return render_template('help.html')


@app.route('/final', methods=['GET', 'POST'])
def final():
    start = time.time()
    date = DAYS[request.args.get('day')]
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(amondo, date)
        executor.submit(iluzjon, int(date.day))
    repertuar = CinemaScraper.result
    repertuar.sort(key=lambda x: str(x['rating']), reverse=True)
    print(time.time() - start)
    return render_template('index.html', post=repertuar)


if __name__ == '__main__':
    app.run()