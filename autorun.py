import schedule
import time

from test import data
from config import host, user, password, db_name, dump_folder
from dump import backup_database

from datetime import datetime


schedule.every().day.at("12:00").do(data)

dt = str(datetime.today()).replace(':', "-")

schedule.every().day.at("00:00").do(lambda: backup_database(host, user, password, db_name, dump_folder, dt))


while True:
    schedule.run_pending()
    time.sleep(1)
