import datetime
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

app = Flask(__name__)


def amondo(number):
    CinemaScraper.result = []
    cinema = Amondo()
    cinema.retrive_movie_info(number)
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

    if cinema.numer > cinema.id:
        return 0

    show_years = cinema.get_shows_list(years)
    cinema.get_result_map(list_times, list_title, show_years)
    return 0


@app.route('/')
def front():
    return render_template('help.html')

@app.route('/final', methods=['GET', 'POST'])
def final():
    date = DAYS[request.args.get('day')]

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(amondo, date)
        executor.submit(iluzjon, int(date.day))

    repertuar = CinemaScraper.result
    repertuar.sort(key=lambda x: str(x['rating']), reverse=True)

    return render_template('index.html', post=repertuar)


if __name__ == '__main__':
    app.run()
