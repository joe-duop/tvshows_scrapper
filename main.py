import pprint
from scraper import Scrapper

if __name__ == '__main__':
    series = Scrapper("p-valley")
    series.the_seasons()
    series.sn_s()
    pprint.pprint(series.episodes)

