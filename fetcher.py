import os
from bs4 import BeautifulSoup
import requests
import time
import yaml

class Fetcher():
    def __init__(self, url):
        self.url = url
        print(url)
        self.headers={'User-Agent': "Chrome/42.0.2311.135"}
    
    def fetch_url_as_bs4_obj(self):
        r = requests.get(url=self.url, headers=self.headers)
        #return r, BeautifulSoup(r.content, 'html.parser')
        return r, BeautifulSoup(r.content, 'html5lib')

    def soup_findall(self, soup_obj, findall_dict):
        '''
        findall_dict = {'to_find':'div', 'filters':{"id" : re.compile('date.*')}}
        '''
        return soup_obj.find_all(findall_dict['to_find'], findall_dict['filters'])


class ALGSFetcher(Fetcher):
    def __init__(self, url, **args):
        time.sleep(15)
        super().__init__(url)


    def get_game_urls(self):
        #<a class="algsGameElem linkNoStyle worldsedgeBg" href="/algs/game/09914f6562a97a9dc531f9b141fe482e" target="_blank">
        r, soup = self.fetch_url_as_bs4_obj()
        soup_game = soup.find_all('a')
        #soup_game = self.soup_findall(soup, {'to_find':'a', 'filters':{'class': lambda l: 'algsGameElem linkNoStyle ' in l}})
        return soup_game
        
class ALGSFetcherWrapper():
    
    Fetchers=[ALGSFetcher]
    BaseURL='https://apexlegendsstatus.com/algs'
    
    def __init__(self, **args):
        self.config = self.get_config()
        pass
    
    def get_data(self):
        for region, page in self.config['region_page'].items():
            #/Y3-Split1/Pro-League/EMEA/Overview
            url = '/'.join([self.BaseURL, self.config['season_split'], self.config['season_league'], region, 'Overvieww'])
            fetcher = ALGSFetcher(url=url)
            print(fetcher.get_game_urls())
            
        
    def get_config(self, file_name='algs.yml'):
        return yaml.safe_load(open(file_name, 'r'))

