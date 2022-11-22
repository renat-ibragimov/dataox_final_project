# dataox_final_project

## TASK

The purpose of this application is to collect, parse, save requested data
from the certain website and send it to API with the ability to apply filters.

## PREPARATION

 - Please clone repository to local machine 
 - As app is dockerized, Docker-Compose container should be built before using. 
   For this purpose use two commands:
   - docker-compose build
   - docker-compose up -d
 - Parser, DB and API will run automatically after docker-compose start
 - Parser can be started using "python3 start.py" command

## SHORT EXPLANATION

This app consists of three main parts: parser, database and API. 
Parser using ThreadPoolExecutor for URL Collector and asyncio with aiohttp for Data Collector.
The simplified sequence looks like:
website: <request-response> :ulr_collector: set of unique urls-> data_collector: scraped data-> 
data_parser: parsed and validated data-> database: <request-data> :API: <filter request-data>  