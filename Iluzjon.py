from concurrent.futures import ThreadPoolExecutor
from CinemaScraper import CinemaScraper


class Iluzjon(CinemaScraper):
    lista_shows = []
    numer = 0

    def __init__(self):
        self.base_url = 'https://www.iluzjon.fn.org.pl/repertuar.html'
        super().__init__(self.base_url)
        Iluzjon.numer += 1
        self.cinema = 'iluzjion'
        self.id = Iluzjon.numer

    def get_shows_list(self, lista):
        def get_year(info):
            try:
                int(info[-1])
                return info[-1].strip()
            except ValueError:
                return "0000"

        with ThreadPoolExecutor(len(lista)) as executor:
            for result in executor.map(get_year, lista):
                Iluzjon.lista_shows.append(result)

        return Iluzjon.lista_shows

    def get_result_map(self, time, title, year):
        def get_result(schedule, movie_title, realise_year):
            dane = CinemaScraper.Movie(title=movie_title, time=schedule, cinema='Iluzjon',
                                       year=realise_year, base_url=self.base_url)
            dane.set_rating()
            return dane.to_dictionary()

        with ThreadPoolExecutor(len(time)) as executor:
            for mapa in executor.map(get_result, time, title, year):
                CinemaScraper.result.append(mapa)
        return CinemaScraper.result
