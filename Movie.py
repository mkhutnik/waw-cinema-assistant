import imdb

from CinemaScraper import CinemaScraper

class Movie:
    IA = imdb.IMDb()
    def __init__(
            self, time, base_url, title=None, cinema=None, year=None,
            rating=None):
        self.base_url = base_url
        self.time = time
        self.title = title
        self.cinema = cinema
        self.year = year
        self.rating = rating

    def set_title(self):
        self.title = CinemaScraper(self.base_url).find_elements_by_tag(
            'h1'
        )[0].text
        return self.title

    def set_cinema(self, cinema_name):
        self.cinema = cinema_name

    def set_rating(self):
        try:
            info = Movie.IA.get_movie(
                Movie.IA.search_movie(f'{self.title} ({self.year})')[0].getID())
            self.rating = info.data['rating']
        except (KeyError, IndexError):
            self.rating = ''

    def set_year(self):
        try:
            year_str = str([i.find_all_next('li') for i in
                            CinemaScraper(self.base_url)._html.find_all(
                                'ul',  class_='movie-info')][0][1])
            self.year = year_str[len(year_str) - 12:len(year_str) - 8]
        except (IndexError, AttributeError):
            self.year = '0000'

    def to_dictionary(self):
        return {
            'rating': self.rating,
            'time': self.time,
            'cinema': self.cinema,
            'title': self.title,
            'link': self.base_url
        }