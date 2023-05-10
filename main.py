import os
from bs4 import BeautifulSoup
import requests
import time
from fetcherwrapper import ALGSFetcherWrapper


def main():
    fw=ALGSFetcherWrapper()
    fetcher = fw.run_pipeline()
    #fetcher = fw.test_get_data()
    
if __name__ == '__main__':
    main()