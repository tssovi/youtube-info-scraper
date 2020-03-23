import time
import threading
from datetime import datetime
from common.data_loader import data_loader
from youtube_scraper.settings import DATA_UPDATE_INTERVAL


class StartAutoUpdater():
    def __init__(self):
        # Set data update min interval
        self.interval = DATA_UPDATE_INTERVAL

        thread = threading.Thread(target=self.run, args=())
        thread.start()

    def run(self):
        while True:
            date_str = datetime.now().__str__()
            print("Time: {} - Run Auto Updater".format(date_str))
            flag = data_loader([])
            if flag:
                print("\nData Updated Successfully\n")

            time.sleep(self.interval)

