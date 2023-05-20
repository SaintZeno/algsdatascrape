import os
from bs4 import BeautifulSoup
import requests
import time
import yaml
from selenium import webdriver ## sorry mom, i've joined the dark side!
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import json
from helpers import progressbar
from fetcherselenium import ALGSFetcher


class ALGSFetcherWrapper():
    
    Fetchers={'ALGSFetcher': ALGSFetcher}
    
    BaseURL='https://apexlegendsstatus.com'


    def __init__(self, **args):
        self.config = self.get_config()
        self.url='/'.join([self.BaseURL, 'algs', self.config['season_split'], self.config['season_league'], self.config['region']])
        self.output_file_name_prefix = f"{self.config['pipeline']}{self.config['season_split']}{self.config['season_league']}{self.config['region']}"
        self.fetcher=self.Fetchers[self.config['fetcher']](self.url)
        pass
    
    def run_pipeline(self):
        self.get_helper_data()
        self.create_get_iterator()
        self.get_data()
        pass

    def create_get_iterator(self):
        if self.config['pipeline'] == 'statistics':
            self.get_iterator = self.fetcher.game_links
        if self.config['pipeline'] == 'game_placement':
            self.get_iterator = self.fetcher.game_links
        if self.config['pipeline'] == 'overall_placement':
            pref = '/'.join(['algs', self.config['season_split'], self.config['season_league'], self.config['region']])
            self.get_iterator = [f'/{pref}/Day{i}' for i in range(1,10)] + [f'/{pref}/Finals']

    def get_helper_data(self):
        ## hardcoded for now... need to config this
        ## eventually we'll have more helper data ?
        if self.config['pipeline']=='statistics':
            self.fetcher.get_game_urls()
        if self.config['pipeline']=='game_placement':
            self.fetcher.get_game_urls()        
        pass

    def get_data(self):
        pipeline_result=[]
        
        for i in progressbar(range(len(self.get_iterator)), "Fetching: ", 40):
            url = self.BaseURL + self.get_iterator[i] 
            pipeline_result_array = self.fetcher.pipeline[self.config['pipeline']](url=url)
            if pipeline_result_array:
                pipeline_result.extend(pipeline_result_array)
                self.write_arr_as_csv(pipeline_result, file_name=f'{self.output_file_name_prefix}-subfile.csv')
        self.write_arr_as_csv(pipeline_result, file_name=f'{self.output_file_name_prefix}-fullfile.csv')
        if "game_link_meta.json" in os.listdir('data/'):
            os.remove("data/game_link_meta.json")

    def write_arr_as_csv(self, arr, file_name=None):
        if file_name in [None]:
            file_name='statistics.csv'
        if file_name[-3:] != 'csv':
            file_name+='.csv'
        with open(f'results/{file_name}', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(arr)
        return True

    def get_config(self, file_name='algs.yml'):
        return yaml.safe_load(open(file_name, 'r'))

