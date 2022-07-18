from datetime import datetime, timedelta
import zoneinfo
import dateutil
import pytz
from exchangelib import EWSTimeZone, EWSDateTime, EWSDate, UTC, UTC_NOW,Credentials, Configuration, DELEGATE, Account
from datetime import datetime, timedelta, timezone
pytz_tz = pytz.timezone('Asia/Jerusalem')
# tz = EWSTimeZone('Asia/Jerusalem')
# tz = EWSTimeZone.localzone()
tz = EWSTimeZone('UTC')

start_time_year = 2022
start_time_month = 7
start_time_day = 14
localized_dt = EWSDateTime(start_time_year, start_time_month, start_time_day, 8, 30, tzinfo=tz)


# py_dt = datetime(2017, 12, 11, 10, 9, 8, tzinfo=tz)
py_dt = datetime.now(pytz.utc)+ timedelta(days=-1)
py_dt = py_dt.replace(tzinfo=UTC)

yesterday = EWSDateTime.from_datetime(py_dt)

tz = EWSTimeZone.localzone()
py_dt = pytz_tz.localize(datetime(start_time_year, start_time_month, start_time_day))
tomorrow = datetime.today() + timedelta(days=1)


creds = Credentials(
    username="trot\\task",
    password="__pool$&^2224"
)
config = Configuration(server='mail.trot.co.il', credentials=creds)

account = Account(
    primary_smtp_address="jonathan@trot.co.il",
    autodiscover=False,
    config=config,
    access_type=DELEGATE
)

root = account.public_folders_root
pubs = (root.glob('*סידור עבודה'))

ews_now = EWSDateTime.now(tz)
# for occurrence in pubs.view(start=yesterday, end=ews_now):
#     try:
#         print(occurrence.start, occurrence.subject)
#     except:
#         pass

