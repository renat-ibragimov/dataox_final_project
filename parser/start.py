from datetime import datetime
from url_collector import UrlCollector
if __name__ == '__main__':
    start = datetime.now()
    UrlCollector()
    print(datetime.now() - start)
