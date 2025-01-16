from concurrent.futures.thread import ThreadPoolExecutor

from CinemaScraper import CinemaScraper
from Movie import Movie


class Amondo(CinemaScraper):
    numer = 0
    url = []

    def __init__(self):
        self.base_url = 'https://kinoamondo.pl/repertuar'
        super().__init__(self.base_url)
        Amondo.numer += 1
        self.cinema = 'amondo'
        self.id = Amondo.numer


    def retrive_movie_info(self, number):
        def __fetch_movie_info(url, time):
            movie = Movie(base_url=url, time=time)
            movie.set_title()
            movie.set_year()
            movie.set_cinema('Amondo')
            movie.set_rating()
            return movie.to_dictionary()

        box = self.html_parser().find(id=f'schedule-{number}')
        try:
            url_list = [i.find('a')['href'] for i in
                        box.find_all('div', class_='col-md-2 col-sm-3')]
        except AttributeError:
            return []

        time_list = [i.text for i in box.find_all(class_='time')]
        if Amondo.numer > self.id:
            return 0

        with ThreadPoolExecutor(len(url_list)) as executor:
            for mapa in executor.map(__fetch_movie_info,
                                     url_list, time_list):
                CinemaScraper.result.append(mapa)

        return 0





