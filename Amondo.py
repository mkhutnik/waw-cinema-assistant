from CinemaScraper import CinemaScraper


class Amondo(CinemaScraper):
    numer = 0
    url = []
    def __init__(self):
        self.base_url = 'https://kinoamondo.pl/repertuar'
        super().__init__(self.base_url)
        Amondo.numer += 1
        self.cinema = 'amondo'
        self.id = Amondo.numer

    def retrive_urls(self, id, allData=None):
        data = self.html_parser().find_all(id = id)
        nested_url = data.find_all('div', class_='col-md-2 col-sm-3')
        allData.find_all(class_='time')




