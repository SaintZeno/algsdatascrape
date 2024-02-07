# algsdatascrape
Selenium Scraper used to scrape ALGS data from https://apexlegendsstatus.com/algs/

pipeline updated such that scraper pulls and stores each game in db (statistics table and placement table) 
then create a separate job which queries db for stats/placement filtered on region/split/season this
job will join the two tables. next is a function to clean data and do the etl. then dump to db