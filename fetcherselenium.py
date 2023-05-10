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


class Fetcher():
    def __init__(self, url):
        print(url)
        self.url = url
        
    def set_driver(self):
        self.driver = webdriver.Chrome()

    def go_to_url(self):
        self.driver.get(self.url)

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
    
    BaseURL='https://apexlegendsstatus.com/'

    def __init__(self, url, **args):
        time.sleep(10)
        super().__init__(url)
        self.game_links=[]
        self.game_meta={}
        self.game_link_meta={} ## holy fuck we have to remove some of these attributes
        self.pipeline = {'statistics': self.get_game_stats_data, 'overview': self.game_meta, 'placement': self.get_game_placement_data}

    def set_game_meta(self, game_name, game_url):
        # url = '/'.join([self.BaseURL, self.config['season_split'], self.config['season_league'], region, 'Overview'])
        # meta to start as 
        url_split=self.url.replace(self.BaseURL, '').split('/')
        self.game_meta = {'season_split':url_split[1], 
                          'season_league':url_split[2], 
                          'region': url_split[3], 
                          'game_name': game_name}
        if '/'+game_url.replace(self.BaseURL, '') in self.game_link_meta.keys():
            self.game_meta.update(self.game_link_meta['/'+game_url.replace(self.BaseURL, '')])
        return self.game_meta

    def get_game_data_as_soup(self, url):
        '''
        game data page (eg: https://apexlegendsstatus.com/algs/game/09914f6562a97a9dc531f9b141fe482e/statsOverview) 
        needs some extra love to load it w/ selenium; this function provides the juice.
        '''
        #soup = self.get_url_as_soup(url=self.BaseURL+game_url+'/statsOverview')
        #<div class="loading" id="loader" style="display: none;">
        time.sleep(10)
        options = webdriver.ChromeOptions()
        #options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(10)
        print(f'driver get to url: {url}')
        driver.get(url=url)
        #element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "menu_statsOverview")))
        #print('found the below number of loader elements')
        #print(len(driver.find_elements(By.ID, 'loader')))
        # when we land on the page we get this ugly pop-up that tells us to change to a more optimized browser; we dont care
        # we just want to close that bitch.
        #WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element_attribute((By.ID, "loader"), 'style', 'display: none;'))
        WebDriverWait(driver, 15).until(EC.text_to_be_present_in_element_attribute((By.XPATH, "//div[@id='loader']"), 'style', 'display: none;'))
        elements = driver.find_elements(By.XPATH, "//button[@class='btn-close white']")
        self.try_to_click(element_list=elements)
        elements = driver.find_elements(By.XPATH, "//button[@class='btn btn-secondary']")
        self.try_to_click(element_list=elements)
        try:
            WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element_attribute((By.ID, "statsContent"), 'class', 'table white table-small dataTable no-footer'))
            page_source = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page_source, 'lxml')    
        except TimeoutException as e:
            driver.quit()
            soup = None
        return soup
    
    def get_placement_data_as_soup(self, url):
        '''
        game data page (eg: https://apexlegendsstatus.com/algs/game/09914f6562a97a9dc531f9b141fe482e/statsOverview) 
        needs some extra love to load it w/ selenium; this function provides the juice.
        '''
        #soup = self.get_url_as_soup(url=self.BaseURL+game_url+'/statsOverview')
        #<div class="loading" id="loader" style="display: none;">
        time.sleep(10)
        options = webdriver.ChromeOptions()
        #options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.implicitly_wait(10)
        print(f'driver get to url: {url}')
        driver.get(url=url)
        #element = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "menu_statsOverview")))
        #print('found the below number of loader elements')
        #print(len(driver.find_elements(By.ID, 'loader')))
        # when we land on the page we get this ugly pop-up that tells us to change to a more optimized browser; we dont care
        # we just want to close that bitch.
        #WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element_attribute((By.ID, "loader"), 'style', 'display: none;'))
        #WebDriverWait(driver, 15).until(EC.text_to_be_present_in_element_attribute((By.XPATH, "//div[@id='loader']"), 'style', 'display: none;'))
        #elements = driver.find_elements(By.XPATH, "//button[@class='btn-close white']")
        #self.try_to_click(element_list=elements)
        #elements = driver.find_elements(By.XPATH, "//button[@class='btn btn-secondary']")
        #self.try_to_click(element_list=elements)
        try:
            WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element_attribute((By.ID, "standingsLeaderboardDisplay"), 'class', 'table table_darker table-borderless center w-100'))
            page_source = driver.page_source
            driver.quit()
            soup = BeautifulSoup(page_source, 'lxml')    
        except TimeoutException as e:
            driver.quit()
            soup = None
        return soup
    
    def try_to_click(self, element_list):
        for el in element_list:
            try:
                el.click()
                #print('clicked')
            except Exception as e:
                #print(f'couldnt click the element!! {str(e)}')
                pass
        return None

    def get_game_stats_data_as_array(self, url):
        ## start w/ stats page since it has a lot of info in it (and is a nicer table)
        print(f"getting stats data from: {url+'/statistics'}")
        soup = self.get_game_data_as_soup(url=url+'/statistics')
        if soup:
            ## the below div has the stats data
            table = soup.find_all('table', {'id':'statsContent', 'class':'table white table-small dataTable no-footer'})
            assert len(table) == 1
            table = table[0]
            res = []
            headers=[i.text.replace('\xa0','') for i in table.find_all('th')]
            res.append(headers)
            for row in table.tbody.find_all('tr'):
                cols = row.find_all('td')
                res.append([i.text.replace('\xa0','') for i in cols])
            return res, soup.title.text
        else:
            # if we couldnt load the page then just fake a blank header, 1 blank row, and game_name.
            # the blank row won't be appended to the final result but the game_name will exist as a row...
            return None, 'Page Timeout - Could not pull data.'

    def get_placement_data_as_array(self, url):
        ##############################################################################################################
        ##############################################################################################################
        #################### skrr skrrr                             ##################################################
        ##############################################################################################################
        ##############################################################################################################
        soup = self.get_placement_data_as_soup(url=url)
        if soup:
            ## the below div has the stats data
            table = soup.find_all('table', {'id':'standingsLeaderboardDisplay', 'class':'table table_darker table-borderless center w-100'})
            assert len(table) == 1
            table = table[0]
            res = []
            headers=[i.text.replace('\xa0','') for i in table.find_all('th')]
            res.append(headers)
            for row in table.tbody.find_all('tr'):
                cols = row.find_all('td')
                res.append([i.text.replace('\xa0','') for i in cols])
            return res, soup.title.text
        else:
            # if we couldnt load the page then just fake a blank header, 1 blank row, and game_name.
            # the blank row won't be appended to the final result but the game_name will exist as a row...
            return None, 'Page Timeout - Could not pull data.'
    
    def append_game_meta(self, arr):
        arr[0].extend(list(self.game_meta.keys()))
        for i in arr[1:len(arr)]:
            i.extend(list(self.game_meta.values()))
        return arr

    def get_game_stats_data(self, url):
        gda, game_name = self.get_game_stats_data_as_array(url=url)
        if gda:
            game_meta = self.set_game_meta(game_name, url)
            gda = self.append_game_meta(gda)
        return gda

    def get_game_placement_data(self, url):
        print(f'getting placement data from {url}')
        gda, game_name = self.get_placement_data_as_array(url=url)
        if gda:
            game_meta = self.set_game_meta(game_name, url)
            gda = self.append_game_meta(gda)
        return gda 

    def get_game_urls_from_data_dir(self):
        print('we have game links on disk! reading them now')
        x=open('data/game_links.txt','r').readlines()
        return [i.replace('\n', '') for i in x]
        
    def save_game_urls_to_data_dir(self):
        print('we need to save game_links to disk!!')
        with open('data/game_links.txt', 'w') as f:
            f.writelines('\n'.join(self.game_links))

    def get_game_urls(self, url=None):
        '''
        need to remove game_link dependency b/c it's not needed anymore w/ game_link_meta
        '''
        if 'game_link_meta.json' in os.listdir('data/'):
            game_link_meta = self.get_game_link_meta_from_data_dir()
            self.game_links = [i for i in game_link_meta.keys() if i != '#']
            self.game_link_meta=game_link_meta
        else:
            url = self.url + '/Overview'
            soup = self.get_url_as_soup(url=url)
            game_link_meta={}
            x = soup.find_all('a', {'class': lambda l: 'algsGameElem linkNoStyle ' in l})
            for game in x:
                game_link_meta[game.attrs['href']] = {c: game.find('p', {'class': c}).text for c in ['gameTitle', 'gameMap']}
            all_links = [i for i in game_link_meta.keys() if i != '#']
            if '#' in game_link_meta.keys():
                game_link_meta.pop('#')
            self.game_links = all_links
            self.save_game_meta_as_json(game_link_meta)
            self.game_link_meta=game_link_meta
        return self.game_links

    def save_game_meta_as_json(self, game_link_meta):
        with open('data/game_link_meta.json', 'w') as f:
            json.dump(game_link_meta, f)
    
    def get_game_link_meta_from_data_dir(self):
        return json.load(open('data/game_link_meta.json', 'r'))

    def get_url_as_soup(self, url=None):
        if url in [None]:
            url = self.url
        options = webdriver.ChromeOptions()
        #options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, 'lxml')
        return soup
        

