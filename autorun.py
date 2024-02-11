import schedule
import time

from app import data
from config import host, user, password, db_name, dump_folder
from dump import backup_database

from datetime import datetime

scraping_start_time = "12:00"
db_backup_time = "00:00"

# Starting scraping function
schedule.every().day.at(scraping_start_time).do(data)

# Need this to fix backup file name(: is not supported)
current_dt = str(datetime.today()).replace(':', "-")

# Starting db backup function
schedule.every().day.at(db_backup_time).do(lambda: backup_database(host, user, password, db_name, dump_folder, current_dt))

# Uncomment to run scraping function
# data()

# Uncomment to run db_backup function
# backup_database(host, user, password, db_name, dump_folder, current_dt)

while True:
    schedule.run_pending()
    time.sleep(1)
