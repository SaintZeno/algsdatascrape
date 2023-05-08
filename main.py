import os
from bs4 import BeautifulSoup
import requests
import time
from fetcherselenium import ALGSFetcherWrapper


def main():
    fw=ALGSFetcherWrapper()
    fetcher = fw.get_data()
    #fetcher = fw.test_get_data()
    
if __name__ == '__main__':
    main()