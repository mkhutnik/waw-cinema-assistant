import requests
from bs4 import BeautifulSoup

def add_info(lista_info):
    return CinemaScraper.result.append(lista_info)

class CinemaScraper:
    result = []

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self._html = None

    def make_request(self):
        return requests.get(self.base_url).text

    def html_parser(self):
        if self._html is None:
            self._html = BeautifulSoup(self.make_request(), 'html.parser')
        return self._html

    def find_elements_by_tag(self, tag):
        if self._html is None:
            self._html = BeautifulSoup(self.make_request(), 'html.parser')
        return self._html.find_all(tag)