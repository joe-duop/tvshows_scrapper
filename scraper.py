#! python3

import requests
from bs4 import BeautifulSoup

"""
page1.html?sort=old
page2.html

#######  THE DATA STRUCTURE  ########
ep = {"sn": {"ep": "ep_url"}}
 
"""


class Scrapper:

    def __init__(self, seriesName):
        self.seriesName = seriesName
        self.series_url = ""
        self.seasons = {}  # sn_name: its_url
        self.episodes = {}  # ep = {"sn": {"ep": "ep_url"}}

    def ep(self):
        pass

    def sn_s(self):
        for sn in self.seasons.keys():
            url = self.seasons[sn]
            ep_elem = "html body div.container div.data_list div.data a"
            elem = self.find_element(url, ep_elem)
            # create the complex ds
            for i in elem:
                ep_name = str(i.get_text())
                ep_url = str(i.get("href"))

                dl_elem = "html body div.container div.data_list div.data a"
                elem = self.find_element(ep_url, dl_elem)
                down_link = elem[1].get("href")

                self.episodes.setdefault(sn, {})
                self.episodes[sn].setdefault(ep_name, down_link)

    def series_name_formatter(self, name):
        while " " in name:
            ind = 0
            l = list(name)
            if " " in l:
                ind = l.index(" ")
            name = name[:ind] + "+" + name[(ind + 1):]
        return name

    def the_seasons(self):
        sn_elem = "html body div.container div.data_list div.data a"
        self.series_url = self.get_series_url()
        elem = self.find_element(self.series_url, sn_elem)
        for i in elem:
            self.seasons[str(i.get_text())] = str(i.get("href"))
        print("series name - " + self.seriesName)
        print("seasons:")
        for i in self.seasons.keys():
            print("\t" + i)

    def get_series_url(self):
        """ return a string - the url of a series """
        url = 'https://google.com/search?q=' + self.series_name_formatter(self.seriesName) + '+tvshows4mobile'
        elem = self.find_search_elem(url)
        seriesPath = elem[0].get_text().split()
        url = "https://tvshows4mobile.com/" + seriesPath[1]
        return url

    def find_element(self, url, web_elem):
        """ downloads the webpage and gets the required web element """
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'}

        print("downloading " + url + " webpage")
        res = requests.get(url, headers=headers)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % exc)

        soup = BeautifulSoup(res.text, "html.parser")
        elems = soup.select(web_elem)
        if len(elems) > 0:
            return elems
        else:
            print("element was not found")

    def find_search_elem(self, url):
        elem = self.find_element(url, "span.dyjrff.qzEoUe")
        return elem
